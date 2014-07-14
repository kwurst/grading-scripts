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
from submissions import SubmissionProcessor


class LabConvert(SubmissionProcessor):
    def __init__(self):
        super().__init__(self)
        self._a2pdf = self.command(
            'a2pdf --noperl-syntax --noline-numbers {ins} -o {ins}.pdf')
        self._pdfcat = self.command('pdftk {ins} cat output {outs}')
        self._create_log = self.command('git log > log.txt')
        self._rm = self.command('rm {ins}')

    def process_submission(self, directory, files):
        self._create_log()
        self._a2pdf.each(files + ['log.txt'])
        outpdf = directory.name + '.pdf'
        pdfs = [str(f) + '.pdf' for f in files] + [directory/'log.txt.pdf']
        self._pdfcat(pdfs, outpdf)
        self._rm(pdfs)
        self._rm(directory/'log.txt')


if __name__ == '__main__':
    LabConvert().run()
