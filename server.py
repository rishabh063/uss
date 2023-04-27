from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/uploadPage')
def uploadPage():
    return render_template('index.html')
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
    file.save(file.filename)
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
    app.run()
