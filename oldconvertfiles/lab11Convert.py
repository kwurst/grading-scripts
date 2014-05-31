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

# Get list of all directories
onlydirectories = [ f for f in os.listdir() if not os.path.isfile(os.path.join(os.curdir,f)) ]

# For each directory
for dir in onlydirectories:
    print(dir)
    os.chdir(dir)
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/Brass.java -o Brass.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/Instrument.java -o Instrument.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/Percussion.java -o Percussion.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/Stringed.java -o Stringed.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/Wind.java -o Wind.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part1/WoodWind.java -o WoodWind.java.pdf')

    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part2/ActionCharacter.java -o ActionCharacter.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part2/CanFight.java -o CanFight.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part2/CanFly.java -o CanFly.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part2/CanSwim.java -o CanSwim.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part2/Hero.java -o Hero.java.pdf')

    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/DangerousMonster.java -o DangerousMonster.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/Dracula.java -o Dracula.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/GodZilla.java -o GodZilla.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/HorrorShow.java -o HorrorShow.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/Lethal.java -o Lethal.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/Monster.java -o Monster.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part3/Vampire.java -o Vampire.java.pdf')

    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/AgeException.java -o AgeException.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/IllegalAgeFormatException.java -o IllegalAgeFormatException.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/NegativeAgeException.java -o NegativeAgeException.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/OutOfAgeLimitException.java -o OutOfAgeLimitException.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/TooOldException.java -o TooOldException.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Lab11Code/Part4/TooYoungException.java -o TooYoungException.java.pdf')

    os.system('git log > log.txt')
    os.system('a2pdf --noperl-syntax --noline-numbers log.txt -o log.txt.pdf')
    
    os.system('pdftk Instrument.java.pdf Stringed.java.pdf Wind.java.pdf Brass.java.pdf WoodWind.java.pdf Percussion.java.pdf CanFight.java.pdf CanSwim.java.pdf CanFly.java.pdf ActionCharacter.java.pdf Hero.java.pdf Monster.java.pdf DangerousMonster.java.pdf GodZilla.java.pdf Lethal.java.pdf Vampire.java.pdf Dracula.java.pdf HorrorShow.java.pdf AgeException.java.pdf IllegalAgeFormatException.java.pdf NegativeAgeException.java.pdf OutOfAgeLimitException.java.pdf TooYoungException.java.pdf TooOldException.java.pdf log.txt.pdf cat output ' + dir + '.pdf')

    os.remove('Brass.java.pdf')
    os.remove('Instrument.java.pdf')
    os.remove('Percussion.java.pdf')
    os.remove('Stringed.java.pdf')
    os.remove('Wind.java.pdf')
    os.remove('WoodWind.java.pdf')

    os.remove('ActionCharacter.java.pdf')
    os.remove('CanFight.java.pdf')
    os.remove('CanFly.java.pdf')
    os.remove('CanSwim.java.pdf')
    os.remove('Hero.java.pdf')

    os.remove('DangerousMonster.java.pdf')
    os.remove('Dracula.java.pdf')
    os.remove('GodZilla.java.pdf')
    os.remove('HorrorShow.java.pdf')
    os.remove('Lethal.java.pdf')
    os.remove('Monster.java.pdf')
    os.remove('Vampire.java.pdf')

    os.remove('AgeException.java.pdf')
    os.remove('IllegalAgeFormatException.java.pdf')
    os.remove('NegativeAgeException.java.pdf')
    os.remove('OutOfAgeLimitException.java.pdf')
    os.remove('TooOldException.java.pdf')
    os.remove('TooYoungException.java.pdf')

    os.remove('log.txt.pdf')
    os.remove('log.txt')
    os.chdir('..')











































