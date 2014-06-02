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
import json
import os.path
import os
import sandbox


CONFIG_FILENAME = sandbox.dir('assignment1.json')


class test_Json(unittest.TestCase):
    def test_canLoadJsonFile(self):
        config_string = ''
        with open(CONFIG_FILENAME) as f:
            config_string = f.read()
        config = json.loads(config_string)
        self.assertTrue('directory' in config)
        self.assertTrue('files' in config)
        self.assertTrue(isinstance(config['directory'], str))
        self.assertTrue(isinstance(config['files'], list))
        self.assertTrue(all([isinstance(x, str) for x in config['files']]))


if __name__ == '__main__':
    unittest.main()
