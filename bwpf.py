# Python Bing Wallpaper Fetcher
# Author ReSec
# The Bing XML URL to fetch: http://www.bing.com/HPImageArchive.aspx
# With parameter:
# format=xml, indicates this will return an XML formatted stream that contains information such as the date the images is for, the relative URL, description, and copyright information.
# idx=0, tells where you want to start from. 0 would start at the current day, 1 the previous day, 2 the day after that, etc. For instance, if the date were 1/30/2011, using idx = 0, the file would start with 20110130; using idx = 1, it would start with 20110129; and so forth.
# n=1, tells how many images to return. n = 1 would return only one, n = 2 would return two, and so on.
# mkt tells which of the eight markets Bing is available for you would like images from. 
# The valid mkt values are: en-US, zh-CN, ja-JP, en-AU, en-UK, de-DE, en-NZ, en-CA.
# This script will try to fetch the above XML and get today's Bing Wallpaper URL, then download the 1920*1200 picture and then set it as Windows Background

import xml.etree.ElementTree
import urllib.request
import os
import re
import time
import threading
import log
import setting
import service
 
manager = setting.getManager()
settings = manager.getDefaultSettings()
lock = threading.RLock()

def fetchElementTree(xmlUrl):
    et = None
    try:
        log.info('Connect to %s to fetch XML' % xmlUrl)
        response = urllib.request.urlopen(xmlUrl,timeout=5)
        et = xml.etree.ElementTree.fromstring(response.read())
    except Exception as e:
        log.exception(e)
    return et

def getWallPaperNodes(root):
    return root.findall(settings['xml-path-image'])
    
def getWallPaperBaseUrl(imageNode):
    return imageNode.find(settings['xml-path-base-url']).text

def parseWallPaperBaseName(wallpaperBaseUrl):
    return re.split(r'/', wallpaperBaseUrl)[-1]
    
def parseWallPaperRealName(wallpaperBaseName):
    return re.split(r'_', wallpaperBaseName)[0]
    
def getWallPaperDate(imageNode):
    return imageNode.find(settings['xml-path-start-date']).text

def fetchWallpaper(wallpaperUrl,wallpaperPath):
    try:
        urllib.request.urlretrieve(wallpaperUrl,filename=wallpaperPath)
        return 0
    except Exception as e:
        log.exception(e)
    return 1

markets=settings['markets'].split(r',')

log.info('Start program')

processDate=time.strftime('%Y%m%d',time.localtime(time.time()))
xmlBaseUrl = settings['xml-base-url']
n = max(min(service.getDayCountSinceLatestProcessDate(),8), int(settings['url-parm-n']))
attempCountMax = int(settings['failure-attemp-time'])
lock = threading.Lock()

def fetchWallpaperFromMarket(market):
    marketAttempCount = 0
    while (marketAttempCount < attempCountMax):
        log.info('Downlaod xml for market: %s' % market)
        xmlUrl = xmlBaseUrl + 'format=' + settings['url-parm-format'] + '&idx=' + settings['url-parm-index'] + '&n=' + str(n) + '&mkt=' + market
        xmlElementTreeRoot = fetchElementTree(xmlUrl)

        if xmlElementTreeRoot != None:
            log.info('Fetched XML, parse wallpaper information and download')
            imageNodeList=getWallPaperNodes(xmlElementTreeRoot)
            
            for imageNode in imageNodeList:
                # parse the Wallpaper URL
                wallpaperBaseUrl = getWallPaperBaseUrl(imageNode)
                wallpaperBaseName = parseWallPaperBaseName(wallpaperBaseUrl)
                wallpaperRealName = parseWallPaperRealName(wallpaperBaseName)
                wallpaperPiexlSize = settings['wallpaper-pixel-width'] + 'x' + settings['wallpaper-pixel-hight']
                wallpaperNamePostfix = '_' + wallpaperPiexlSize + '.' + settings['wallpaper-foramt']
                wallpaperUrl = settings['wallpaper-base-url'] + wallpaperBaseName + wallpaperNamePostfix
                wallpaperFolder = settings['wallpaper-folder']
                wallpaperTempFolder = settings['temp-folder']
                wallpaperPath = wallpaperFolder + processDate + '_' + wallpaperRealName + '_' + market + wallpaperNamePostfix
                wallpaperTempPath = wallpaperTempFolder + '/' + processDate + '_' + wallpaperRealName + '_' + market + wallpaperNamePostfix + '.temp'
                
                # show Wallpaper info
                log.info('------------------------------------------')
                log.info('Wallpaper Information')
                log.info('Base  Url  : %s' % wallpaperBaseUrl)
                log.info('Base  Name : %s' % wallpaperBaseName)
                log.info('Real  Name : %s' % wallpaperRealName)
                log.info('Full  Url  : %s' % wallpaperUrl)
                log.info('Full  Path : %s' % wallpaperPath)
                log.info('------------------------------------------')
                
                log.info('Fetch wallpaper')
                fetchAttempCount = 0
                while (fetchAttempCount  < attempCountMax):
                    log.info('Check if %s has been fetched before' % wallpaperTempPath)
                    if not os.path.exists(wallpaperTempPath):
                        exitCode = fetchWallpaper(wallpaperUrl, wallpaperTempPath)
                    else:
                        log.info('Wallpaper %s has been download to temp folder, skip download' % (wallpaperTempPath))
                        exitCode = 0

                    if exitCode == 0:
                        lock.acquire()
                        if service.isFetched(wallpaperRealName)==True:
                            log.info('Wallpaper %s has been move to picture folder, skip it' % (wallpaperRealName))
                            lock.release()
                            break
                    
                        log.info('%s %s has been temperately fetched to %s' % (wallpaperRealName, market, wallpaperTempPath))
                        log.info('Moving %s from %s to %s' % (wallpaperRealName, wallpaperTempPath, wallpaperPath))
                        os.rename(wallpaperTempPath, wallpaperPath)
                        service.saveRecord(processDate, wallpaperRealName)
                        lock.release()
                        break
                    else:
                        fetchAttempCount = fetchAttempCount + 1
                        sleep=settings['failure-sleep-time']
                        log.warning('Encountered error while fetching wallpaper, retry again in %s seconds' % sleep)
                        time.sleep(int(settings['failure-sleep-time']))
                
            break
        else:
            marketAttempCount = marketAttempCount + 1
            sleep=settings['failure-sleep-time']
            log.error('Encountered error while fetching XML for %s, retry again in %s seconds' % (market, sleep))
            time.sleep(int(settings['failure-sleep-time']))

time.sleep(2)

threadList = []
for market in markets:
    time.sleep(0.25)
    threadName = market
    thread = threading.Thread(target=fetchWallpaperFromMarket, name=threadName, args=(market,))
    thread.start()
    threadList.append(thread)

while (len(threadList) > 0):
    #log.info('Still has ' + str(len(threadList)) + ' thread running')
    
    while (len(threadList) > 0 and not threadList[0].is_alive()): del threadList[0]
        
    time.sleep(2)
    
log.info('Process is done, exit program')