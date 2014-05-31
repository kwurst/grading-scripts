import argparse
import os
from assignment import Assignment
from command import Command


class LabConvert(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('config', help='JSON configuration file')
        parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
        args = parser.parse_args()
        Command.set_default_verbosity(args.verbose)
        self._a2pdf = Command('a2pdf --noperl-syntax --noline-numbers "{ins}" -o "{ins}.pdf"')
        self._pdfcat = Command('pdftk "{ins}" cat output "{outs}"')
        self._create_log = Command('git log > log.txt')
        self._rm = Command('rm "{ins}"')
        Assignment(args.config).accept(self.go, cd=True)


    def go(self, directory, files):
        self._create_log()
        self._a2pdf.each(files + ['log.txt'])
        outpdf = directory.name + '.pdf'
        pdfs = [str(f) + '.pdf' for f in files] + [directory/'log.txt.pdf']
        self._pdfcat(pdfs, outpdf)
        self._rm(pdfs)
        self._rm(directory/'log.txt')


if __name__ == '__main__':
    LabConvert()
