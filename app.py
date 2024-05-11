from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from rembg import remove

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the existence of the UPLOAD_FOLDER directory
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        remove_background(filepath)
        return redirect(url_for('result', filename=filename))

def remove_background(filepath):
    output_path = filepath + '_no_bg.png'
    with open(filepath, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            f_out.write(remove(f_in.read()))
    return output_path

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename + '_no_bg.png')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
