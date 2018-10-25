from observer import *
import cv2
import numpy as np
import time
import os

class Vi(Observer):
    # 사용자의 요청 구분 예)목소리들려줘 노래들려줘 구분, 외부 참조내용 내부에서 구분할때도 사용할것
    NAME = 'VI'
    PUSHCODE_P1 = NAME + "-사진"
    # PUSHCODE_P2 = NAME+"-ob2"
    # PUSHCODE_P3 = NAME+"-ob3"

    # 메시지 관련
    BREAK_AWAY = "아이가 자리에서 벗어났어요!"
    RETURN_BACK = "아이가 자리에 돌아왔어요!"
    UNTILL_BREAK = "아이가 오랫동안 자리에서 벗어났어요!"

    # 카메라 관련
    cap = 0
    vi_width = 0
    vi_height = 0
    origin_frame = []

    # 영상처리 관련
    old_frame = []
    old_gray = []
    frame = []
    frame_gray = []
    diff = []
    edges = []
    contours = []

    # 세이프티존 관련
    sz_x = 0
    sz_y = 0
    sz_w = 0
    sz_h = 0

    # 관찰 프레임 관련
    st_frame = 0
    out_frame = 0
    sz_frame = 0
    os_frame = 0
    ob_frame = 0

    # 무게중심 관련
    mx = 0
    my = 0

    # 타임 관련
    return_time = 0
    out_time = 0
    untill_time = 0


    def __init__(self, Push):
        self.EV_PUSH = Vi.NAME + "관측 푸쉬"
        self.RQ_PUSH = Vi.NAME + "요청처리 메세지"
        self.reSet(Push)
        self.mPush = Push
        self.sz_frame = 15
        self.os_frame = 10
        self.ob_frame = 1
        self.sz_size = 100
        print("Running Vi")
        while (self.cap == 0):
            try:
                self.openCamera()
            except:
                print("Open camera error")
                continue


    # 오버라이딩, 요청처리기능 만약 하위 클래스가 처리하는게 없다면 False 반환
    def processRequest(self, PUSHCODE):
        try:
            if (PUSHCODE == self.PUSHCODE_P1):  # 넘어오는 코드별로 분류하여 행동처리 PUSHCODE == PUSHCODE_P1 이런식으로
                print("Vi - picture request")
                self.picturePush()
                return self.RQ_PUSH + "  " + PUSHCODE
            else:
                return False
        except:
            print("Vi - request 에러")
            return False

    # 오버라이딩, 관측 중 푸쉬해야하는 상황이 발생하면 정의해둔 메세지 리턴
    def detectEnvironment(self):
        try:
            self.getCapture()
            if self.contours:
                self.getMoment()
        except:
            print("Image processing error")
        try:
            res = self.checkSaftyZone  # 적당한 메서드를 호출해서 알람발생해야한다면 알람에 들어갈 메세지 리턴하게할것
            #  반드시 위에 상수를 참조하여 쓸 걸
            if (res == False):
                return False
            else:  # 필요시 elif등 사용할것
                return self.res
        except:
            return False
        self.showFrame()
        self.waitCamera()
        self.copyFrame()

    def openCamera(self):
        os.system('sudo modprobe bcm2835-v4l2')
        self.cap = cv2.VideoCapture(0)
        self.vi_width = int(self.cap.get(3))
        self.vi_height = int(self.cap.get(4))
        self.getSaftyZone()
        ret, self.old_frame = self.cap.read()
        if self.old_frame is None:
            print("Old camera error")
            return
        self.old_gray = cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)\

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

    def checkObserveFrame(self):
        self.st_frame = self.st_frame + 1
        if self.st_frame < self.os_frame: return 1
        if self.st_frame != self.sz_frame:
            if self.st_frame % self.ob_frame != 0 and self.out_frame == 0:
                return 1
            if self.st_frame % 5 != 0:
                return 1
        return 0

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

    def checkSaftyZone(self):
        time = time.time()
        el_return_time = time - self.return_time
        el_out_time = time - self.out_time
        el_untill_time = time - self.untill_time
        if self.outCheck() == 1:
            self.out_frame = self.out_frame + 1
        else:
            if self.out_frame > 30 and int(el_return_time) % 300:
                self.out_frame = 0
                self.out_time = 0
                return (self.RETURN_BACK)
            if self.out_frame == 30 and int(el_out_time) % 300:
                self.out_time = time.time()
                return (self.BREAK_AWAY)
            if self.out_frame > 0 and self.out_frame % 500 == 0 and int(el_untill_time) % 600 == 0:
                self.untill_time = time.time()
                return (self.UNTILL_BREAK)
            return 0
        
    def picturePush(self):
        cv2.imwrite(self.mPush.T.SERIAL + ".png", self.origin_frame)
        self.mPush.T.pushImage(item.user, self.mPush.T.SERIAL + ".png")

    def copyFrame(self):
        self.old_gray = self.frame_gray.copy()

    def showFrame(self):
        cv2.imshow('fgmask', self.frame)
        cv2.imshow('EDGES', self.edges)

    def waitCamera(self):
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            return

if __name__ == "__main__":
    vi = Vi(Observer)
    vi.run()
