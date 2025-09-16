import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger


def pdf_cat(pdfs, output_stream="output.pdf"):
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(output_stream)
    merger.close()


def pdf_dup(pdfile, output_stream=None, nb=2):
    if not output_stream:
        output_stream = pdfile
    merger = PdfMerger()
    for _ in range(nb):
        merger.append(f"{pdfile}.pdf")
    merger.write(f"{output_stream}.pdf")
    merger.close()


def split_pdf(i_name, o_name, nb=0):
    inputpdf = PdfFileReader(open(i_name, "rb"))
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(nb))
    with open(o_name, "wb") as outputStream:
        output.write(outputStream)


os.chdir("/home/mohamed/Downloads")
files = [f for f in sorted(os.listdir()) if f.endswith("pdf")]

pdf_cat(files)
