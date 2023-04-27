from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadPage')
def uploadPage():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/showdoc')
def showDoc():
    return render_template('index.html')  
  
@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    if 'file' not in request.files:
        return 'No file uploaded'

    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    passphrase = request.form.get('passphrase')
    print(passphrase)
    content = request.form.get('encryptedContent')
    print(content)
    contentType = request.form.get('contentType')
    print(contentType)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully'

@app.route('/collect', methods=['POST'])
def collect():
    if 'file' not in request.files:
        return 'No file uploaded'

    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    passphrase = request.form.get('passphrase')
    print(passphrase)
    return 'File uploaded successfully'
if __name__ == '__main__':
    app.run(debug=True, port=8080)
