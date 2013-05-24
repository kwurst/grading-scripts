#!/bin/bash

# This script returns a graded student assignment to their repository.
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

git add $1.pdf # add the graded assignment
git commit -m"Returned $2" # commit the graded assignment
git push ${1%%-*} $1 # push the changes to student repository

git checkout master # return to the master branch






















































