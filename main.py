from flask import Flask,render_template,request,url_for
import predictions
import pdf_settings
import settings
from docx import Document
import utils
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter
import docx2txt
app = Flask(__name__)
app.secret_key = 'Resume Parsing App'
import os
a = []
@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        file = request.files['file_name']
        filename = file.filename
        upload_image_path = utils.save_upload_image(file)
        #print('file saved in = ',upload_image_path)
        if filename.endswith('.pdf'):
            path = pdf_settings.join_path(pdf_settings.MEDIA_DIR,'filename.pdf')
            complete_text = ''
            with fitz.open(path) as doc:
                for page in doc:
                    complete_text += page.get_text()
            l, number, emails, years, name, found_skills = predictions.get_predictions(complete_text)
            result = {"Name ": name, 'Resume Category': l, "Mobile Number ": number, "Email: ": emails,
                      'Total years of Experience': years, 'Skills': found_skills}
            return render_template('predictions.html', results=result)
        elif filename.endswith('.docx'):
            path = settings.join_path(settings.MEDIA_DIR, 'filename.docx')
            resume = path
            resume_text = Document(resume)
            complete_text = ''
            for p in resume_text.paragraphs:
                complete_text += p.text
            l, number, emails, years, name, found_skills = predictions.get_predictions(complete_text)
            result = {"Name ":name,'Resume Category' :l,"Mobile Number ":number,"Email: ":emails,'Total years of Experience' :years,'Skills':found_skills}
            return render_template('predictions.html', results = result)


        return render_template('scanner.html')
    return render_template('scanner.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

