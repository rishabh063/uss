from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from facial_position_detection import * 
import time
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
    if file.filename == '':
        return 'No file selected'

    # Get the emailID, date of birth, and content type from the form
    emailID = request.form.get('emailID')
    content = request.form.get('encryptedContent')
    contentType = request.form.get('contentType')
    filename='images/'+emailID+'img.'+file.filename.split('.')[-1]
    file.save(filename)
    time.sleep(0.1)
    if not checkFace(filename):
        return 'No Face Found'
    data = DocumentEntry(id=emailID , econtent=content, contentType=contentType  , photoID=filename)
    db.session.add(data)
    db.session.commit()
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
    output=run(filename ,[[0,0,1,1]], baseFile )
    print(output)
    if output:
        return str(users[0].econtent)
    return 'Face mismatch'
if __name__ == '__main__':
    app.run(debug=True, port=8080)
