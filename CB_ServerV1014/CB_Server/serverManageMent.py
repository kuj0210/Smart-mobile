from flask import request
import defaultMessage
import compareSentence
from Register import Register
from flask import request
import requests
import json
from IDissuance import *

class NaverManager:
    def __init__(self):
        self.mMsgList =defaultMessage.MessageList()
        self.mRegister = Register()
        self.PUSH_URL = "https://gw.talk.naver.com/chatbot/v1/event"
        self.UPDATE_URL = "https://gw.talk.naver.com/chatbot/v1/imageUpload HTTP/1.1"
        self.SERVER_URL = 'https://kitiot.tk:443/'
        self.IMAGE_URL = self.SERVER_URL+'download/'
        self.SIGN_UP_URL =  self.SERVER_URL+'sign_up/'
    
    def getOnlyImageBox(self,user,url):
        imag ={
            "event": "send",
            "user": user,   
            "imageContent":
            {
                "imageUrl": url
            }
        }
        return imag

    def getImageBox(self,user,url):
        imag={
            "event": "send",
            "user": user,
            
            "compositeContent": {
                "compositeList":[{
                        "title": "모빌사진",
                        "description": "요청하신 사진입니다",
                        "image": {
                            "imageUrl": url
                        }
                }]
            }
        }

        return imag
    def getUpdateBox(self,url):
        return {"imageUrl": url}
    def getPostBodyMessage(self,user,text):
        postBodyMessage = {
            "event": "send",
            "user" : user,
            "textContent": {
                "text": text
            },
            "options": {
                "notification": "true" 
            }
        }
        return postBodyMessage

    def getPostPushMessage(self,user,text):
        postBodyMessage = {
            "event": "send",
            "user" : user,
            "textContent": {
                "text": text
            }
        }
        return postBodyMessage

    def ImageJson(self,user,URL):
        postBodyMessage = {
            "event": "send",
            "user" : user,
            "imageUrl": URL
        }
        return postBodyMessage

    def sendPush(self,URL,user,msg):
        header = {"Content-Type": "application/json;charset=UTF-8","Authorization": "kaQdS4oaQjKux6wN7QJJ" }
        res = requests.post(url=URL, headers=header, data=json.dumps(self.getPostPushMessage(user,msg)))
    
    def upLoad(self,url):
        header = {"Content-Type": "application/json;charset=UTF-8","Authorization": "kaQdS4oaQjKux6wN7QJJ" }
        res = requests.post(url=self.UPDATE_URL, headers=header, data=json.dumps(self.getUpdateBox(url)))
    def sendIMAG(self,user,URL):
        print(self.getOnlyImageBox(user,URL))
        header = {"Content-Type": "application/json;charset=UTF-8","Authorization": "kaQdS4oaQjKux6wN7QJJ" }
        res = requests.post(url= self.PUSH_URL, headers=header, data=json.dumps(self.getOnlyImageBox(user,URL)))
    # 2차원 데이터를 1차원으로 변경
    def getDataFromNaverTalk(self,dataFromMessenger):
        dicForSaveUserData ={}
        user = dataFromMessenger["user"]
        event = dataFromMessenger["event"] 
        dicForSaveUserData ={"user":user,"event":event}

        if event !="friend":
            if "textContent" in dataFromMessenger:
                dicForSaveUserData["typing"] = dataFromMessenger["textContent"]["inputType"]
            else:
                dicForSaveUserData["typing"] ="None"
                
            if  dicForSaveUserData["typing"]=="typing":
                 dicForSaveUserData["message"] = dataFromMessenger["textContent"]["text"]   

        if "options" in dataFromMessenger and "set" in dataFromMessenger["options"]:
             dicForSaveUserData["state"]=dataFromMessenger["options"]["set"]
            
        return dicForSaveUserData


    #이벤트 처리 데이터
    def eventHandler(self,infomationFromNaverTalk):
        sendMSG = "None"
        msgList =self.mMsgList
        user =infomationFromNaverTalk["user"]
        if infomationFromNaverTalk["event"] == "open":
            sendMSG = msgList.getOpenMsg()
    
        elif infomationFromNaverTalk["event"] == "leave":
            sendMSG =msgList.getLeavMsg()

        elif infomationFromNaverTalk["event"]=="friend":
            if infomationFromNaverTalk["state"]=="on":
                sendMSG = msgList.getFriendOn()
            else:
                self.mRegister.insertUserRequest(user,"UPDATE")
                sendMSG = msgList.getFriendOff() +"\n"+ self.mRegister.deleteUserData(user)
                

        elif infomationFromNaverTalk["event"]=="echo":
            return "Echo"
 
         
        elif infomationFromNaverTalk["event"] == "send" and infomationFromNaverTalk["typing"]=="typing":   
            sendMSG =self.handlerForSendEvent(user,infomationFromNaverTalk["message"])
        else:
            sendMSG =msgList.getmessageTypeError()
        
        postBodyMessage = self.getPostBodyMessage( user,sendMSG) 
        return postBodyMessage
         
    def getSerial(self,str):
        print(str)
        return str.split(':')[1].replace(' ','')

    def handlerForSendEvent(self,user,msg):
        #finder setting
        IDI = IDIssuance()
        usecaseFinder =compareSentence.UsecaseFinder()
        usecaseFinder.setUserSetting()
        requestlist=usecaseFinder.analyzeSentence(msg)
        if "howToUse" in requestlist:
            print("도움 ")
            smsg = self.mMsgList.getHowToUse()
            return smsg

        elif "regist" in requestlist:
            id = IDI.getTempID(user)
            print("ID:: "+id)
            if self.mRegister.insertTempID(user, id) == False:
                print(self.mMsgList.ERR_REGISTERD_USER)
                return 
           
            return "아래의 사용자 등록 폼에 따라 등록을 해주세요.\n"+self.SIGN_UP_URL+id
        else :
            res=self.mRegister.insertUserRequest(user," ".join(requestlist))
            if len(requestlist) == 0:
                return self.mMsgList.ERR_RECEVIED_MSG

            #2 리퀘스트에 해당 시리얼 넣음
            return " ".join(requestlist)+res


if __name__ == "__main__":
    print("TEST")