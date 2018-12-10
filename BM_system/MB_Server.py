import time
from push import *

class MobileSystem:
    def __init__(self):
        # 시스템 정보
        self.CONFIG = "configPI.txt"

        # 필요변수 생성
        self.T = Translator()
        self.Push = Push()
        self.USECASEDIC = {}

        #값 초기화
        self.setUsecase()
        if self.loadSerail() ==False:
            exit()
        self.bootUp()

    # parshing for data from server
    def parshResponseByNL(self,res):
        res =res.split("\n")
        res.pop()
        for i in range(len(res)):
            res[i]=res[i].strip()
        return res
    def parshResponseBySP(self,res):
        res =res.split(" ")
        return res

    # for data load
    def loadSerail(self):
        try:
            with open(self.CONFIG, "r") as f:
                Translator.SERIAL=f.readline()
                return True
        except:
            print("파일 입출력 에러")
            return False
        return False
    def setUsecase(self):
        #유스케이스 = [푸쉬클래스내의 구분코드, 전달할 메세지코드]
        self.USECASEDIC["info"] = [self.Push.IF, Info.PUSHCODE_P1]
        self.USECASEDIC["camera"] =[self.Push.VI,Vi.PUSHCODE_P1]
        self.USECASEDIC["music"] = [self.Push.VO,Vo.PUSHCODE_P1]
        self.USECASEDIC["voice"] = [self.Push.VO,Vo.PUSHCODE_P2]
    def bootUp(self):
        res = -1
        while res==-1:
            try:
                res=self.T.sendMsg(self.T.BOOT_URL,"NO_USER",Translator.SERIAL)
                Translator.userList= self.parshResponseByNL(res)
                print(Translator.userList)
            except:
                print("유저로딩 실패, 재시도")
                res = -1

    # for get data from server
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
    def classfyList(self,toDoList):
        user_data = toDoList.pop(0)
        user = user_data.pop(0)
        return user,user_data

    # for push
    def getOB_CODE(self,UC_CODE):
        return self.USECASEDIC[UC_CODE][0]
    def getPUSHCODE(self,UC_CODE):
        return self.USECASEDIC[UC_CODE][1]

    # system run
    def runMobile(self):
        try:
            self.Push.PushTh.start()
            print("하위시스템 on")
        except:
            print("하위시스템 ERR")
            return

        while True:
            try:
                toDoList = self.getRequest(6)
                if toDoList == False:
                    print("No toDoList")
                    continue
                else:
                    print(toDoList)
                    while (len(toDoList) > 0):
                        user,user_data = self.classfyList(toDoList)
                        if 'UPDATE' in user_data:
                            self.bootUp()
                        for UC_CODE in self.USECASEDIC:
                            if UC_CODE in user_data:
                                self.Push.pushToObjerver(self.getOB_CODE(UC_CODE),user,self.getPUSHCODE(UC_CODE))

            except:
                print("runMobile 리퀘스트 에러")

if __name__ =="__main__":
    MS=MobileSystem()
    MS.runMobile()

