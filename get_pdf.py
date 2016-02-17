import pyPdf
import subprocess as sp
import shlex
import sys
import os


def get_urls(file_path):
    """
    Extract URL's a PDF file

    http://stackoverflow.com/a/28425572/1780891
    """
    PDFFile = open(file_path, 'rb')

    PDF = pyPdf.PdfFileReader(PDFFile)
    pages = PDF.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    urls = []

    for page in range(pages):
        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()

        if pageObject.has_key(key):
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if u[ank].has_key(uri):
                    urls.append(u[ank][uri])

    return urls


def download_pdfs(urls):
    for url in urls:
        cmd = "wget '%s'" % (url)
        try:
            sp.call(shlex.split(cmd))
        except ValueError:
            pass


def print_format(path):
    files = [x for x in os.listdir(path) if x.endswith('.pdf')]
    for pdffile in files:
        name = pdffile.replace('.pdf', '').replace('_', ' ')
        print("\subsubsection{%s}\n\includepdf[pages=-]{%s%s}\n"%(name,path,pdffile))


def fix_file_names(path):
    # This for the counter comments files which originally had a number
    # like 201601180330014016775 prepended to each file name
    file_names = os.listdir(path)
    for f_name in file_names:
        if f_name.endswith(".pdf"):
            new_name = f_name[21:]
            cmd = "mv %s %s" % (f_name, new_name)
            sp.call(shlex.split(cmd))


if __name__ == "__main__":
    file_name = sys.argv[1]
    download_pdfs(get_urls(file_name))
