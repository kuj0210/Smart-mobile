class DBString:
	def __init__(self):
	#DB 정보관리 , 테이블 명칭 변경 시 모든 쿼리에 적용
		self.DB_NAME = "SystemData"
		self.UT_NAME = "naverUser"
		self.ST_NAME = "mobileSystem"
		self.RQ_NAME = "request"
		self.TI_NANE = "TempID"
		self.MT_NAME = "messageTable"
		#쿼리문 관리

		##DB사용 쿼리문
		self.US_DBQ =	"use %s;"%(self.DB_NAME)
		
		#전달문자관리
		##성공
		self.SUCESS_IST_USER="등록 완료"
		self.SUCESS_DEL_NO_REGISTERD_USER ="미등록 유저입니다. 모든 정보들이 삭제되었습니다"
		self.SUCESS_DEL_REGISTERD_USER="등록 시 넣은 정보들이 정상 삭제 되었습니다."

		##테이블 생성쿼리문
		self.CT_DBQ =  '''
		    	create database %s 
			    	DEFAULT CHARACTER 
			    	SET utf8 collate utf8_general_ci;
                    %s
			    '''%(self.DB_NAME,self.US_DBQ)


		self.CT_UTQ = 	'''
			    create table %s(
				    user_key varchar(50),
				    serial varchar(50),
				    email varchar(100),
				    location varchar(30),
				    primary key (user_key,serial)
				    ) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;
		    '''%(self.UT_NAME)
		

		self.CT_STQ = 	'''
			    create table %s(
				    serial varchar(50),
				    ) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;
			    '''%(self.ST_NAME)


		self.CT_RQQ = 	'''
			    create table %s(
				    serial varchar(50),
				    requestor varchar(50),
					request varchar(50),
					FOREIGN KEY (serial) REFERENCES %s (serial)
				    ) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;
			    '''%(self.RQ_NAME,self.ST_NAME)

		self.CT_TIQ= '''
				create table %s (
					user_key varchar(50),
					ID varchar(50),
					primary key (user_key, ID)
					) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;
				''' %(self.TI_NANE)

		self.CT_MTQ='''
				create table %s (
					msg varchar(250),
					idx int primary key auto_increment
					) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;
				''' %(self.MT_NAME)


		##테이블 선택 쿼리문
		self.ST_UTQ = "select * from %s;"%(self.UT_NAME)
		self.ST_STQ = "select * from %s;"%(self.ST_NAME) 
		self.ST_RQSTQ = "select * from %s;"%(self.RQ_NAME)
		self.ST_TIQ = "select * from %s;"%(self.TI_NANE)
		self.ST_MTQ = "select * from %s;"%(self.MT_NAME)

	# 유저관련 쿼리문
	def getQ_ST_U_FromUserKey(self,UK):
		return "select user_key from %s where %s.user_key = \"%s\";"%(self.UT_NAME,self.UT_NAME,UK)
	
	def getQ_ST_U_FromSerial(self,SR):
		return "select user_key from %s where %s.serial = \"%s\";"%(self.UT_NAME,self.UT_NAME,SR)

	def getQ_ST_U_FromUserKey_Serial(self,UK,SR):
	    return "select * from %s where %s.user_key=\"%s\" and user_key.serial=\"%s\";"%(self.UT_NAME,self.UT_NAME,UK,self.UT_NAME,SR)
	def getQ_IT_U(self,user_key,serial,email,location):
	    return "insert into %s values (\"%s\", \"%s\", \"%s\", \"%s\");"%(self.UT_NAME,user_key,serial,email,location)
	def getQ_DT_U(self,user):
	    return "delete from %s where %s.user_key =\"%s\";"%(self.UT_NAME,self.UT_NAME,user)
	def getQ_ST_ALL_U(self):
		return "select user_key from %s;"%(self.UT_NAME)

	#
	def getQ_IT_SR(self, SR):
		return "insert into %s values (\"%s\");"%(self.ST_NAME, SR)

	#tempID관련 쿼리문
	def getQ_ST_T_UK_FromTempID(self, id):
		return "select user_key from %s where %s.ID = \"%s\";"%(self.TI_NANE, self.TI_NANE, id)
	def getQ_ST_T_FromTempID(self, id):
		return "select * from %s where ID = \"%s\";"%(self.TI_NANE, id)
	def getQ_IT_T(self, user_key, id):
		return "insert into %s values (\"%s\", \"%s\");"%(self.TI_NANE, user_key, id)
	def getQ_DT_T(self, id):
		return "delete from %s where %s.ID = \"%s\";"%(self.TI_NANE, self.TI_NANE, id)


	#시리얼 관련 쿼리문
	def getQ_ST_S_FromSerial(self,SR):
		return "select * from %s where %s.serial = \"%s\";"%(self.ST_NAME,self.ST_NAME,SR)

	def getQ_ST_S_FromUser(self,UR):
		return "select %s.serial from %s where %s.user_key = \"%s\";"%(self.UT_NAME,self.UT_NAME,self.UT_NAME,UR)

    #리퀘스트 관련 쿼리문
	def getQ_IT_R_Value(self,UR,SR,request):
		return "insert into %s values (\"%s\", \"%s\",\"%s\");"%(self.RQ_NAME,SR,UR,request)
	def getQ_ST_RQST_From_SR(self,SR):
		return "select * from %s where %s.serial = \"%s\";"%(self.RQ_NAME,self.RQ_NAME,SR)
	def getQ_DT_RQST_From_SR(self,SR):
		return "delete from %s where %s.serial = \"%s\";"%(self.RQ_NAME,self.RQ_NAME,SR)

    #메세지 관련 쿼리문
	def getQ_ST_M_From_IDX(self,IDX):
		return "select msg from %s where %s.idx = \"%d\";" % (self.MT_NAME, self.MT_NAME, IDX)
	def getQ_IT_M(self, msg):
		return "insert into %s values (\"%s\", NULL);" % (self.MT_NAME, msg)
	def getQ_DT_M_From_IDX(self,IDX):
		return "delete from %s where %s.idx = \"%s\";" % (self.MT_NAME, self.MT_NAME, IDX)
	def getQ_MSG_Table_Len(self):
		return "select count(*) from %s;" % (self.MT_NAME)



if __name__=="__main__":
	sql =DBString()
	str=sql.getQ_ST_S_FromUser("u9-NF6yuZ8H8TAgj1uzqnQ")
	print(str)
