from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from ai_code import *
from fpdf import FPDF
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('view_pdf', filename=filename))
    else:
        flash('Allowed file types are pdf')
        return redirect(request.url)

@app.route('/view/<filename>')
def view_pdf(filename):
    return render_template('view_pdf.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/query', methods=['POST'])
def query_pdf():
    filename = request.form['filename']
    query_text = request.form.get('query_text', '')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resp = filter_information(file_path, query_text)
    # query_result_filename = f"query_result_{filename}"
    query_result_filename = f"1_{filename}"
    query_result_path = os.path.join(app.config['UPLOAD_FOLDER'], query_result_filename)
    create_pdf(resp, query_result_path)
    return render_template('query_results.html', results=query_text, filename=query_result_filename)


@app.route('/visualize', methods=['POST'])
def visualize_query():
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'rb') as f:
        content = f.read()
    return render_template('visualize.html', content=content.decode('latin-1'), filename=filename)


if __name__ == '__main__':
    app.run(debug=True, port=3001)
