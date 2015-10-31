# Python Bing Wallpaper Fetfher Log Module

import time
import logging
import setting

print('Initialing Log Module')
manager = setting.getManager(interpolation=None)
settings = manager.getDefaultSettings()
 
logger = logging.getLogger('debug')
logger.setLevel(logging.DEBUG)

# file handler 
logFileName='%s.log' % time.strftime('%Y%m%d',time.localtime(time.time()))
fh = logging.FileHandler(settings['log-folder']+'/'+logFileName)
fh.setLevel(logging.DEBUG)

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
 
# create formatter
formatter = logging.Formatter(settings['log-format'])
 
# set formatter for both handlers
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
 
def debug(msg):
    logger.debug(msg)
	
def info(msg):
    logger.info(msg)
 
def error(msg):
    logger.error(msg)
	
def warning(msg):
	logger.warning(msg)
	
def exception(e):
	logger.exception(e)
	
def log_uncaught_exception(ex_cls, ex, tb):

    logger.critical(''.join(traceback.format_tb(tb)))
    logger.critical('{0}: {1}'.format(ex_cls, ex))

    sys.excepthook = log_uncaught_exception