from docx import Document
import re

def txt_to_docx(fileIn, fileOut):
    document = Document()

    myfile = open(fileIn).read()
    myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile) # remove all non-XML-compatible characters

    document.add_paragraph(myfile)
    document.save(f"{fileOut}.docx")


