import pymysql

class Register:
	def __init__(self,msgList):
		self.mMsgList=msgList
		# DB 계정정보 관리
		self.conn = None
		self.curs = None
		self.serial = None
		self.host = "localhost"
		self.user = "root"
		self.pw = "1234"
		self.charset = "utf8"

		#로그 정보
		self.LOG = "DB_LOG"
		#전달 문자

		#DB 정보관리 , 테이블 명칭 변경 시 모든 쿼리에 적용
		self.DB_NAME = "SystemData"
		self.UT_NAME = "naverUser"
		self.ST_NAME = "mobileSystem"
		#쿼리문 관리

		##DB사용 쿼리문
		self.US_DBQ =	"use %s;"%(self.DB_NAME)
		
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
					primary key (user_key,serial)
					) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;

	
			'''%(self.UT_NAME)
		

		self.CT_STQ = 	'''
				create table mobileSystem(
					serial varchar(50),
					url varchar(50)
					) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;


				'''

		##테이블 선택 쿼리문
		self.ST_UTQ = "select * from naverUser;"
		self.ST_STQ = "select * from mobileSystem;"

		
      
	def connectDB(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pw, charset=self.charset)
		self.curs = self.conn.cursor()

	def checkUserTable(self):
		try:
		    with self.conn.cursor() as self.curs:        
		    	self.curs.execute(self.US_DBQ)
		except:
		    with self.conn.cursor() as self.curs:
		        self.curs.execute(self.CT_DBQ )
		    self.conn.commit()

		    with self.conn.cursor() as self.curs:
		        self.curs.execute(self.US_DBQ)

		   
		    try:
		        with self.conn.cursor() as self.curs:
		            self.curs.execute(self.ST_UTQ)
		    except:
		        with self.conn.cursor() as self.curs:
		            self.curs.execute(self.CT_UTQ)
		    self.conn.commit()

	def checkSystemTable(self):
		try:
			with self.conn.cursor() as self.curs:
				self.curs.execute(self.ST_STQ)
		except:
			with self.conn.cursor() as self.curs:
				self.curs.execute(self.CT_STQ)
		self.conn.commit()

	def openDB(self):
		self.connectDB()
		self.checkUserTable()
		self.checkSystemTable()


	def closeDB(self):
		self.conn.close()


	#유저 관련 쿼리문
	def getSTUQ_FromUserKey(self,UK):
		return "select * from %s where %s.user_key = \"%s\";"%(self.UT_NAME,self.UT_NAME,UK)
	def getSTUQ_FromUserKey_Serial(self,UK,SR):
		return "select * from %s where %s.user_key=\"%s\" and user_key.serial=\"%s\";"%(self.UT_NAME,self.UT_NAME,UK,self.UT_NAME,SR)
	def getITUQ(self,user_key,serial):
		return "insert into %s values (\"%s\", \"%s\");"%(self.UT_NAME,user_key,serial)
 	
	#시리얼 관련 쿼리문
	def getSTSQ_FromSerial(self,SR):
		return "select * from %s where %s.serial = \"%s\";"%(self.ST_NAME,self.ST_NAME,SR)


	def checkRegistedUser(self, user_key):
		try:
			with self.conn.cursor() as self.curs:
				query = self.getSTUQ_FromUserKey(user_key)
				self.curs.execute(query)
				rows = self.curs.fetchall()

				if len(rows) > 0: 
					return True
				else:
					return False
		except:
				return False

	def checkRegistedSerial(self, serial):
		try:
			with self.conn.cursor() as self.curs:
				query = self.getSTSQ_FromSerial(serial)
				self.curs.execute(query)
				rows = self.curs.fetchall()
				if len(rows) > 0: 
					return True
				else :
					return False

		except:
				return False

			


	def insertUserData(self, user_key, serial):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkRegistedUser(user_key) == True:
				return self.mMsgList.ERR_REGISTERD_USER
			try:
				if self.checkRegistedSerial(serial) == False:
					return self.mMsgList.ERR_NO_REGISTERD_SERIA
				
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.getITUQ(user_key,serial))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_IST_USER
			except:
				self.closeDB()
				return self.mMsgList.ERR_REGISTE_USER


	def getDTUQ(self,user):
		return "delete from %s where %s.user_key =\"%s\";"%(self.UT_NAME,self.UT_NAME,user)
	
	def deleteUserData(self, user_key):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkRegistedUser(user_key) == False:
				return self.mMsgList.SUCESS_DEL_NO_REGISTERD_USER
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.getDTUQ(user_key))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_DEL_REGISTERD_USER
			except:
				self.closeDB()
				return  self.mMsgList.ERR_DEL_REGISTERD_USER	







