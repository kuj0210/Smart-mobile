class MessageList:
    def __init__(self):

        #for chattingRoom EV
        self.OPEN_MSG = """
                안녕하세요!!! Smart Mobile 시스템입니다.
                무엇을 도와드릴까요?
                """
        self.LEAVE_MSG = "나중에 또봐요~ :)"
        
        #for message EV
        self.ERR_TYPE_MSG ="현재 지원하지 않는 타입의 메세지예요 ㅠㅠ"

        #for friend EV
        self.ON_FRIEND_MSG = "안녕하세요! Smart Mobile이에요! 친구가 되서 반가워요"
        self.OFF_FRIEND_MSG = "더는 친구가 아니게 되었네요... 즐거웠어요"
        
        #for regist EV
        
        ##성공
        self.SUCESS_IST_USER="등록 완료"
        self.SUCESS_DEL_NO_REGISTERD_USER ="미등록 유저입니다. 모든 정보들이 삭제되었습니다"
        self.SUCESS_DEL_REGISTERD_USER="등록 시 넣은 정보들이 정상 삭제 되었습니다."

		##에러
        self.ERR_REGISTERD_USER="이미 등록된 유저입니다."
        self.ERR_NO_REGISTERD_SERIAL="잘못된 시리얼번호입니다."
        self.ERR_REGISTE_USER="유저등록에러"
        self.ERR_DEL_REGISTERD_USER="등록정보 삭제 에러"
        
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

  