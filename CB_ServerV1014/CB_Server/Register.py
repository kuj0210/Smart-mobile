import pymysql
from DBString import *
from defaultMessage import*
class Register:
	def __init__(self):
		self.mMsgList=MessageList()
		# DB 계정정보 관리
		self.conn = None
		self.curs = None
		self.serial = None
		self.host = "localhost"
		self.user = "d134"
		self.pw = "asdf1234"   		#ss1234
		self.charset = "utf8"

		#로그 정보
		self.LOG = "DB_LOG"
		#전달 문자
		self.SQL =  DBString()
		


      
	def connectDB(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pw, charset=self.charset)
		self.curs = self.conn.cursor()
		try:
		    with self.conn.cursor() as self.curs:        
		    	self.curs.execute(self.SQL.US_DBQ)
		except:
		    with self.conn.cursor() as self.curs:
		        self.curs.execute(self.SQL.CT_DBQ )
		    self.conn.commit()

		    with self.conn.cursor() as self.curs:
		        self.curs.execute(self.SQL.US_DBQ)

	def checkUserTable(self):	   
		    try:
		        with self.conn.cursor() as self.curs:
		            self.curs.execute(self.SQL.ST_UTQ)
		    except:
		        with self.conn.cursor() as self.curs:
		            self.curs.execute(self.SQL.CT_UTQ)
		    self.conn.commit()

	def checkSystemTable(self):
		try:
			with self.conn.cursor() as self.curs:
				self.curs.execute(self.SQL.ST_STQ)
		except:
			with self.conn.cursor() as self.curs:
				self.curs.execute(self.SQL.CT_STQ)
		self.conn.commit()

	def checkRequestTable(self):
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.ST_RQSTQ)
			except:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.CT_RQQ)
			self.conn.commit()

	def checkTempIDTable(self):
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.ST_TIQ)
			except:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.CT_TIQ)
			self.conn.commit()


	def openDB(self):
		self.connectDB()
		self.checkUserTable()
		self.checkSystemTable()
		self.checkRequestTable()
		self.checkTempIDTable()

	def closeDB(self):
		self.conn.close()

	def checkRegistedUserForOuter(self, user_key):
		self.openDB()
		try:
			with self.conn.cursor() as self.curs:
				query = self.SQL.getQ_ST_U_FromUserKey(user_key)
				self.curs.execute(query)
				rows = self.curs.fetchall()
				self.closeDB()
				if len(rows) > 0:
					return True
				else:
					return False
		except:
				self.closeDB()
				return False
		self.closeDB()

	def checkRegistedUser(self, user_key):
		try:
			with self.conn.cursor() as self.curs:
				query = self.SQL.getQ_ST_U_FromUserKey(user_key)
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
				query = self.SQL.getQ_ST_S_FromSerial(serial)
				self.curs.execute(query)
				rows = self.curs.fetchall()
				if len(rows) > 0:
					return True
				else :
					return False
		except:
				return False

	def checkTempIDByTempID(self, tempID):
		try:
			with self.conn.cursor() as self.curs:
				query = self.SQL.getQ_ST_T_FromTempID()
				self.curs.execute(query)
				rows = self.curs.fetchall()
				if len(rows) > 0:
					return True
				else:
					return False
		except:
				return False

	def insertUserData(self, user_key, serial, email, location):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkRegistedUser(user_key) == True:
				return self.mMsgList.ERR_REGISTERD_USER
			try:
				if self.checkRegistedSerial(serial) == False:
					return self.mMsgList.ERR_NO_REGISTERD_SERIAL

				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_IT_U(user_key,serial,email,location))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_IST_USER
			except:
				self.closeDB()
				return self.mMsgList.ERR_REGISTE_USER
		self.closeDB()

	def insertUserRequest(self, user_key, rqst):
		self.openDB()
		if self.checkRegistedUser(user_key) == False:
				return self.mMsgList.ERR_NO_REGISTERD_USER
		SR =self.getSerialFromUser(user_key)

		with self.conn.cursor() as self.curs:
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_IT_R_Value(user_key,SR,rqst))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_RECEVIED_MSG
			except:
				print("인서트예외")
				self.closeDB()
				return self.mMsgList.ERR_RECEVIED_MSG
		self.closeDB()

	def fetchRequest(self,SR):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkRegistedSerial(SR) == False:
				return self.mMsgList.ERR_NO_REGISTERD_SERIAL
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_ST_RQST_From_SR(SR))
					list=self.curs.fetchall()
					if len(list)<=0:
						return False
					self.curs.execute(self.SQL.getQ_DT_RQST_From_SR(SR))
					self.conn.commit()
				self.closeDB()
				return self.listToString(list)
			except:
				self.closeDB()
				return
		self.closeDB()

	def deleteUserData(self, user_key):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkRegistedUser(user_key) == False:
				return self.mMsgList.SUCESS_DEL_NO_REGISTERD_USER
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_DT_U(user_key))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_DEL_REGISTERD_USER
			except:
				self.closeDB()
				return  self.mMsgList.ERR_DEL_REGISTERD_USER
		self.closeDB()

	def deleteTempID(self, tempID):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkTempIDTable() == False:
				return self.mMsgList.SUCESS_DEL_NO_TEMPID
			try:
				with self.conn.cursor() as self.curs:
					print(self.SQL.getQ_DT_T(tempID))
					self.curs.execute(self.SQL.getQ_DT_T(tempID))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_DEL_TEMPID
			except:
				self.closeDB()
				return self.mMsgList.ERR_DEL_TEMPID
		self.closeDB()

	def getSerialFromUser(self,user_key):
		with self.conn.cursor() as self.curs:
			if self.checkRegistedUser(user_key) == False:
				return self.mMsgList.ERR_NO_REGISTERD_USER
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_ST_S_FromUser(user_key))
					SR = self.curs.fetchall()

					if len(SR)<=0:
						return False
				return SR[0][0]
			except:
				print("getsr시리얼 예외")
				return  self.mMsgList.ERR_SCH_SR

	def getUserFromSerial(self,SR):
		with self.conn.cursor() as self.curs:
			if self.checkRegistedSerial(SR) == False:
				return self.mMsgList.ERR_NO_REGISTERD_SERIAL
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_ST_U_FromSerial(SR))
					UK = self.curs.fetchall()
					if len(UK)<=0:
						return False
				return self.listToString(UK)
			except:
				print("겟유저프롬 예외")
				return  self.mMsgList.ERR_SCH_UK

	def insertTempID(self, user_key, id):
		self.openDB()
		if self.checkRegistedUser(user_key) == True:
			return False

		with self.conn.cursor() as self.curs:
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_IT_T(user_key, id))
					self.conn.commit()
				self.closeDB()
				return self.mMsgList.SUCESS_IST_TEMPID
			except:
				self.closeDB()
				return self.mMsgList.ERR_IST_TEMPID
		self.closeDB()

	def getUserKeyByTempID(self, tempID):
		self.openDB()
		with self.conn.cursor() as self.curs:
			if self.checkTempIDTable() == False:
				return self.mMsgList.ERR_NO_TEMPID
			try:
				with self.conn.cursor() as self.curs:
					self.curs.execute(self.SQL.getQ_ST_T_UK_FromTempID(tempID))
					user_key = self.curs.fetchall()[0][0]
					self.curs.execute( self.SQL.getQ_DT_T(tempID))
				self.closeDB()
				return user_key
			except:
				self.closeDB()
				return self.mMsgList.ERR_SCH_UK_FROM_TEMPID
		self.closeDB()


	def listToString(self,list):
		print(list)
		str=""
		for item in list:
			for atom in item:
				str+=atom+" "
			str+="\n"
		return str

if __name__=="__main__":
	user ="u9-NF6yuZ8H8TAgj1uzqnQ"
	Reg =Register()

	print(Reg.insertUserData("testkey", "SR0003", "test@email.com", "Location"))
	print(Reg.insertTempID("testkey", "ID"))
	print(Reg.getUserKeyByTempID("ID"))
	#Reg.deleteUserData("testkey")
	#Reg.deleteTempID("ID")
	print(Reg.insertUserData(user, "SR0003", "test2@email.com", "location2"))
	print(Reg.insertUserRequest(user,"TEST1 TEST2 TEST3"))
	#print(Reg.insertUserRequest("testor","TEST4"))
