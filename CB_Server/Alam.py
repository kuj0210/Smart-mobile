import threading
import time
from serverManageMent import NaverManager
from Register import Register

class Alam:
    def __init__(self,H,M,S):
        self.T = threading.Thread(target=self.alamForThread)

        self.H_s = int(H.split("-")[0])
        self.H_e = int(H.split("-")[1])

        self.M_s = int(M.split("-")[0])
        self.M_e = int(M.split("-")[1])

        self.S_s = int(S.split("-")[0])
        self.S_e = int(S.split("-")[1])

    def alamToUser(self):
        nM = NaverManager()
        tm = time.localtime()

        userList = self.rg.getALL_UserKey()
        Len = self.rg.getMsgTableLen()
        self.index %= Len
        self.index += 1
        msg = self.rg.getMSGfromIDX(self.index)
        print("test1")
        print(msg)
        print(index)
        print(userList)
        for user in userList:
            print("in loop")
            nM.sendPush(nM.PUSH_URL, user, "오늘의 꿀팁")
            nM.sendIMAG(user, nM.IMAGE_URL + msg)

    def alamForThread(self):
        while True:
            current = time.localtime()
            h = current.tm_hour
            m = current.tm_min
            s = current.tm_sec

            ck1 = self.H_s <= h and self.H_e>=h
            ck2 = self.M_s <= m and self.M_e>=m
            ck3 = self.S_s <= s and self.S_e >=s
            if ck1 and ck2 and ck3:
                self.alamToUser()
                time.sleep(0.5)

    def run(self):
        self.T.start()
a = Alam("13-14","0-59","30-30")
a.run()


