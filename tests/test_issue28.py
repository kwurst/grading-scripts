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
import unittest
import os.path
import os
from io import StringIO
import sys
import tests.sandbox as sandbox
from submissions import Assignment, Command


OUTFILE = sandbox.dir('issue28.txt')


class test_issue28(unittest.TestCase):

    def tearDown(self):
        if os.path.isfile(OUTFILE):
            os.remove(OUTFILE)

    def test_missingFile_keepGoing(self):
        out = self._get_stdout_as_StringIO()
        try:
            collector = Collector(OUTFILE)
            Assignment(sandbox.dir('issue28.json')).accept(collector.visit)
            self.assertTrue(len(collector.get_lines()) == 5)
            output = out.getvalue().strip()
        finally:
            self._restore_stdout()

    def _get_stdout_as_StringIO(self):
        self._saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        return out

    def _restore_stdout(self):
        sys.stdout = self._saved_stdout


class Collector(object):
    def __init__(self, file_):
        self._file = file_
        self.ls = Command('ls "{ins}" >> ' + file_)

    def visit(self, submission_directory, files_to_collect):
        for file in files_to_collect:
            self.ls(file)

    def get_lines(self):
        lines = []
        with open(self._file) as outfile:
            lines = outfile.readlines()
        return lines



if __name__ == '__main__':
    unittest.main()
