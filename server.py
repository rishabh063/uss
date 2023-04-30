from flask import Flask, render_template, request , Response , send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from facial_position_detection import * 
import time
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class DocumentEntry(db.Model):
    id = db.Column(db.Text, primary_key=True)
    econtent = db.Column(db.Text, nullable=False)
    contentType = db.Column(db.String(120),  nullable=False)
    photoID = db.Column(db.String(120),  nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
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
    # Get the uploaded file
    file = request.files['file']
    doc=request.files['file2']
    file_content = doc.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')
    if file.filename == '':
        return 'No file selected'

    # Get the emailID, date of birth, and content type from the form
    emailID = request.form.get('emailID')
    contentType = doc.filename.split('.')[-1]
    print(contentType)
    if contentType!='webp' and contentType!='png' and contentType!='jpeg' and contentType!='jpg':
        return 'Only Images are allowed'
    filename='images/'+emailID+'img.'+file.filename.split('.')[-1]
    file.save(filename)
    time.sleep(0.1)
    if not checkFace(filename):
        return 'No Face Found'
    try:
        data = DocumentEntry(id=emailID , econtent=base64_content, contentType=contentType  , photoID=filename)
        db.session.add(data)
        db.session.commit()
    except:
        return 'Email already Filled'
    return 'added to the database'
@app.route('/collect', methods=['POST'])
def collect():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']

    if file.filename == '':
        return 'No file selected'
    
    emailID = request.form.get('emailID')
    users = DocumentEntry.query.filter_by(id=emailID).all()
    # Print each user's name and email
    try:
        baseFile=users[0].photoID
    except:
        return 'Email Not Found'
    filename='videos/'+emailID+'temp.'+file.filename.split('.')[-1]
    file.save(filename)
    time.sleep(0.1)
    try:
        output=run(filename ,[[0,0,1,1]], baseFile )
    except:
        return "Video doesnt Match"
    print(output)
    if output:
        decoded_bytes = base64.b64decode(users[0].econtent)
        # Create a Flask Response object with the decoded bytes as the content
        img_buffer = BytesIO(decoded_bytes)
        print(users[0].contentType.split('.')[-1])
    # Return the image file using Flask's send_file function
        return send_file(img_buffer, mimetype='image/'+users[0].contentType.split('.')[-1])


    return 'Face mismatch'
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080)
