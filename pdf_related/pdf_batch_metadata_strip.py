#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from os import path
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileWriter

# Replace with your the folder containing the "to-be-sanitized" pdfs
TARGET_FOLDER = ""
# The filename postfix for the sanitized pdfs
SANITIZED_POSTFIX = "-sanitized"


def find_ext(dr, ext):
    # For Python 3.7+ : return glob(path.join(dr, f"*.{ext}")
    return glob(path.join(dr, "*.{}".format(ext)))


def deleteMetadata(doc_address):
    output_path = os.path.splitext(doc_address)[0] + SANITIZED_POSTFIX + ".pdf"

    # There is no interface through pyPDF with which to set this other then getting
    # your hands dirty like so:
    with open(doc_address, 'rb') as input:
        reader = PdfFileReader(input)

        writer = PdfFileWriter()

        writer.appendPagesFromReader(reader)

        # Write/Delete your metadata here:
        writer.addMetadata({
            '/Author': ''
        })

        fout = open(output_path, 'wb')
        writer.write(fout)

        fout.close()
    return 1


def main():
    for file_path in find_ext(TARGET_FOLDER, "pdf"):
        deleteMetadata(file_path)


if __name__ == '__main__':
    main()