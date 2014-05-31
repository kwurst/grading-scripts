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

import os

def process(dir):
    print(dir)

    os.system('a2pdf --noperl-syntax --noline-numbers Project1Code/Product.java -o Product.java.pdf')
    os.system('a2pdf --noperl-syntax --noline-numbers Project1Code/UserInterface.java -o UserInterface.java.pdf')
    os.system('git log | a2pdf --noperl-syntax --noline-numbers --title "git log" -o log.pdf')

    os.system('pdftk Product.java.pdf UserInterface.java.pdf log.pdf cat output ' + dir + '.pdf')

    os.remove('Product.java.pdf')
    os.remove('UserInterface.java.pdf')
    os.remove('log.pdf')












































