from flask import request
import defaultMessage
import compareSentence

class NaverManager:
    def __init__(self):
        self.mMsgList =defaultMessage.MessageList()
    
        
    def getPostBodyMessage(self,user,text):
        postBodyMessage = {
            "event": "send",
            "user" : user,
            "textContent": {
                "text": text
            }
        }
        return postBodyMessage


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



    def eventHandler(self,infomationFromNaverTalk):
        sendMSG = "None"
        msgList =self.mMsgList

        if infomationFromNaverTalk["event"] == "open":
            sendMSG = msgList.getOpenMsg()
    
        elif infomationFromNaverTalk["event"] == "leave":
            sendMSG =msgList.getLeavMsg()

        elif infomationFromNaverTalk["event"]=="friend":
            if infomationFromNaverTalk["state"]=="on":
                sendMSG = msgList.getFriendOn()
            else:
                sendMSG = msgList.getFriendOff()
        elif infomationFromNaverTalk["event"]=="echo":
            return "Echo"

         
        elif infomationFromNaverTalk["event"] == "send" and infomationFromNaverTalk["typing"]=="typing":   
            sendMSG =self.handlerForSendEvent(infomationFromNaverTalk["user"],infomationFromNaverTalk["message"])
            print("return")
            print(sendMSG)
        else:
            sendMSG =msgList.getmessageTypeError()
        
        postBodyMessage = self.getPostBodyMessage( infomationFromNaverTalk["user"],sendMSG) 
        return postBodyMessage
         

    def handlerForSendEvent(self,user,msg):
            #finder setting
        usecaseFinder =compareSentence.UsecaseFinder()
        usecaseFinder.setUserSetting()
        requestlist=usecaseFinder.analyzeSentence(msg)
        if "howToUse" in requestlist:
            requestlist+="\ninfo [주어]: 온도,습도,먼지,공기,방,상황 [동사]알려[가중치] 모두다"
            requestlist+="\n\nmusic [주어]: 동요,노래 [동사]재생,들려주 [가중치] 모두다"
            requestlist+="\n\nvoice [주어]: 목소리,음성,엄마,아빠,부모,가족 [동사]재생,들려주 [가중치] 모두다"
            requestlist+="\n\ncamera [주어]: 사진,상황,모습,얼굴,현황 [동사]보여주,찍,알려 [가중치] 모두다"

      
        return " ".join(requestlist)
