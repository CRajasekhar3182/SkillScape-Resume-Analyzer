import os
import settings
import pdf_settings
import numpy as np
from imutils.perspective import four_point_transform
import glob
from pdf2docx import converter,parse,Converter
from pdf2docx import parse
from docx import Document
import utils
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
import docx2txt

def save_upload_image(fileObj):
    filename = fileObj.filename
    if filename.endswith('.pdf'):
        filename = fileObj.filename
        extensions = ['docx', 'pdf']
        c = []
        d = []
        for i in extensions:
            if i in filename:
                d.append(i)
                c.append(filename.index(i))
        k = c[0]
        filename = filename[:k]
        save_filename = 'filename.' + d[0]
        upload_image_path = pdf_settings.join_path(pdf_settings.SAVE_DIR,
                                               save_filename)

        fileObj.save(upload_image_path)
        return upload_image_path
    elif filename.endswith('.docx'):
        extensions = ['docx','pdf']
        c = []
        d = []
        for i in extensions:
            if i in filename:
                d.append(i)
                c.append(filename.index(i))
        k = c[0]
        filename = filename[:k]
        save_filename = 'filename.' + d[0]
        upload_image_path = settings.join_path(settings.SAVE_DIR,
                                                   save_filename)

        fileObj.save(upload_image_path)
        return upload_image_path
    else:
        return "Only PDF and docx files are allowed"




