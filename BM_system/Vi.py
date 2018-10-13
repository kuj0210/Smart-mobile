from observer import *
import cv2
import numpy as np
import time
import os

class Vi(Observer):
    BREAK_AWAY = ""
    RETURN_BACK = ""
    UNTILL_BREAK = ""
    frame = []
    origin_frame = []
    my_contours = []
    st_frame = 0
    out_frame = 0
    sz_frame = 0
    os_frame = 0
    ob_frame = 0
    sz_size = 0
    cap = 0
    vi_width = 0
    vi_height = 0
    contours = []
    edges = []
    mx = 0
    my = 0
    sz_x = 0
    sz_y = 0
    sz_w = 0
    sz_h = 0
    old_frame = []
    old_gray = []
    diff = []



    def __init__(self,Push):
        self.reSet(Push)
        self.BREAK_AWAY = "아이가 자리에서 벗어났어요!"
        self.RETURN_BACK = "아이가 자리에 돌아왔어요!"
        self.UNTILL_BREAK = "아이가 오랫동안 자리에서 벗어났어요!"
        self.mPush = Push
        self.sz_frame = 15
        self.os_frame = 10
        self.ob_frame = 1
        self.sz_size = 100
      
    def outCheck(self):
        if self.mx > self.sz_x and self.mx < self.sz_x + self.sz_w and self.my > self.sz_y and self.my < self.sz_y + self.sz_h:
            return 0
        else:
            return 1  

    def openCamera(self):
        os.system('sudo modprobe bcm2835-v4l2')
        self.cap = cv2.VideoCapture(0)
        self.vi_width = int(self.cap.get(3))
        self.vi_height = int(self.cap.get(4))     
        self.getSaftyZone()
        ret, self.old_frame = self.cap.read()
        if self.old_frame is None:
            print("camera error1")
            return
        self.old_gray = cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
        
    def getCapture(self):
        ret, self.frame = self.cap.read()
        if self.frame is None:
            print("camera error2")
            return
        self.origin_frame = self.frame.copy()
        self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.diff = cv2.absdiff(self.old_gray, self.frame_gray)
        kernel = np.ones((3, 3), np.float32) / 25
        dst = cv2.filter2D(self.diff, -1, kernel)
        self.edges = cv2.Canny(dst, 0, 30)
        _, self.contours, _ = cv2.findContours(self.edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    def getMoment(self):
        max_area = 0
        ci = 0
        for i in range(0, len(self.contours)):
            cnt = self.contours[i]
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_area = area
                ci = i
        cnt = self.contours[ci]
        mmt = cv2.moments(cnt)
        if mmt['m00'] != 0:
            self.mx = int(mmt['m10'] / mmt['m00'])
            self.my = int(mmt['m01'] / mmt['m00'])
        cv2.rectangle(self.frame, (int(self.mx), int(self.my)), (int(self.mx), int(self.my)), (0, 0, 255), 8)
        if self.frame is None:
            return

    def getSaftyZone(self):
        self.sz_x = self.vi_width / 4
        self.sz_y = self.vi_height / 4
        self.sz_w = self.vi_width / 2
        self.sz_h = self.vi_height / 2
        self.setSafttyZoneSize()
       
    def setSafttyZoneSize(self):
        tmp_rx = self.sz_x
        tmp_ry = self.sz_y
        self.sz_x = tmp_rx + int((100 - self.sz_size) / 200 * self.sz_w)
        self.sz_y = tmp_ry + int((100 - self.sz_size) / 200 * self.sz_h)
        self.sz_w = self.sz_size / 100 * self.sz_w
        self.sz_h = self.sz_size / 100 * self.sz_h

    def checkSaftyZone(self):
        if self.outCheck() == 1:
            self.out_frame = self.out_frame + 1
        else:
            if self.out_frame > 30:
                self.out_frame = 0
                return (self.RETURN_BACK)
        if self.out_frame == 30:
            return (self.BREAK_AWAY)
        if self.out_frame > 0 and self.out_frame % 500 == 0:
            return (self.UNTILL_BREAK)
        return 0
    
    def checkObserveFrame(self):
        self.st_frame = self.st_frame + 1
        if self.st_frame < self.os_frame: return 1
        if self.st_frame != self.sz_frame:
            if self.st_frame % self.ob_frame != 0 and self.out_frame == 0:
                return 1
            if self.st_frame % 5 != 0:
                return 1
        return 0

    def run(self):
        print("Running Vi")
        while(True):
            try :
                if self.cap == 0 :
                    self.openCamera()
            except :
                print("Open camera error")
                continue
            try :
                item = self.popRQ()
            except :
                print("Vo에서 popRQ 리퀘스트 받기 에러")
                continue
            if (item != False):
                try :
                    print("Running picture request")
                    cv2.imwrite(self.mPush.T.SERIAL + ".png" , self.origin_frame)
                    self.mPush.T.pushImage(item.user,self.mPush.T.SERIAL + ".png" )
                except :
                    print('Picture push error')
                    continue

            if(True):
                if self.checkObserveFrame() == 1:
                    continue
                try :
                    self.getCapture()
                    if self.contours :
                        self.getMoment()
                except :
                    print("Image processing error")
                try :
                    MSG = self.checkSaftyZone()
                    if MSG != 0:
                        self.mPush.insertMSG('ALL', MSG)
                        #time.sleep(10)
                except :
                    print("MSG error")                    
                cv2.imshow('fgmask', self.frame)
                cv2.imshow('EDGES', self.edges)
                k = cv2.waitKey(1) & 0xff
                if k == 27:
                    break
                self.old_gray = self.frame_gray.copy()
        self.cap.release()
        cv2.destroyAllWindows()

        time.sleep(15)


