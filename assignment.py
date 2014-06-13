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
import pathlib
import json
import os


class Assignment(object):
    '''Provides traversal and path resolution for visitors over an assignment
    directory.
    '''

    def __init__(self, config_file, verbose=False, cd=True):
        self._config_file = pathlib.Path(config_file).resolve()
        self._verbose = verbose
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
        if self._verbose:
            print('Processing', directory)

    def _notify_end_process_directory(self, directory):
        if self._verbose:
            print('Done processing', directory)

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
            print('Not found: ' + str(root/path))
        return resolved
