# Python Bing Wallpaper Fetcher Service Module

import database
import time

def saveProcessDate(pdate):
	row=database.dao.selectProcessDate(pdate)
	if row==None:
		database.dao.insertProcessDate(pdate)

def savePictureName(pname):
	row=database.dao.selectPictureName(pname)
	if row==None:
		database.dao.insertPictureName(pname)
	
def saveRecord(pdate, pname):
	saveProcessDate(pdate)
	savePictureName(pname)
	database.dao.insertRecord(pdate, pname)
	
def isFetched(pname):
	row=database.dao.selectPictureName(pname)
	if row!=None:
		return True
	else:
		return False
	
	
def getDayCountSinceLatestProcessDate():
	value=database.dao.selectLatestProcessDate()
	if (value[0]==None or value[0]==0):
		return 1

	lpdate=time.strptime(str(value[0]),"%Y%m%d")
	now=time.time()
	return int((now-time.mktime(lpdate))/(24*60*60))
	
def isTodayFetched():
	return getDayCountSinceLatestProcessDate()<=0