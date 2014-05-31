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

# This script returns a graded student assignment to their repository.
# It will leave the graded assignment in a new branch.
# The student will have to merge the changes into their master branch
# (or you have to issue a pull request, and maybe merge it depending on
# how much you want to do for the students.)

# This script will fetch a student assignment from Bitbucket for grading.
# The files are converted to a single PDF and put into the grading folder.
# Use the Lab1Return.sh script to return the graded PDF to the students.

# The script takes a single parameter, which is the concatenation of all
# of the Bitbucket accounts of the students in the team, separated by a dashes.
# e.g. jsmith1-mjones
# It expects that the first username is the owner of the shared repository.

import argparse
import sys
import os
import subprocess

# Set up to parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('directory', help='Assignment directory')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
args = parser.parse_args()

PIPE = subprocess.PIPE

# Change to assignment directory
os.chdir(args.directory) # directory for assignment

os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Shape.java -o Shape.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/ThreeDimensionalShape.java -o ThreeDimensionalShape.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/TwoDimensionalShape.java -o TwoDImensionalShape.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Cone.java -o Cone.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Sphere.java -o Sphere.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Cube.java -o Cube.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Cylinder.java -o Cylinder.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Triangle.java -o Triangle.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Rectangle.java -o Rectangle.java.pdf')
os.system('a2pdf --noperl-syntax --noline-numbers Project4Code/Circle.java -o Circle.java.pdf')

os.system('git log | a2pdf --noperl-syntax --noline-numbers --title "git log" -o log.pdf')
os.system('pdftk Shape.java.pdf ThreeDimensionalShape.java.pdf Cone.java.pdf Sphere.java.pdf Cube.java.pdf Cylinder.java.pdf TwoDimensionalShape.java.pdf Triangle.java.pdf Rectangle.java.pdf Circle.java.pdf log.pdf cat output cyates2.pdf')
os.remove('Shape.java.pdf')
os.remove('ThreeDimensionalShape.java.pdf')
os.remove('TwoDimensionalShape.java.pdf')
os.remove('Cone.java.pdf')
os.remove('Sphere.java.pdf')
os.remove('Cube.java.pdf')
os.remove('Cylinder.java.pdf')
os.remove('Triangle.java.pdf')
os.remove('Rectangle.java.pdf')
os.remove('Circle.java.pdf')

os.remove('log.pdf')











































