import threading

class Vi():
    def __init__(self,Push):
        self.mPush = Push
    def run(self):
        while(True):
            if(True): #이탈 시
                self.mPush.insertMSG("비디오 스레드")

class Vo():
    def __init__(self,Push):
        self.mPush = Push
    def run(self):
        while(True):
            if(True): #이탈 시
                self.mPush.insertMSG("음성 스레드")

class Push(threading.Thread):
    def __init__(self):
        self.sem_using = threading.Semaphore(1) # 1명만 쓸것
        self.sem_emp = threading.Semaphore(0)
        self.Q=[]
        self.mvi = Vi(self)
        self.mvo = Vo(self)
        self.VIth =threading.Thread(target=self.mvi.run)
        self.VOth = threading.Thread(target=self.mvo.run)

    def insertMSG(self,str):
        self.sem_using.acquire()
        self.Q.append(str)
        print("--------------------in 관측자[%s]삽입완료"%str)
        self.sem_using.release()
        self.sem_emp.release() # 세마포어 값 증가

    def getMSG(self):
        self.sem_emp.acquire()
        self.sem_using.acquire()
        msg =self.Q[0]
        del self.Q[0]
        self.sem_using.release()
        return msg

    def run(self):
        self.VIth.start()
        self.VOth.start()
        while(True):
            print("in 관찰자[%s]"%( self.getMSG()) )


p=Push()
p.run()
