from docx import Document
import re

def txt_to_docx(fileIn, fileOut):
    document = Document()

    myfile = open(fileIn).read()
    myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile) # remove all non-XML-compatible characters

    document.add_paragraph(myfile)
    document.save(f"{fileOut}.docx")


def docx_to_txt(fileIn, fileOut):

    file_out = open(fileOut, "w")
    file_out.write(Document(fileIn).paragraphs[0].text)
    file_out.close()

