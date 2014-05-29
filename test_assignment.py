import unittest
import sandbox
import os.path
import assignment


class test_Assignmnet(unittest.TestCase):

    def setUp(self):
        self.collector = Collector()

    def test_each(self):
        the_assignment = assignment.new(sandbox.dir('assignment1.json'))
        the_assignment.accept(self.collector.visit)
        self.assertPathsExist()

    def assertPathsExist(self):
        self.assertTrue(self.collector.directories, msg="No directories collected.")
        self.assertTrue(self.collector.files, msg="No files collected.")
        for d in self.collector.directories:
            self.assertTrue(d.exists(), msg="Directory does not exist: " + str(d))
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


if __name__ == '__main__':
    unittest.main()
