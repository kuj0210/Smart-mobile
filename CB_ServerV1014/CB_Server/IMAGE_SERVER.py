#-*-coding: utf-8-*-
from flask import Flask,request,jsonify,send_from_directory, redirect,url_for,render_template
from flask_sslify import SSLify
from serverManageMent import NaverManager 
import compareSentence
from konlpy.corpus import kolaw
import jpype
from Register import *
import os


UPLOAD_FOLDER = 'uploaded'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 
@app.route("/<user>/image",methods=["POST",'GET'])
def image(user):
    nM=NaverManager()
    file =request.files['file']
    print("파일받기완료")
    filename=file.filename
    print("이름추출")
    SR=filename.split(".")[0]
    print("SR추출")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    print("저장완료")
    print(nM.SERVER_URL +filename)
    nM.sendPush(nM.PUSH_URL,user,nM.IMAGE_URL +filename)
    print("업로드")
    return "TRUE"


@app.route('/download/<filename>', methods=['GET'])
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

if __name__ == "__main__":
   
    app.run(host='0.0.0.0', port=80, debug = True)
    
