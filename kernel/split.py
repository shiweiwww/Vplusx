#coding:utf-8
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
# del temp files
def del_temp_files(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            try:
                os.remove(c_path)
            except:
                print(c_path)
def split_pdf(infn):
    # clear tempfile
    del_temp_files("temp")

    # split pdf by pages
    pdf_input = PdfFileReader(open(infn, 'rb'))
    page_count = pdf_input.getNumPages()
    print("xxxxxx",page_count)
    # read first-5th as the index
    pdf_output = PdfFileWriter()
    for i in range(0, 5):
        pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open("temp/%s"%0 + "_result.pdf", "wb"))
    print('finishindex')    
    # split pdf by page
    for i in range(5, page_count):
        pdf_output = PdfFileWriter()
        pdf_output.addPage(pdf_input.getPage(i))
        pdf_output.write(open("temp/%s"%i + "_result.pdf", "wb"))


if __name__ == '__main__':
    pdf_path = 'resource/ccc.pdf'
    split_pdf(pdf_path)