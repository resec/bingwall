# Python Bing Wallpaper Fetcher Setting Module

import configparser

SETTING_FILE_NAME='/home/yougoer/Pictures/BingWallPaper/bingwall/setting.ini'
DEFAULT_SETTING_GROUP='DEFAULT'

class manager:
	def __init__(self, sfile, _interpolation):
		self.configparser = configparser.SafeConfigParser(interpolation=_interpolation)
		self.configparser.read(sfile)
	
	def getDefaultSettings(self):
		return self.getSettings(DEFAULT_SETTING_GROUP)

	def getSettings(self, group):
		return self.configparser[group]
		
def getManager(interpolation=configparser.BasicInterpolation()):
	return manager(SETTING_FILE_NAME,interpolation)