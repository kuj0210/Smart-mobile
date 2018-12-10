from observer import *
import time
import pigpio
import PPD42NS
import DHT22
import os

class Info(Observer):
    # 사용자의 요청 구분 예)목소리들려줘 노래들려줘 구분, 외부 참조내용 내부에서 구분할때도 사용할것
    NAME = 'Info'
    PUSHCODE_P1 = NAME+"INFO" #둘다
    PUSHCODE_P2 = NAME+"DHT"  #온습도만
    PUSHCODE_P3 = NAME+"DUST" #먼지만

    def __init__(self,Push):
        self.EV_PUSH = Info.NAME+"관측 푸쉬"
        self.RQ_PUSH = Info.NAME+"요청처리 메세지"
        self.reSet(Push)
        self.mPush = Push
        self.Dust_BCM = 24 #먼지센서 BCM핀 번호
        self.DHT_BCM = 22  #온습도 BCM핀 번호
        self.Info_Lock = 1000   #realam 타이머
        self.setStatToAnotherForImage()
        os.system('sudo pigpiod')


    #오버라이딩, 요청처리기능 만약 하위 클래스가 처리하는게 없다면 False 반환
    def processRequest(self, PUSHCODE):
        if (PUSHCODE == self.PUSHCODE_P1): # 온습도 먼지   #넘어오는 코드별로 분류하여 행동처리 PUSHCODE == PUSHCODE_P1 이런식으로
            try:
                r = self.Dust_Run()
                r /= 2
                h, t = self.DHT_Run()
                res = "\n  -습도 : {0:.4f}per\n -온도 : {1:.4f}`C\n -먼지 농도 : {2:.2f}per\n 입니다.\n".format(h, t, r)
                return self.RQ_PUSH + res
            except:
                print("값 읽기 에러 - info-info")
                return False

        else:
            return False

    # 오버라이딩, 관측 중 푸쉬해야하는 상황이 발생하면 정의해둔 메세지 리턴
    def detectEnvironment(self):
        res = False  # 적당한 메서드를 호출해서 알람발생해야한다면 알람에 들어갈 메세지 리턴하게할것
                    # 반드시 위에 상수를 참조하여 쓸 걸
        r, h, t = 0, 0, 0

        if self.Info_Lock < 300:  # Lock이 걸렸을 시
            self.Info_Lock += 1
            time.sleep(1)
            return False

        try:
            r = self.Dust_Run()
            r /= 2
            h, t = self.DHT_Run()
            print(h, t, r)  #센서 구동 확인용 print (습도, 온도, 먼지농도)
            res = "Info-detecte\n  -습도 : {0:.4f}per\n -온도 : {1:.4f}`C\n -먼지 농도 : {2:.2f}per\n 입니다.\n".format(h, t, r)
        except:
            print("값 읽기 에러 - info")

        if (res == False):
            return False
        elif (h > 90 or t > 30 or r >80 or t < 10):  # 필요시 elif등 사용할것
            self.Info_Lock = 0   #결과 리턴시 Lock 일단 50초
            return res



    ############################################################################################################

    def Dust_Run(self):   #먼지농도 확인
        pi = pigpio.pi()
        s = PPD42NS.sensor(pi, self.Dust_BCM)
        g, r, c = s.read()
        while True:
            time.sleep(1)  # Use 30 for a properly calibrated reading.
            g, r, c = s.read()
            if r >= 0 and r <= 100:
                break
        pi.stop()
        return r

    def DHT_Run(self):   #온습도 확인
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
            #elif h == -999 and t == -999:
                #print("DHT - 센서 핀 연결확인")

        s.cancel()
        pi.stop()
        return s.humidity(), s.temperature()

#Info.py 테스트
#if __name__ == "__main__":
#    I = Info(Observer)
#    print(I.processRequest("INFO"))
#    while True:
#        print(I.Info_Lock)
#        print(I.detectEnvironment())