from flask import request
import defaultMessage
import compareSentence
from Register import Register

class NaverManager:
    def __init__(self):
        self.mMsgList =defaultMessage.MessageList()
        self.mRegister = Register(self.mMsgList)
        
    def getPostBodyMessage(self,user,text):
        postBodyMessage = {
            "event": "send",
            "user" : user,
            "textContent": {
                "text": text
            }
        }
        return postBodyMessage

    # 2차원 데이터를 1차원으로 변경
    def getDataFromNaverTalk(self,dataFromMessenger):
        dicForSaveUserData ={}
        user = dataFromMessenger["user"]
        event = dataFromMessenger["event"] 
        dicForSaveUserData ={"user":user,"event":event}

        if event !="friend":
            dicForSaveUserData["typing"] = dataFromMessenger["textContent"]["inputType"]
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
        return str.split(':')[1].replace(' ','')

    def handlerForSendEvent(self,user,msg):
            #finder setting
        usecaseFinder =compareSentence.UsecaseFinder()
        usecaseFinder.setUserSetting()
        requestlist=usecaseFinder.analyzeSentence(msg)
        if "howToUse" in requestlist:
            smsg = mMsgList.getHowToUse()
            return smsg
        elif "regist" in requestlist:
            serial =self.getSerial(msg)
            smsg=self.mRegister.insertUserData(user,serial)
            return smsg
        return " ".join(requestlist)