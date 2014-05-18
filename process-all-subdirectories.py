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

# Set up to parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('directory', help='Directory to process all subdirectories')
parser.add_argument('script', help='Processing script')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
args = parser.parse_args()

mod = __import__(args.script)

# Change to assignment directory
os.chdir(args.directory) # directory for assignment

# Get list of all directories
onlydirectories = [ f for f in os.listdir() if not os.path.isfile(os.path.join(os.curdir,f)) ]

# For each directory
for dir in onlydirectories:
    os.chdir(dir)
    
    mod.process(dir)
    
    os.chdir('..')











































