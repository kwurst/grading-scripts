import argparse
import os
from assignment import Assignment
from command import Command


a2pdf = Command('a2pdf --noperl-syntax --noline-numbers "{ins}" -o "{ins}.pdf"')
pdfcat = Command('pdftk "{ins}" cat output "{outs}"')
create_log = Command('git log > log.txt')
rm = Command('rm "{ins}"')

        Assignment(args.config, args.verbose).accept(self.go, cd=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='JSON configuration file')
    args = parser.parse_args()
    assignment.new(args.config).accept(go, cd=True)


def go(directory, files):
    create_log()
    print('done creating log')
    a2pdf.each(files + ['log.txt'])
    print('done pdfing')
    outpdf = directory.name + '.pdf'
    print('generated file name')
    pdfs = [str(f) + '.pdf' for f in files] + [directory/'log.txt.pdf']
    pdfcat(pdfs, outpdf)
    print('done concatentating')
    rm(pdfs)
    rm(directory/'log.txt')


if __name__ == '__main__':
    main()
