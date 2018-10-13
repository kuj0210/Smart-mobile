#-*-coding: utf-8-*-
from flask import Flask,request,jsonify,send_from_directory, redirect,url_for,render_template
from flask_sslify import SSLify
from serverManageMent import NaverManager 
import compareSentence
from konlpy.corpus import kolaw
import jpype
from Register import *
import os
from datetime import datetime
import time
from memo import Memory
THusecaseFinder =compareSentence.UsecaseFinder()
UPLOAD_FOLDER = 'uploaded'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sslfy =SSLify(app, permanent=True)
Memo = Memory()

@app.route("/",methods=["POST"])
def naver_Servermain():
    # make manager
    Manager =NaverManager()
    # get data from naver  talk talk
    dataFromMessenger =request.get_json()# get json data from naver talk talk
    infomationFromNaverTalk=Manager.getDataFromNaverTalk(dataFromMessenger) # it is process for data sorting
    user =infomationFromNaverTalk["user"]
    postBodyMessage = Manager.eventHandler(infomationFromNaverTalk) # process event
    if postBodyMessage == "ECHO":
      return
    return jsonify(postBodyMessage), 200

@app.route("/bootUp",methods=["POST"])
def bootUpMobile():
    # make manager
    reg = Register()
    dataFromMessenger =request.get_json()# get json data from naver talk talk
    SR=dataFromMessenger['textContent']['text']
    reg.openDB()
    UK=reg.getUserFromSerial(SR)
    reg.closeDB()
    return UK 

@app.route("/RQST",methods=["POST"])
def passRequest():
    reg = Register()
    dataFromMessenger =request.get_json()# ge/home/test"t json data from naver talk talk
    SR=dataFromMessenger['textContent']['text']
    rq=reg.fetchRequest(SR)
    if rq == False:
        return "NO"
    return rq
 
@app.route("/push",methods=["POST"])
def pushResult():
    nM=NaverManager()
    dataFromMessenger =request.get_json()# get json data from naver talk talk
    user =msg=dataFromMessenger['user']
    msg=dataFromMessenger['textContent']['text']
    nM.sendPush(nM.PUSH_URL,user,msg)
    
    
    return "True"


@app.route("/<user>/image", methods=["POST", 'GET'])
def image(user):
    nM = NaverManager()
    file = request.files['file']  # 파일받기
    filename = file.filename  # 이름얻기
    SR = filename.split(".")[0]  # 시리얼번호 추출
    now = datetime.now()  # 시간얻기
    f = filename.split(".")  # 파싱
    sndF = f[0] + '_%s-%s-%s-%s-%s-%s.' % (now.year, now.month, now.day, now.hour, now.minute, now.second) + f[1]
        # 파일이름 완성

        # 이전에 저장한것 삭제
    res = Memo.dememorization(f[0])
    if res != False:
        os.remove(res)

    # 파일저장
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], sndF))
    nM.sendIMAG(user, nM.IMAGE_URL + sndF)
    # 방금 저장한 파일 기억
    Memo.memorization(f[0], os.path.join(app.config['UPLOAD_FOLDER'], sndF))
    return "TRUE"


@app.route('/download/<filename>', methods=['GET'])
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

@app.route('/sign_up/<temp_user_key>', methods=['GET', 'POST'])
def sign_up(temp_user_key):
    if request.method == 'GET':
        return render_template('regist.html')

    else:
        #get data from form
        serial = request.form['serial']
        email = request.form['email']
        location = request.form['location']
        reg = Register() 
        #get user key from temp id
        userKey = reg.getUserKeyByTempID(temp_user_key)
        #regist user
        reg.insertUserData(userKey, serial, email, location)
        #delete temp information
        reg.deleteTempID(temp_user_key)
        # push mobile to notify update user
        reg.insertUserRequest(userKey,"UPDATE")
        return render_template("regist_success.html"), 200


if __name__ == "__main__":
	#일반
	ssl_cert = '/etc/letsencrypt/live/kitiot.tk/fullchain.pem'
	ssl_key =  '/etc/letsencrypt/live/kitiot.tk/privkey.pem'
	contextSSL =  (ssl_cert, ssl_key)
	   #user ="u9-NF6yuZ8H8TAgj1uzqnQ"
	app.run(host='0.0.0.0', port=443, debug = True, ssl_context = contextSSL)
