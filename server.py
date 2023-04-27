from flask import Flask, render_template, request, send_from_directory, send_file, redirect, url_for
import requests
import json
import os
from cryptography.fernet import Fernet



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
    # Get the uploaded file
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'

    # Get the passphrase, date of birth, and content type from the form
    passphrase = request.form.get('passphrase')
    dob = request.form.get('dob')
    content_type = request.form.get('contentType')

    # Encrypt the file using the passphrase
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(file.read())

    # Convert the encrypted data to a string
    encrypted_data_str = encrypted_data.decode('latin-1')

    # Save the encrypted file to disk
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    # Create a dictionary of metadata to send to the backend
    metadata = {
        'passphrase': passphrase,
        'dob': dob,
        'content_type': content_type,
        'key': key
    }

    # Send the metadata and encrypted file to the backend
    #data = {
     #   'metadata': metadata,
    #    'encrypted_data': encrypted_data_str
    #}
    #headers = {'Content-type': 'application/json'}
    #response = requests.post('http://localhost:8080/upload', data=json.dumps(data), headers=headers)


    return '''
    <script>
        alert('File uploaded successfully');
        window.location.href = '/';
    </script>
    '''

    # print(request.files)
    # if 'file' not in request.files:
    #     return 'No file uploaded'

    # file = request.files['file']
    # if file.filename == '':
    #     return 'No file selected'
    # passphrase = request.form.get('passphrase')
    # print(passphrase)
    # content = request.form.get('encryptedContent')
    # print(content)
    # contentType = request.form.get('contentType')
    # print(contentType)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # return 'File uploaded successfully'

@app.route('/collect', methods=['POST'])
def collect():
    if 'file' not in request.files:
        return 'No file uploaded'

    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    
    passphrase = request.form.get('passphrase')
    key_file = request.files['key']
    print(passphrase)

    # Read the key from the key file
    key = key_file.read()

    # Decrypt the file using the key and passphrase
    f = Fernet(key)
    encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)

    # Save the decrypted file to disk
    filename = file.filename
    decrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return render_template('index.html', decrypted_file_path=decrypted_file_path, os=os)



if __name__ == '__main__':
    app.run(debug=True, port=8080)
