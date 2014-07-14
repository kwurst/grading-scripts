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
import tests.sandbox as sandbox
from submissions import Assignment, Command
from pathlib import Path


class test_Assignment(unittest.TestCase):

    def setUp(self):
        self.collector = Collector()

    def test_each(self):
        the_assignment = Assignment(sandbox.dir('assignment1.json'))
        the_assignment.accept(self.collector.visit)
        self.assertPathsExist()

    def assertPathsExist(self):
        self.assertTrue(
            self.collector.directories, msg="No directories collected.")
        self.assertTrue(self.collector.files, msg="No files collected.")
        for d in self.collector.directories:
            self.assertTrue(
                d.exists(), msg="Directory does not exist: " + str(d))
            self.assertTrue(d.is_dir(), msg="Not a directory: " + str(d))
        for f in self.collector.files:
            self.assertTrue(f.exists(), msg="File does not exist: " + str(f))
            self.assertTrue(f.is_file(), msg="Not a file: " + str(f))


class Collector(object):
    def __init__(self):
        self.directories = []
        self.files = []

    def visit(self, submission_directory, files_to_collect):
        self.directories.append(submission_directory)
        for file in files_to_collect:
            self.files.append(file)




class test_Command(unittest.TestCase):

    def setUp(self):
        self.directory = Path(sandbox.dir('test_Command'))
        self.directory.mkdir()
        self.file_ = self.directory / 'test_simple'
        self.filename = str(self.file_)

    def tearDown(self):
        for f in self.directory.glob('*'):
            f.unlink()
        self.directory.rmdir()

    def test_simple(self):
        touch = Command('touch ' + self.filename)
        remove = Command('rm ' + self.filename)
        touch()
        self.assertTrue(self.file_.exists())
        remove()
        self.assertTrue(not self.file_.exists())

    def test_implicit_ins(self):
        touch, remove = self._get_parameterized_commands()
        touch(self.file_)
        self.assertTrue(self.file_.exists())
        remove(self.file_)
        self.assertTrue(not self.file_.exists())

    def _get_parameterized_commands(self):
        touch = Command('touch {ins}')
        remove = Command('rm {ins}')
        return (touch, remove)

    def test_explicit_ins(self):
        touch, remove = self._get_parameterized_commands()
        touch(ins=self.file_)
        self.assertTrue(self.file_.exists())
        remove(ins=self.file_)
        self.assertTrue(not self.file_.exists())

    def test_list_ins(self):
        touch, remove = self._get_parameterized_commands()
        touch(ins=[self.file_, self.filename+'2'])
        self.assertTrue(self.file_.exists(), msg="File: {}".format(self.file_))
        self.assertTrue(Path(self.filename+'2').exists())
        remove(ins=[self.file_, self.filename+'2'])
        self.assertTrue(not self.file_.exists())
        self.assertTrue(not Path(self.filename+'2').exists())

    def test_explicit_outs(self):
        touch, remove = self._get_parameterized_commands()
        touch(self.file_)
        copy = Command('cat {ins} > {outs}')
        copy(self.file_, outs=self.filename+'2')
        self.assertTrue(Path(self.filename+'2').exists())

    def test_implicit_outs(self):
        touch, remove = self._get_parameterized_commands()
        touch(self.file_)
        copy = Command('cat {ins} > {outs}')
        copy(self.file_, self.filename+'2')
        self.assertTrue(Path(self.filename+'2').exists())

    def test_only_outs(self):
        write_hi = Command('echo hi > {outs}')
        write_hi(outs=self.file_)
        self.assertTrue(self.file_.exists())

    def test_format_args_noneReturnsNone(self):
        command = Command('')
        self.assertIsNone(command._format_args(None))

    def test_format_args_oneReturnsQuoted(self):
        command = Command('')
        result = command._format_args('hi')
        self.assertEquals('"hi"', result)

    def test_format_args_quotesEscaped(self):
        command = Command('')
        original = '"hi"'
        expected = '"\\"hi\\""'
        result = command._format_args(original)
        self.assertEquals(expected, result)

    def test_format_args_list(self):
        command = Command('')
        original = [ 'hi', 'mom', '"how"' ]
        expected = '"hi" "mom" "\\"how\\""'
        result = command._format_args(original)
        self.assertEquals(expected, result)

if __name__ == '__main__':
    unittest.main()
