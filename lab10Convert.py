import argparse
import os
import assignment
from command import Command


a2pdf = Command('a2pdf --noperl-syntax --noline-numbers "{ins}" -o "{ins}.pdf"')
pdfcat = Command('pdftk "{ins}" cat output "{outs}"')
create_log = Command('git log > log.txt')
rm = Command('rm "{ins}"')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='JSON configuration file')
    args = parser.parse_args()
    assignment.new(args.config).accept(go, cd=True)


def go(directory, files):
    create_log()
    a2pdf.each(files + ['log.txt'])
    outpdf = directory.name + '.pdf'
    pdfcat(directory.glob('*.pdf'), outpdf)
    rm([f for f in directory.glob('*.pdf') if str(f) != outpdf])
    rm('log.txt')


if __name__ == '__main__':
    main()
