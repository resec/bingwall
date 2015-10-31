# Python Bing Wallpaper Fetcher Database Module
# Initialize the database

import sqlite3 as sqlite
import setting
import log
import lock

SQL_INSERT_PROCESS_DATE="insert into pdates (pdate) values (?)"
SQL_INSERT_RECORD="insert into drecords (pdate, pname) values (?,?)"
SQL_INSERT_PICTURE_NAME="insert into pnames (pname) values (?)"
SQL_SELECT_RECORD_BY_PROCESS_DATE="select pname from drecords where pdate=?"
SQL_SELECT_LATEST_PROCESS_DATE="select max(pdate) from pdates"
SQL_SELECT_PROCESS_DATE="select pdate from pdates where pdate=?" 
SQL_SELECT_PICTURE_NAME="select pname from pnames where pname=?"

settings = setting.getManager().getDefaultSettings()
con=sqlite.connect(settings['database-file-name'], check_same_thread=False)

def init():
	cur=con.cursor()
	cur.executescript(open(settings['database-init-script-name']).read())
	con.commit()
	
if settings['database-init']=='1':
	log.info('Initializing database')
	init()
	settings['database-init']='0'

class dao:

	def __init__(self, con):
		self.con=con
		self._lock = lock.RWLock()

	def insertProcessDate(self, pdate):
		self._lock.acquire_write()
		self.con.execute(SQL_INSERT_PROCESS_DATE, [pdate])
		self.con.commit()
		self._lock.release_write()
		
	def insertRecord(self, pdate, pname):
		self._lock.acquire_write()
		self.con.execute(SQL_INSERT_RECORD, [pdate, pname])
		self.con.commit()
		self._lock.release_write()
		
	def insertPictureName(self, pname):
		self._lock.acquire_write()
		self.con.execute(SQL_INSERT_PICTURE_NAME, [pname])
		self.con.commit()
		self._lock.release_write()
	
	def selectRecordByProcessDate(self, pdate):
		self._lock.acquire_read()
		row = self.con.execute(SQL_SELECT_RECORD_BY_PROCESS_DATE, [pdate]).fetchall()
		self._lock.release_read()
		return row
		
	def selectLatestProcessDate(self):
		self._lock.acquire_read()
		row = self.con.execute(SQL_SELECT_LATEST_PROCESS_DATE).fetchone()
		self._lock.release_read()
		return row
		
	def selectProcessDate(self, pdate):
		self._lock.acquire_read()
		row = self.con.execute(SQL_SELECT_PROCESS_DATE, [pdate]).fetchone()
		self._lock.release_read()
		return row
		
	def selectPictureName(self, pname):
		self._lock.acquire_read()
		row = self.con.execute(SQL_SELECT_PICTURE_NAME, [pname]).fetchone()
		self._lock.release_read()
		return row
		
dao=dao(con)