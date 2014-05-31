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
import sandbox
from command import Command
from pathlib import Path


class test_Command(unittest.TestCase):

    def setUp(self):
        Command.set_default_verbosity(False)
        self.directory = Path(sandbox.dir('test_Command'))
        self.directory.mkdir()
        self.file_ = self.directory / 'test_simple'
        self.filename = str(self.file_)

    def tearDown(self):
        Command.set_default_verbosity(False)
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
        touch = Command('touch "{ins}"')
        remove = Command('rm "{ins}"')
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
        self.assertTrue(self.file_.exists())
        self.assertTrue(Path(self.filename+'2').exists())
        remove(ins=[self.file_, self.filename+'2'])
        self.assertTrue(not self.file_.exists())
        self.assertTrue(not Path(self.filename+'2').exists())

    def test_explicit_outs(self):
        touch, remove = self._get_parameterized_commands()
        touch(self.file_)
        copy = Command('cat "{ins}" > "{outs}"')
        copy(self.file_, outs=self.filename+'2')
        self.assertTrue(Path(self.filename+'2').exists())

    def test_implicit_outs(self):
        touch, remove = self._get_parameterized_commands()
        touch(self.file_)
        copy = Command('cat "{ins}" > "{outs}"')
        copy(self.file_, self.filename+'2')
        self.assertTrue(Path(self.filename+'2').exists())

    def test_only_outs(self):
        write_hi = Command('echo hi > "{outs}"')
        write_hi(outs=self.file_)
        self.assertTrue(self.file_.exists())

    def test_default_verbosity_is_false(self):
        ls = Command('ls')
        self.assertFalse(ls._verbose)

    def test_verbosity_true(self):
        ls = Command('ls', verbose=True)
        self.assertTrue(ls._verbose)

    def test_set_default_verbosity_true(self):
        Command.set_default_verbosity(True)
        ls = Command('ls')
        self.assertTrue(ls._verbose)

    def test_override_default_verbosity_false(self):
        Command.set_default_verbosity(True)
        ls = Command('ls', False)
        self.assertFalse(ls._verbose)


if __name__ == '__main__':
    unittest.main()
