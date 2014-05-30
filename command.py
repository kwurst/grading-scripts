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
    def __init__(self, command_string):
        self._command_string = command_string

    def __call__(self, ins=None, outs=None):
        ins = self._format_args(ins)
        outs = self._format_args(outs)
        if ins is None and outs is None:
            command = self._command_string
        elif ins is None:
            command = self._command_string.format(outs=outs)
        elif outs is None:
            command = self._command_string.format(ins=ins)
        else:
            command = self._command_string.format(ins=ins, outs=outs)
        os.system(command)

    def each(self, ins=None, outs=None):
        for i in range(len(ins)):
            ins_i = ins[i]
            if isinstance(outs, list):
                outs_i = outs[i]
            else:
                outs_i = outs
            self(ins_i, outs_i)

    def _format_args(self, args):
        if args is None:
            return None
        if isinstance(args, list):
            return '" "'.join([str(i) for i in args])
        elif not isinstance(args, str):
            return str(args)
        return args
