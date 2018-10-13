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

    def run(self):
        print("running info")
        while (True):
            try:
                item = self.popRQ()
            except:
                print("info에서 popRQ 리퀘스트 받기 에러")
                continue

            try:
                g, r, c = self.Dust_Run()
                h, t = self.DHT_Run()
            except:
                print("값 읽기 에러 - info request")
                continue

            try:
                if (item != False):
                    print("request info")
                    result_msg = "\n현재 방 안의\n  -습도 : {0:.4f}per\n -온도 : {1:.4f}`C\n -먼지 농도 : {2:.2f}per\n 입니다.\n".format(h, t, r)
                    self.mPush.insertMSG(item.user, "Smart mobile에서 요청에 응답드립니다-%s" % result_msg)

                if (True):
                    if (h > 80) or (t > 35):
                        result_msg = "\n현재 방 안의\n  -습도 : {0:.4f}per\n -온도 : {1:.4f}`C\n -먼지 농도 : {2:.2f}per\n로 쾌적하지 않습니다.\n".format(h, t, r)
                        self.mPush.insertMSG('ALL', "Smart mobile에서 알려드립니다-%s" % result_msg)
                        time.sleep(15)
            except:
                print("푸시 에러")
                continue

    def Dust_Run(self):
        pi = pigpio.pi()
        s = PPD42NS.sensor(pi, self.Dust_BCM)
        g, r, c = s.read()
        while True:
            time.sleep(1)  # Use 30 for a properly calibrated reading.
            g, r, c = s.read()
            if r >= 0 and r <= 100:
                break
        pi.stop()
        return g, r, c

    def DHT_Run(self):
        INTERVAL = 3
        pi = pigpio.pi()
        s = DHT22.sensor(pi, self.DHT_BCM)
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

        s.cancel()
        pi.stop()
        return s.humidity(), s.temperature()