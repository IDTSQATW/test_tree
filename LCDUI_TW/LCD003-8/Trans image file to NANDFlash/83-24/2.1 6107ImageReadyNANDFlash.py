#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import System
import os
import os.path


DL.SendIOCommand("IDG", "832600", 30000)
time.sleep(0.1)

def getDateTime():
	strYMD = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	return str(strYMD)

def GetFiles_libFatherPath():
	Pathfather = str(__file__).replace(r'\2.1 6107ImageReadyNANDFlash.py','')+ r'\ANANDFiles'
	return Pathfather

def CkFileExist(FilePath):
	try:
		f =open(FilePath)
		f.close()
	except IOError:
		return False
	return True
 
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    return fsize

LogFatherPath = GetFiles_libFatherPath()
DL.setText('Green',LogFatherPath)

def getListFiles(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
          ret.append(os.path.join(root,filespath))
    return ret
ret = getListFiles(LogFatherPath)
# print(ret)
IMAGES = []
list = []
for i in ret:
      if (os.path.splitext(i)[1]=='.jpg') or (os.path.splitext(i)[1]=='.JPG'):
            list.append(i)
for j in range(0,len(list)):
	#DL.setText('BLACK',list[j])
	#DL.setText('BLACK',str(get_FileSize(list[j])) + "bytes")
	tmp = list[j]
	filename = tmp.replace(LogFatherPath  , "")
	filename = filename.replace ('\\',"")
	IMAGES.append ([list[j] , get_FileSize(list[j]),filename])
DL.setText('BLACK','Total No = ' + str(len(IMAGES)))


for catch in IMAGES:
	DL.ClearWindowText()
	DL.setText('RED',catch[2])
	DL.setText('RED',str(catch[1]))
	DL.setText('GREEN',catch[0])
	IMAGEONE = []
	file = open(catch[0],"rb")
	packscount = 0 
	if (0 == catch[1]%1000):
		packscount = catch[1]/1000
	else:
		packscount = catch[1]/1000 + 1
	for k in range (0, packscount):
		if((catch[1]%1000 > 0) and k == packscount):
			IMAGEONE.append(DL.stringToHexString(file.read(catch[1]%1000)))	
		else:
			IMAGEONE.append(DL.stringToHexString(file.read(1000)))
	file.close()
	INDEX = 0
	SCMD = "8324" + DL.stringToHexString(catch[2]) + "00" + DL.stringToHexString(str(catch[1])) + "00"
	for l in range (0, packscount):
		STMP = SCMD
		INDEX = INDEX + 1
		if(catch[1] <= 1000):
			DL.setText('RED',"Only 1 PACK " )
			STMP = STMP + "3300"
		else:
			if(INDEX == 1):
				DL.setText('RED',"Send 1st PACK " )
				STMP = STMP + "3200"
			elif(INDEX == packscount):
				DL.setText('RED',"Send last PACK " )
				STMP = STMP + "3100"
			else:
				DL.setText('BLACK',"Send normal PACK " )
				STMP = STMP + "3000"
		DL.setText('BLACK',"PACK Index " + str(l) + ":\r\n") #+ IMAGEONE[l])
		STMP = STMP + IMAGEONE[l]
		DL.SendIOCommand("IDG", STMP, 30000)
		#time.sleep(0.1)
		
	IMAGEONE = []
	#break #Lock single
	SCMD = ""
