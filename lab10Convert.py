import argparse
import os
import assignment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='JSON configuration file')
    args = parser.parse_args()
    assignment.new(args.config).accept(go, cd=True)


def go(directory, files):
    for file_ in files:
        a2pdf(file_)
    os.system('git log > log.txt')
    a2pdf('log.txt')
    outpdf = str(directory.name) + '.pdf'
    os.system('pdftk *.pdf cat output ' + outpdf)
    for file_ in directory.glob('*.pdf'):
        if str(file_) != outpdf:
            os.remove(file_)
    os.remove('log.txt')


def a2pdf(file_):
    os.system('a2pdf --noperl-syntax --noline-numbers "%s" -o "%s"' %
            (str(file_.name), str(file_.name) + '.pdf'))


if __name__ == '__main__':
    main()
