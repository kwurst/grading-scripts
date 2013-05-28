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
# It also copies the solution to their repository.
# It will leave the graded assignment in a new branch.
# The student will have to merge the changes into their master branch
# (or you have to issue a pull request, and maybe merge it depending on
# how much you want to do for the students.)

# The script takes two parameters

# Parameter 1 is the concatenation of all of the Bitbucket accounts of the students in the team, 
# separated by a dashes e.g. jsmith1-mjones
# It expects that the first username is the owner of the shared repository.

# Parameter 2 is name of the assignment e.g. Lab1

cd $2 # folder for local repository

git checkout $1 # checkout the student branch

cp ../grading/$2/$1.pdf ./ # copy the graded assignment to student repository
cp -r ../../../Labs/$2/$2'Solution' ./$2'Solution' # copy the solution to student repository

git add $1.pdf # add the graded assignment
git add $2'Solution' # add the solution

git commit -m"Returned graded $2 (and solution)" # commit the graded assignment
git push ${1%%-*} $1 # push the changes to student repository

git checkout master # return to the master branch






















































