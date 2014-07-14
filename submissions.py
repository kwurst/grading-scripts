# Copyright (C) 2014 Karl R. Wurst
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
import argparse
import logging
import json
import os
import pathlib


class SubmissionProcessor(object):
    '''
    Base class for submission processors. To use:
        1) Inherit.
        2) Call super constructor.
        3) Optionally set self.cd = False to prevent changing into each
        submission directory before calling process_submissions.
        4) Implement process_submission.
    '''
    def __init__(self):
        self.cd = True
        self._arguments = CommandLineArguments()
        self._init_logging()
        self._assignment = Assignment(self._arguments.config)

    def _init_logging(self):
        if self._arguments.verbose:
            logging.basicConfig(level='DEBUG')
        elif self._arguments.brief:
            logging.basicConfig(level='WARNING')
        else:
            logging.basicConfig(level='INFO')

    def run(self):
        self._assignment.accept(self.process_submission, self.cd)

    def process_submission(self, directory, files):
        '''
        Called once for each submission directory. `directory` is a
        `pathlib.Path` to the submission directory. `files` is a possibly empy
        list of `pathlib.Path`s to files in `directory` to process.  The paths
        in `files` have been resolved against directory. All `files` exist.
        '''
        raise NotImplementedError('Must implement.')

    def command(self, shell_string):
        '''
        Returns a `Command` for the given `shell_string`.
        '''
        return Command(shell_string)


class CommandLineArguments(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('config', help='JSON configuration file')
        self._parser.add_argument(
            '-v', '--verbose',
            help='increase output verbosity',
            action='store_true',
            default=False
            )
        self._parser.add_argument(
            '-b', '--brief',
            help='decrease output verbosity',
            action='store_true',
            default=False
            )
        self._parser.parse_args(namespace=self)


class Assignment(object):

    def __init__(self, config_file, cd=True):
        self._config_file = pathlib.Path(config_file).resolve()
        self._cd = cd
        self._config_dict = None
        self._submission_directories = []

        self._load_config()
        self._load_submission_directories()

    def _load_config(self):
        self._config_dict = self._read_config()
        self._config_dict['directory'] = self._resolve_path(
            self._config_dict['directory'],
            root=self._config_file.parent
            )
        self._config_dict['files'] = [
            pathlib.Path(file_) for file_ in self._config_dict['files']
            ]

    def _read_config(self):
        config = None
        with self._config_file.open() as file_:
            config = json.load(file_)
        return config

    def _load_submission_directories(self):
        self._submission_directories = [
            self._resolve_path(d, root=self._config_dict['directory'])
            for d in self._config_dict['directory'].glob('*')
            if d.is_dir()
            ]

    @staticmethod
    def _resolve_path(path, root=None):
        path = pathlib.Path(path)
        if path.is_absolute():
            return path
        elif root is None:
            return path.resolve()
        else:
            return (pathlib.Path(root).resolve() / path).resolve()

    def accept(self, visit, cd=None):
        '''
        Calls visit(directory, files) for each submission directory.  Directory
        is a pathlib.Path that is the submission directory being visited. Files
        is a list of pathlib.Path objects that are the files within the
        directory to process.

        visit: callable

        cd: boolean - defaults True - uses accept to change into each
            submission directory.
        '''
        self._cd = cd if cd is not None else self._cd
        for directory in self._submission_directories:
            self._notify_start_process_directory(directory)
            self._process_directory(visit, directory)
            self._notify_end_process_directory(directory)

    def _notify_start_process_directory(self, directory):
        logging.info('Processing {directory}'.format(directory=directory))

    def _notify_end_process_directory(self, directory):
        logging.info('Done processing {directory}'.format(directory=directory))

    def _process_directory(self, visit, directory):
        self._enter_directory(directory)
        visit(directory, self._get_resolved_files(directory))
        self._exit_directory()

    def _enter_directory(self, directory):
        if self._cd:
            self._original_directory = pathlib.Path.cwd()
            os.chdir(str(directory))

    def _exit_directory(self):
        if self._cd:
            os.chdir(str(self._original_directory))

    def _get_resolved_files(self, root):
        resolved_or_none = [
                self._resolve_path_or_none(f, root=root)
                for f in self._config_dict['files']]
        resolved = [f for f in resolved_or_none if f is not None]
        return resolved
    
    def _resolve_path_or_none(self, path, root=None):
        resolved = None
        try:
            resolved = self._resolve_path(path, root=root)
        except FileNotFoundError:
            logging.warning('Not found: {path}'.format(path=str(root/path)))
        return resolved


class Command(object):
    '''
    Command represents a reusable shell command.

    Examples creating a command:

        concat = Command('cat {ins} > {outs}')
        concat2 = Command('cat {ins} > {ins}.2')

    {ins} and {outs} will be replaced by the parameters passed to the command
    when called. These parameters will be quoted when substituted in. So, do not
    quote.

    Example calls:

        concat('f1', 'f2')  # copies f1 to f2
        concat(['f1', 'f2'], 'f3')  # lists, concats f1 and f2 into f3
        concat(pathlib.Path('f1'), 'f2')  # you may pass Paths.
        concat(o1, o2)  # o1 and o2 will be converted to a string via str().
        concat(Path('.').glob('*.txt'), 'out.txt')  # globbing
        concat(outs='f3', ins=['f1', 'f2'])  # named parameters
        concat2('f1')  # copies f1 to f1.2 ; optional parameters
        concat2.each(['f1', 'f2])  # copies f1 to f1.2 and f2 to f2.2
        concat.each(['f1', 'f2'], ['f3', 'f4'])  # copies f1 to f3 and f2 to f4
    '''

    def __init__(self, command_string):
        self._command_string = command_string

    def __call__(self, ins=None, outs=None):
        ins = self._format_args(ins)
        outs = self._format_args(outs)
        command = self._command_string.format(ins=ins, outs=outs)
        self._run_command(command)

    def _format_args(self, args):
        if args is None:
            return None
        if isinstance(args, list):
            return ' '.join([self._format_args(arg) for arg in args])
        elif not isinstance(args, str):
            args_string =  str(args)
        else:
            args_string = args
        args_string = args_string.replace('"', '\\"')
        args_string =  '"' + args_string + '"'
        return args_string


    def _run_command(self, command):
        logging.debug(command)
        os.system(command)

    def each(self, ins=None, outs=None):
        for i in range(len(ins)):
            ins_i = ins[i]
            outs_i = outs[i] if isinstance(outs, list) else outs
            self(ins_i, outs_i)
