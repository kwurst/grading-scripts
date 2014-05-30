import unittest
import sandbox
from command import Command
from pathlib import Path


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


if __name__ == '__main__':
    unittest.main()
