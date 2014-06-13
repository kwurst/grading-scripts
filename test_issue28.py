import unittest
import sandbox
import os.path
import os
from assignment import Assignment
from command import Command


OUTFILE = sandbox.dir('issue28.txt')


class test_issue28(unittest.TestCase):

    def tearDown(self):
        if os.path.isfile(OUTFILE):
            os.remove(OUTFILE)

    def test_missingFile_keepGoing(self):
        collector = Collector()
        Assignment(sandbox.dir('issue28.json')).accept(collector.visit)
        lines = []
        with open(OUTFILE) as outfile:
            lines = outfile.readlines()
        self.assertTrue(len(lines) == 5)


class Collector(object):
    def __init__(self):
        self.ls = Command('ls "{ins}" >> ' + OUTFILE)

    def visit(self, submission_directory, files_to_collect):
        for file in files_to_collect:
            self.ls(file)


if __name__ == '__main__':
    unittest.main()
