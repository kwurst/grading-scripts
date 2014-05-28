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

# This script will run another script on all subdirectories of a particular directory

# run as:
# python process-all-subdirectories.py directory script
#
# the script name should not end in .py
#
# the script should have a process function that takes a directory name as a parameter

import argparse
import os
import importlib
import json


def main():
    args = parse_command_line_arguments()
    config = load_json_configuration(args.config)
    script = import_(args.script)
    directories = get_student_directories(config['directory'])
    run_script_on_directories_with_config(script, directories, config)


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Path to JSON configuration file')
    parser.add_argument('script', help='Processing script')
    return parser.parse_args()


def load_json_configuration(filename):
    config_string = ''
    with open(filename) as config_file:
        config_string = config_file.read()
    return json.loads(config_string)


def import_(scriptname):
    print(scriptname)
    return importlib.import_module(scriptname)


def get_student_directories(root_directory):
    return [ f for f in os.listdir(root_directory) if not os.path.isfile(os.path.join(root_directory, f)) ]


def run_script_on_directories_with_config(script, directories, config):
    for directory in directories:
        script.process(directory, config)


if __name__ == '__main__':
    main()
