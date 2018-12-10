class MessageList:
    def __init__(self):

        #for chattingRoom EV
        self.OPEN_MSG = """안녕하세요!!! Smart Mobile 시스템입니다.
        무엇을 도와드릴까요?"""
        self.LEAVE_MSG = "나중에 또봐요~ :)"
        self.SUCESS_RECEVIED_MSG = " 기능이 접수완료 되었습니다."
        

        #for message EV
        self.ERR_TYPE_MSG ="현재 지원하지 않는 타입의 메세지예요 ㅠㅠ"
        self.ERR_RECEVIED_MSG = '모르겠어요! 사용이 어려우시면 "도움말"을 입력해보시겠어요?'
        #for friend EV
        self.ON_FRIEND_MSG = "안녕하세요! Smart Mobile이에요! 친구가 되서 반가워요"
        self.OFF_FRIEND_MSG = "더는 친구가 아니게 되었네요... 즐거웠어요"

        
        #for regist EV
        ##성공
        self.SUCESS_IST_USER="등록 완료"
        self.SUCESS_DEL_NO_REGISTERD_USER ="미등록 유저입니다. 모든 정보들이 삭제되었습니다"
        self.SUCESS_DEL_REGISTERD_USER="등록 시 넣은 정보들이 정상 삭제 되었습니다."
        self.SUCESS_DEL_NO_TEMPID="TEMPID가 없습니다"
        self.SUCESS_DEL_TEMPID = "TEMPID가 삭제되었습니다."
        self.SUCESS_IST_TEMPID = "TEMPID가 입력 성공"

		##에러
        self.ERR_REGISTERD_USER="이미 등록된 유저입니다."
        self.ERR_NO_REGISTERD_SERIAL="잘못된 시리얼번호입니다."
        self.ERR_REGISTE_USER="유저등록에러"
        self.ERR_DEL_REGISTERD_USER="등록정보 삭제 에러"
        self.ERR_SCH_SR = "시리얼 확인중 알 수 없는 에러가 발생 했습니다"
        self.ERR_SCH_UK = "유저 확인중 알 수 없는 에러가 발생 했습니다"
        self.ERR_NO_REGISTERD_USER = "미등록된 유저입니다"
        self.ERR_DEL_TEMPID = "TEMPID 삭제 에러"
        self.ERR_IST_TEMPID = "TEMPID 입력 에러"
        self.ERR_NO_TEMPID = "TEMPID가 없습니다."
        self.ERR_SCH_UK_FROM_TEMPID = "UK 확인 에러 from TEMPID"
        
        #for help EV
    
        self.HOW_TO_USE ='''info [주어]: 온도,습도,먼지,공기,방,상황 [동사]알려[가중치] 모두다
        music [주어]: 동요,노래 [동사]재생,들려주 [가중치] 모두다
        voice [주어]: 목소리,음성,엄마,아빠,부모,가족 [동사]재생,들려주 [가중치] 모두다
        camera [주어]: 사진,상황,모습,얼굴,현황 [동사]보여주,찍,알려 [가중치] 모두다
        howToUse 도움말
        regist 등록 : serial (ex) 등록:SR_1452
        '''
  
      

    def getOpenMsg(self):
        return self.OPEN_MSG

    def getLeavMsg(self):
        return self.LEAVE_MSG
    def getFriendOn(self):
        return self.ON_FRIEND_MSG
    def getFriendOff(self):
        return self.OFF_FRIEND_MSG

    def getmessageTypeError(self):
        return self.ERR_TYPE_MSG
    def getHowToUse(self):
        return self.HOW_TO_USE

  