'''
Copyright (c) IoT-Pet-Home-system team : Woo-jin Kim, Keon-hee Lee, Dae-seok Ko
LICENSE : GPL v3 LICENSE

- Description : https://github.com/kuj0210/IoT-Pet-Home-System
- If you want to contact us, please send mail "beta1360@naver.com"

* Server.py
  - Core Modules That Work with Server.
  - Perform the role of the main server by running this module
'''

#-*-coding: utf-8-*-

from flask import Flask,request,jsonify,send_from_directory
from serverManageMent import NaverManager 
import compareSentence
from konlpy.corpus import kolaw
import jpype

'''
 Content with the verb or noun : 50
 It must content with noun : 60
 All content with verb and noun: 100
'''


THusecaseFinder =compareSentence.UsecaseFinder()
UPLOAD_FOLDER = 'uploaded'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#@app.route("/",methods=["POST"])
#def naver_ServerManager():
#    '''
#    - Related Naver-talk-talk Platform
#    - This function manage the related Naver-talk-talk API 
#      and reply to Naver-talk-talk API server.  
#    '''
#    data = request.get_json()
#    return jsonify(naverMessage.manageEvent(data=data, usecase=usecase)),200


@app.route("/",methods=["POST"])
def naver_Servermain():

    '''
    - Related Naver-talk-talk Platform
    - This function manage the related Naver-talk-talk API 
      and reply to Naver-talk-talk API server. 
 
    '''
    # make manager
    Manager =NaverManager()
    # get data from naver  talk talk
    dataFromMessenger =request.get_json()# get json data from naver talk talk
    infomationFromNaverTalk=Manager.getDataFromNaverTalk(dataFromMessenger) # it is process for data sorting
    user =infomationFromNaverTalk["user"]

    #
    postBodyMessage = Manager.eventHandler(infomationFromNaverTalk) # process event
    if postBodyMessage == "ECHO":
      return
    
    print("Manager_LOG %s\n\n"%postBodyMessage)
            

    return jsonify(postBodyMessage), 200

 
if __name__ == "__main__":
    '''
    It's the main part. After you set up the SSL certificate path, 
    attach it to the flask framework and launch the Web server.
    '''
    ssl_cert = '/etc/letsencrypt/live/www.kit-iot-system.tk/fullchain.pem'
    ssl_key =  '/etc/letsencrypt/live/www.kit-iot-system.tk/privkey.pem'
    contextSSL =  (ssl_cert, ssl_key)
    app.run(host='0.0.0.0', port=443, debug = True, ssl_context = contextSSL)

