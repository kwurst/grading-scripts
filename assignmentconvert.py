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

import argparse
import logging
import os
from grade.engine import Assignment, Command


class LabConvert(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('config', help='JSON configuration file')
        parser.add_argument(
            '-v', '--verbose',
            help='increase output verbosity',
            action='store_true',
            default=False
            )
        parser.add_argument(
            '-b', '--brief',
            help='decrease output verbosity',
            action='store_true',
            default=False
            )
        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(level='DEBUG')
        elif args.brief:
            logging.basicConfig(level='WARNING')
        else:
            logging.basicConfig(level='INFO')
        self._a2pdf = Command(
            'a2pdf --noperl-syntax --noline-numbers "{ins}" -o "{ins}.pdf"')
        self._pdfcat = Command('pdftk "{ins}" cat output "{outs}"')
        self._create_log = Command('git log > log.txt')
        self._rm = Command('rm "{ins}"')
        Assignment(args.config).accept(self.process_submission)

    def process_submission(self, directory, files):
        self._create_log()
        self._a2pdf.each(files + ['log.txt'])
        outpdf = directory.name + '.pdf'
        pdfs = [str(f) + '.pdf' for f in files] + [directory/'log.txt.pdf']
        self._pdfcat(pdfs, outpdf)
        self._rm(pdfs)
        self._rm(directory/'log.txt')


if __name__ == '__main__':
    LabConvert()
