from Vi import *
from Vo import *
from Info import *
from Translator import *


class Push():
    VI = "VI"
    VO = "VO"
    IF = "IF"

    def __init__(self):
        self.T = Translator()
        self.sem_using = threading.Semaphore(1)  # 1명만 쓸것
        self.sem_emp = threading.Semaphore(0)  # 처음 큐는 비어있음
        self.sem_ob = threading.Semaphore(1)
        self.Q = []

        self.observerDic = {}
        self.thList = []
        self.setUpObserverDic()
        self.setUpThread()
        self.PushTh = threading.Thread(target=self.run)

    def setUpObserverDic(self):
        self.observerDic[Push.VI] = Vi(self)
        self.observerDic[Push.VO] = Vo(self)
        self.observerDic[Push.IF] = Info(self)

    def pushToObjerver(self, OB_CODE, user, msg):
        self.sem_ob.acquire()
        if OB_CODE in self.observerDic:
            self.observerDic[OB_CODE].insertRQ(user, msg)
        else:
            raise ("CAN NOT FIND OBJSERVER")
        self.sem_ob.release()

    def setUpThread(self):
        for ob in self.observerDic:
            self.thList.append(threading.Thread(target=self.observerDic[ob].run))

    def insertMSG(self, user, str):
        self.sem_using.acquire()  # 사용을 알림
        self.Q.append(Request(user, str))
        self.sem_using.release()  # 다썻다 알림
        self.sem_emp.release()  # 세마포어 값 증가, 비어있던 큐에 1개들어갓음 알림

    def getMSG(self):
        self.sem_emp.acquire()  # 비어있으면 대기
        self.sem_using.acquire()  # 쓴다고 알림
        msg = self.Q[0]
        del self.Q[0]
        self.sem_using.release()  # 다
        return msg

    def startTh(self):  # on observer
        for th in self.thList:
            th.start()

    def run(self):
        self.startTh()
        cunt = 0
        while (True):
            print("wait.....")
            msg = self.getMSG()
            if msg.user == "ALL":
                print("ALL")
                self.T.pushToAllUser(msg.msg)
            else:
                print("user")
                self.T.pushToUser(msg.user, msg.msg)


if __name__ == "__main__":
    p = Push()
    p.PushTh.start()
