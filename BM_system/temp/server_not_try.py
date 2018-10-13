
import time
from push import *

class MobileSystem:
    def __init__(self):
        self.T = Translator()
        self.Push = Push()
        self.CONFIG = "configPI.txt"
        #시스템 정보

        #값 초기화
        if self.loadSerail() ==False:
            exit()
        self.bootUp()
        print("프로그램 안전부팅 완료")
    def parshResponseByNL(self,res):
        res =res.split("\n")
        res.pop()
        for i in range(len(res)):
            res[i]=res[i].strip()
        return res
    def parshResponseBySP(self,res):
        res =res.split(" ")
        return res


    def loadSerail(self):
        try:
            with open(self.CONFIG, "r") as f:
                Translator.SERIAL=f.readline()
                return True
        except:
            print("파일 입출력 에러")
            return False
        return False
    def bootUp(self):
        res=self.T.sendMsg(self.T.BOOT_URL,"NO_USER",Translator.SERIAL)
        Translator.userList= self.parshResponseByNL(res)
        print(Translator.userList)

    def getRequest(self,wating):
        time.sleep(wating)
        res = self.T.sendMsg(self.T.RQST_URL,"NO_USER",Translator.SERIAL)
        if 'NO' in res:
            return False
        res =self.parshResponseByNL(res)
        list =[]
        for item in res:
            atom = self.parshResponseBySP(item)
            atom.pop(0)
            list.append(atom)
        return list
    def runMobile(self):
        #self.T.pushImage(Translator.userList[0],Translaotr.SERIAL+".png")
        print("프로그램 시작합니다.")
        self.Push.PushTh.start()


        while True:
            list =self.getRequest(5)
            if list ==False:
                continue
            else:
                list =list.pop(0)
                user = list.pop(0)
                
                print(list)

                if 'UPDATE' in list:
                    print("유저변동발생!")
                    self.bootUp()

                if 'info' in list:
                    self.Push.observerList[Push.IF].insertRQ(user, "인포메이션 스레드::정보기능완료")  # 사진기능 요청
                if 'camera' in list:
                    self.Push.observerList[Push.VI].insertRQ(user, "비디오스레드::사진기능완료")  # 사진기능 요청
                if 'voice' in list:
                    self.Push.observerList[Push.VO].insertRQ(user,"voice")
                if 'music' in list:
                    self.Push.observerList[Push.VO].insertRQ(user,"music")

if __name__ =="__main__":
    MS=MobileSystem()
    MS.runMobile()

