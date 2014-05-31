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
import os.path
from assignment import Assignment


class test_Assignment(unittest.TestCase):

    def setUp(self):
        self.collector = Collector()

    def test_each(self):
        the_assignment = Assignment(sandbox.dir('assignment1.json'))
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
