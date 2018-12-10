import time
import threading

class Request:
    def __init__(self,u,m):
        self.user=u
        self.msg=m

class Observer(object):
    # 푸쉬종류 구분, 외부 참조내용 내부에서 구분할때도 사용할것
    PUSHCODE_P1 = "ob1"
    PUSHCODE_P2 = "ob2"
    PUSHCODE_P3 = "ob3"

    STAT_CAMERATHREAD = "camera thread"
    STAT_ANOTHOERTHREAD = "anther thread"
    STAT_NOMALTHREAD = "nomal thread"
    def __init__(self,push):
        #메세지 정의부
        self.EV_PUSH = "옵저버푸쉬"  # 상속받는 하위 클래스는 해당내용 변경할것, 필요하다면 추가
        self.RQ_PUSH = "요청이 완료되었습니다."  # 상속받는 하위 클래스는 해당내용 변경할것, 필요하다면 추가
        self.STATMENT =Observer.STAT_NOMALTHREAD
        self.CONSTLIST=[]
        self.reSet(push)

    def setPusher(self):
        self.dPusher = self.mPush.insertMSG
        self.pPusher = self.mPush.insertMSG
    def setImagePusher(self):
        self.dPusher = self.mPush.T.pushImage
        self.pPusher = self.mPush.T.pushImage

    def setStatToImagePush(self):
        self.setImagePusher()
        self.STATMENT = Observer.STAT_CAMERATHREAD

    def setStatToAnotherForImage(self):
        self.STATMENT = Observer.STAT_ANOTHOERTHREAD



    #건들면죽인다2
    def reSet(self,push):
        self.mRQList =[]
        self.mPush =push
        self.sem_using = threading.Semaphore(1)
        self.setPusher()
        self.CONSTLIST=[]


    #이거 건들면 죽는걸로 안끝남
    def insertRQ(self,user,msg):
        self.sem_using.acquire()
        self.mRQList.append(Request(user,msg))
        self.sem_using.release()

    #이거 건들면 죽는걸로 안끝남2
    def popRQ(self):
        self.sem_using.acquire()
        if len(self.mRQList)==0:
            self.sem_using.release()
            return False
        rq = self.mRQList.pop(0)
        self.sem_using.release()
        return rq

    #오버라이딩, 요청처리기능 만약 하위 클래스가 처리하는게 없다면 False 반환
    def processRequest(self, PUSHCODE):
        if (PUSHCODE !=-1):
            return self.RQ_PUSH +"  "+PUSHCODE
        else:
            return False# 하는일이 없다면

    # 오버라이딩, 관측 중 푸쉬해야하는 상황이 발생하면 정의해둔 메세지 리턴
    def detectEnvironment(self):
        res = False  # 적당한 메서드를 호출해서 알람발생해야한다면 알람에 들어갈 메세지 리턴하게할것
        # 반드시 위에 상수를 참조하여 쓸 걸

        if (res == False):
            return False
        else:  # 필요시 elif등 사용할것
            return self.res


    # 건들지 말것(오버라이딩금지)
    def detect(self):
        res = self.detectEnvironment()
        if(res):
            return res
        else:
            return False


    #이거 건들면 죽는걸로 안끝남3
    def run(self):
        while(True):
            rqst = self.popRQ()# 들어온 기능 요청 확인
            if(rqst): #만약 요청이 왔다면,
                pmsg=self.processRequest( rqst.msg ) #요청처리함수 실행, 결과받기
                self.pPusher(rqst.user, pmsg)# 메세지전달
                if (self.STATMENT == Observer.STAT_CAMERATHREAD):
                    self.mPush.insertMSG(rqst.user, rqst.msg)

            dmsg =self.detect() # 관측시작
            if(dmsg): #특이점 발견 시
                if self.STATMENT == Observer.STAT_NOMALTHREAD: #일반이면 모두 푸쉬
                    self.dPusher('ALL', dmsg)
                elif self.STATMENT == Observer.STAT_ANOTHOERTHREAD:#카메라 스레드아니면
                    self.mPush.pushToObjerver(self.mPush.VI, 'ALL', dmsg)




