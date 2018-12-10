from observer import *
import cv2
import numpy as np
import time
from datetime import datetime
import os
import glob

class Vi(Observer):
    NAME = '현재'
    PUSHCODE_P1 = NAME+" 아이의 모습입니다"
    PICTURE_NAME = ""
    
    # 메시지 관련
    BREAK_AWAY = "아이가 자리에서 벗어났어요!"
    RETURN_BACK = "아이가 자리에 돌아왔어요!"
    UNTILL_BREAK = "아이가 오랫동안 자리에서 벗어났어요!"

    cap = 0
    frame = []
    picture = []

    def __init__(self,Push):
        self.EV_PUSH = Vi.NAME+"관측 푸쉬"
        self.RQ_PUSH = Vi.NAME+"요청처리 메세지"
        self.reSet(Push)
        self.mPush = Push
        self.setStatToImagePush()
        self.dPusher = self.mPush.insertMSG
        os.system('sudo modprobe bcm2835-v4l2')
        self.CONSTLIST.append(Vi.BREAK_AWAY)
        self.CONSTLIST.append(Vi.RETURN_BACK)
        self.CONSTLIST.append(Vi.UNTILL_BREAK)
        self.removePicture()
        

    def processRequest(self, PUSHCODE):
        try:
            if PUSHCODE == self.PUSHCODE_P1 or self.STATMENT == Observer.STAT_CAMERATHREAD:
                print("Vi - picture request")
                self.openCamera()
                self.writePicture()
                return self.PICTURE_NAME
            else:
                return False
        except:
            print("Vi - request 에러")
            return False

    def openCamera(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap is None:
            print("openCamera 에러")
            return
        ret, self.frame = self.cap.read()
        self.cap.release()

    def writePicture(self):
        self.removePicture()
        now = datetime.now()
        self.PICTURE_NAME = self.mPush.T.SERIAL + '_%s-%s-%s-%s-%s-%s' %(now.year, now.month, now.day, now.hour, now.minute, now.second) + ".png"
        cv2.imwrite(self.PICTURE_NAME, self.frame)
    
    def removePicture(self):
        images = glob.glob('./SR*.png')
        for fname in images:
            os.remove(fname) 

if __name__ == "__main__":
    vi=Vi(Observer)
    vi.run()
