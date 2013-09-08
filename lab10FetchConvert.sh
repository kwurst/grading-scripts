#!/bin/bash

# Copyright (C) 2013 Karl R. Wurst
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
# Use the Lab2Return.sh script to return the graded PDF to the students.

# The script takes a single parameter, which is the concatenation of all
# of the Bitbucket accounts of the students in the team, separated by a dashes.
# e.g. jsmith1-mjones
# It expects that the first username is the owner of the shared repository.

cd Lab10 # folder for local repository

git remote add ${1%%-*} git@bitbucket.org:${1%%-*}/lab10.git # add a remote for the student repository
git fetch ${1%%-*} # fetch the student work
git checkout -b $1 ${1%%-*}/master # make a student branch

# Convert file(s) to PDF(s) and place in grading directory
a2pdf --noperl-syntax Lab10Code/Part1/Brass.java > ../grading/Lab10/$1Brass.pdf
a2pdf --noperl-syntax Lab10Code/Part1/Instrument.java > ../grading/Lab10/$1Instrument.pdf
a2pdf --noperl-syntax Lab10Code/Part1/Percussion.java > ../grading/Lab10/$1Percussion.pdf
a2pdf --noperl-syntax Lab10Code/Part1/Stringed.java > ../grading/Lab10/$1Stringed.pdf
a2pdf --noperl-syntax Lab10Code/Part1/Wind.java > ../grading/Lab10/$1Wind.pdf
a2pdf --noperl-syntax Lab10Code/Part1/WoodWind.java > ../grading/Lab10/$1WoodWind.pdf

a2pdf --noperl-syntax Lab10Code/Part2/ActionCharacter.java > ../grading/Lab10/$1ActionCharacter.pdf
a2pdf --noperl-syntax Lab10Code/Part2/CanFight.java > ../grading/Lab10/$1CanFight.pdf
a2pdf --noperl-syntax Lab10Code/Part2/CanFly.java > ../grading/Lab10/$1CanFly.pdf
a2pdf --noperl-syntax Lab10Code/Part2/CanSwim.java > ../grading/Lab10/$1CanSwim.pdf
a2pdf --noperl-syntax Lab10Code/Part2/Hero.java > ../grading/Lab10/$1Hero.pdf

a2pdf --noperl-syntax Lab10Code/Part3/DangerousMonster.java > ../grading/Lab10/$1DangerousMonster.pdf
a2pdf --noperl-syntax Lab10Code/Part3/Dracula.java > ../grading/Lab10/$1Dracula.pdf
a2pdf --noperl-syntax Lab10Code/Part3/GodZilla.java > ../grading/Lab10/$1GodZilla.pdf
a2pdf --noperl-syntax Lab10Code/Part3/Lethal.java > ../grading/Lab10/$1Lethal.pdf
a2pdf --noperl-syntax Lab10Code/Part3/Monster.java > ../grading/Lab10/$1Monster.pdf
a2pdf --noperl-syntax Lab10Code/Part3/Vampire.java > ../grading/Lab10/$1Vampire.pdf

pdftk ../grading/Lab10/$1Instrument.pdf ../grading/Lab10/$1Stringed.pdf ../grading/Lab10/$1Percussion.pdf ../grading/Lab10/$1Wind.pdf ../grading/Lab10/$1Brass.pdf ../grading/Lab10/$1WoodWind.pdf ../grading/Lab10/$1ActionCharacter.pdf ../grading/Lab10/$1CanFight.pdf ../grading/Lab10/$1CanSwim.pdf ../grading/Lab10/$1CanFly.pdf ../grading/Lab10/$1Hero.pdf ../grading/Lab10/$1Monster.pdf ../grading/Lab10/$1DangerousMonster.pdf ../grading/Lab10/$1Lethal.pdf ../grading/Lab10/$1Vampire.pdf ../grading/Lab10/$1GodZilla.pdf ../grading/Lab10/$1Dracula.pdf cat output ../grading/Lab10/$1.pdf

rm ../grading/Lab10/$1Brass.pdf
rm ../grading/Lab10/$1Instrument.pdf
rm ../grading/Lab10/$1Percussion.pdf
rm ../grading/Lab10/$1Stringed.pdf
rm ../grading/Lab10/$1Wind.pdf
rm ../grading/Lab10/$1WoodWind.pdf

rm ../grading/Lab10/$1ActionCharacter.pdf
rm ../grading/Lab10/$1CanFight.pdf
rm ../grading/Lab10/$1CanFly.pdf
rm ../grading/Lab10/$1CanSwim.pdf
rm ../grading/Lab10/$1Hero.pdf

rm ../grading/Lab10/$1DangerousMonster.pdf
rm ../grading/Lab10/$1Dracula.pdf
rm ../grading/Lab10/$1Godzilla.pdf
rm ../grading/Lab10/$1Lethal.pdf
rm ../grading/Lab10/$1Monster.pdf
rm ../grading/Lab10/$1Vampire.pdf

git checkout master # return to master branch





















































