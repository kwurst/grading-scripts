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
