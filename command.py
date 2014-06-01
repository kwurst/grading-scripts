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
import os
import assignment


class Command(object):
    '''
    Command represents a reusable shell command.

    Examples creating a command:

        concat = Command('cat "{ins}" > "{outs}"')
        concat2 = Command('cat "{ins}" > "{ins}.2"')

    IMPORTANT: Always encluse placeholders in double quotes.

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
    _default_verbosity = False

    @classmethod
    def set_default_verbosity(cls, flag):
        cls._default_verbosity = flag

    def __init__(self, command_string, verbose=None):
        self._verbose = \
            verbose if verbose is not None else Command._default_verbosity
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
            return '" "'.join([str(i) for i in args])
        elif not isinstance(args, str):
            return str(args)
        return args

    def _run_command(self, command):
        if self._verbose:
            print(command)
        os.system(command)

    def each(self, ins=None, outs=None):
        for i in range(len(ins)):
            ins_i = ins[i]
            outs_i = outs[i] if isinstance(outs, list) else outs
            self(ins_i, outs_i)
