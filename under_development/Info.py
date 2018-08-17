from observer import *
import time
import pigpio
import PPD42NS
import DHT22

class Info(Observer):
    def __init__(self, Push):
        self.reSet(Push)
        self.Dust_BCM = 24
        self.DHT_BCM = 22
        self.sleep_timer = 100

    def run(self):
        print("running info")
        while (True):
            try:
                item = self.popRQ()
            except:
                print("info에서 popRQ 리퀘스트 받기 에러")
                continue

            try:
                DHT_msg, Warning_flag = self.DHT_Run(self.DHT_BCM)
            except:
                print("값 읽기 에러 - info request")
                continue

            try:
                if item != False:
                    print("request info")
                    Dust_msg = self.Dust_Run(self.Dust_BCM)
                    self.mPush.insertMSG(item.user, "Smart mobile에서 요청에 응답드립니다-%s\n" % DHT_msg + Dust_msg)

                if self.sleeper():
                    continue

                if Warning_flag:
                    print("Warning msg")
                    self.mPush.insertMSG('ALL', "Smart mobile에서 알려드립니다-%s\n" % DHT_msg)
                    self.sleep_timer = 0
                    time.sleep(10)
            except:
                print("푸시 에러")
                continue

    def sleeper(self):
        self.sleep_timer += 1
        if self.sleep_timer < 60:
            time.sleep(10)
            return True
        return False

    def Dust_Run(self, BCM):
        pi = pigpio.pi()
        s = PPD42NS.sensor(pi, BCM)
        while True:
            time.sleep(1)
            g, r, c = s.read()
            if r > 0:
                break
        msg = "\n  -먼지 농도 : {0:.1f}".format(r)
        pi.stop()
        return msg

    def DHT_Run(self, BCM):
        INTERVAL = 3
        pi = pigpio.pi()
        s = DHT22.sensor(pi, BCM)
        r = 0
        next_reading = time.time()

        while True:
            r += 1
            s.trigger()
            time.sleep(0.2)
            h = s.humidity()
            t = s.temperature()
            next_reading += INTERVAL
            time.sleep(next_reading - time.time())
            if h > -100 and t > -100:
                break

        msg = "\n 현재 방 안의\n  -습도 : {0:.4f}per\n  -온도 : {1:.4f}`C".format(h, t)
        flag = False
        if h > 80 or t > 40:
            flag = True
        s.cancel()
        pi.stop()
        return msg, flag

            t = s.temperature()
            next_reading += INTERVAL
            time.sleep(next_reading - time.time())
            if h > -100 and t > -100:
                break

        msg = "\n 현재 방 안의\n  -습도 : {0:.4f}per\n  -온도 : {1:.4f}`C".format(h, t)
        flag = False
        if h > 80 or t > 40:
            flag = True
        s.cancel()
        pi.stop()
        return msg, flag
