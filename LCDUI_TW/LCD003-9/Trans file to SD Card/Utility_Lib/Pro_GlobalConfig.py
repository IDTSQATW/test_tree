#Pro_SendCmd Py - Command Exchange
import sys
import time
import System
from System import Array, String

class Pro_GlobalConfig:
	
	# 1, Set Config with tlvSet's field of [Set Test Value]
	# 2, Get Config by 03-02
	# 3, Compare get from device to tlvSet's field of [Default Value]
	#tlvSet
	# Set TLV Set Table:
	# tlvSet = [
	#	[Tag,		Length,		[Set Test Value , Default Value]]
	#	['DFEE2D' ,	'01',		['00',		'00']],
	# 	['9C',		'01',		['00',		'00']],

	# iType
	# 0 : set the test value in tlvSet[i][2][0]
	# 1 : set the test value in tlvSet[i][2][1]

	def SetConfigByType(self,tlvSet,iType, DL):
		C0400 = '04 00'
		for i in range(0,len(tlvSet)):
			C0400 += str(tlvSet[i][0])
			C0400 += str(tlvSet[i][1])
			C0400 += str(tlvSet[i][2][iType])	

		DL.SendIOCommand("IDG",C0400,30000)
		if(False == DL.Check_RXResponse(0,"04 00",True)):
			DL.fails = DL.fails + 1

		DL.SendIOCommand("IDG","03 02",30000)
		strResponse = DL.Get_RXData(0)
		strResponse=strResponse.replace(" ","")
		DL.setText("GREEN",  strResponse)
		TagNumsB = 0
		listTagB=System.Array.CreateInstance(String,1)
		listLengthB=System.Array.CreateInstance(String,1)
		listValueB=System.Array.CreateInstance(String,1)
		(TagNumsB, listTagB,listLengthB,listValueB) = DL.tlvGet(strResponse,listTagB,listLengthB,listValueB)
		if(TagNumsB > 0):
#			DL.setText("Black", "TAG\t\tLength\t\tValue")
#			for i in range(0,TagNumsB):
#				DispInfo = str(listTagB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listLengthB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listValueB[i])
#				DL.setText("Green", DispInfo)
#			DL.setText("Black", "\r\n")
		
			i = 0
			j = 0
			for i in range(0,len(tlvSet)):
				bFind = False
				for j in range(0,TagNumsB):
					if (tlvSet[i][0]== listTagB[j]):
						bFind = True
						break
				if(bFind):
					if( tlvSet[i][0]== '9F21' ):
						if (tlvSet[i][1]== listLengthB[j] and tlvSet[i][2][iType][0:4]== listValueB[j][0:4]):
							DispInfo = "TLV Set OK:\t"
							DispInfo += str(tlvSet[i][0])
							DispInfo += '\t\t'
							DispInfo +=  str(tlvSet[i][1])
							DispInfo += '\t\t'
							DispInfo +=  str(tlvSet[i][2][iType])
							DL.setText("Green", DispInfo)
							continue
					if (tlvSet[i][1]== listLengthB[j] and tlvSet[i][2][iType]== listValueB[j]):
						DispInfo = "TLV Set OK:\t"
						DispInfo += str(tlvSet[i][0])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][2][iType])
						DL.setText("Green", DispInfo)
					else:
						DispInfo = "TLV Set Error:\t"
						DispInfo = str(tlvSet[i][0])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][2][iType])
						DL.setText("Red", DispInfo)
						DL.fails = DL.fails + 1
				else:
					DispInfo = "TLV Set Warning:\t"
					DispInfo += str(tlvSet[i][0])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][1])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][2][iType])
					DL.setText("Red", DispInfo)
					DL.warnings = DL.warnings + 1
	
		if(0 < (DL.fails + DL.warnings)):
			DL.setText("RED", "Pro_GlobalConfig : SetConfigByType - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
			return False
		else:
			DL.setText("GREEN", "Pro_GlobalConfig : SetConfigByType - PASS\r\n Warning:0\r\n Fail:0" )
			return True
	
	# 1, Get Config by 03-02
	# 2, Compare get from device to tlvSet's field of [Default Value]
	# Check the Default Value is right (compare to tlvSet's Default Value)
	# Set TLV Set Table:
	# tlvSet = [
	#	[Tag,		Length,		[Set Test Value , Default Value]]
	#	['DFEE2D' ,	'01',		['00',		'00']],
	# 	['9C',		'01',		['00',		'00']],
	def CheckDefaultConfig(self,tlvSet,DL):
		DL.SendIOCommand("IDG","03 02",30000)
		strResponse = DL.Get_RXData(0)
		strResponse=strResponse.replace(" ","")
		DL.setText("GREEN",  strResponse)
		TagNumsB = 0
		listTagB=System.Array.CreateInstance(String,1)
		listLengthB=System.Array.CreateInstance(String,1)
		listValueB=System.Array.CreateInstance(String,1)
		(TagNumsB, listTagB,listLengthB,listValueB) = DL.tlvGet(strResponse,listTagB,listLengthB,listValueB)
		if(TagNumsB > 0):
#			DL.setText("Black", "TAG\t\tLength\t\tValue")
#			for i in range(0,TagNumsB):
#				DispInfo = str(listTagB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listLengthB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listValueB[i])
#				DL.setText("Green", DispInfo)
#			DL.setText("Black", "\r\n")
		
			i = 0
			j = 0
			for i in range(0,len(tlvSet)):
				bFind = False
				for j in range(0,TagNumsB):
					if (tlvSet[i][0]== listTagB[j]):
						bFind = True
						break
				if(bFind):
					if (tlvSet[i][1]== listLengthB[j] and tlvSet[i][2][1]== listValueB[j]):
						DispInfo = "Default Value OK:\t"
						DispInfo += str(tlvSet[i][0])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][2][1])
						DL.setText("Green", DispInfo)
					else:
						DispInfo = "Default Value Error:\t"
						DispInfo = str(tlvSet[i][0])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][2][1])
						DL.setText("Red", DispInfo)
						DL.fails = DL.fails + 1
				else:
					DispInfo = "Default Value Warning:\t"
					DispInfo += str(tlvSet[i][0])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][1])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][2][1])
					DL.setText("Red", DispInfo)
					DL.warnings = DL.warnings + 1
	
		if(0 < (DL.fails + DL.warnings)):
			DL.setText("RED", "Pro_GlobalConfig : CheckDefaultConfig - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
			return False
		else:
			DL.setText("GREEN", "Pro_GlobalConfig : CheckDefaultConfig - PASS\r\n Warning:0\r\n Fail:0" )
			return True
		



	# tlvSet
	# Set TLV Set Table:
	# tlvSet = [
	#	[Tag,		Length,		Set Test Value ]
	#	['DFEE2D' ,	'01',		'00'],
	# 	['9C',		'01',		'00'],
	def SetConfig(self,tlvSet,DL):
		C0400 = '04 00'
		for i in range(0,len(tlvSet)):
			C0400 += str(tlvSet[i][0])
			C0400 += str(tlvSet[i][1])
			C0400 += str(tlvSet[i][2])	

		DL.SendIOCommand("IDG",C0400,30000)
		if(False == DL.Check_RXResponse(0,"04 00",True)):
			DL.fails = DL.fails + 1
		DL.SendIOCommand("IDG","03 02",30000)
		strResponse = DL.Get_RXData(0)
		strResponse=strResponse.replace(" ","")
		DL.setText("GREEN",  strResponse)
		TagNumsB = 0
		listTagB=System.Array.CreateInstance(String,1)
		listLengthB=System.Array.CreateInstance(String,1)
		listValueB=System.Array.CreateInstance(String,1)
		(TagNumsB, listTagB,listLengthB,listValueB) = DL.tlvGet(strResponse,listTagB,listLengthB,listValueB)
		if(TagNumsB > 0):
#			DL.setText("Black", "TAG\t\tLength\t\tValue")
#			for i in range(0,TagNumsB):
#				DispInfo = str(listTagB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listLengthB[i])
#				DispInfo += '\t\t'
#				DispInfo +=  str(listValueB[i])
#				DL.setText("Green", DispInfo)
#			DL.setText("Black", "\r\n")
			
			i = 0
			j = 0
			for i in range(0,len(tlvSet)):
				bFind = False
				for j in range(0,TagNumsB):
					if (tlvSet[i][0]== listTagB[j]):
						bFind = True
						break
				if(bFind):
					if( tlvSet[i][0]== '9F21' ):
						if (tlvSet[i][1]== listLengthB[j] and tlvSet[i][2][0:4]== listValueB[j][0:4]):
							DispInfo = "TLV Set OK:\t"
							DispInfo += str(tlvSet[i][0])
							DispInfo += '\t\t'
							DispInfo +=  str(tlvSet[i][1])
							DispInfo += '\t\t'
							DispInfo +=  str(tlvSet[i][2][iType])
							DL.setText("Green", DispInfo)
							continue
					if (tlvSet[i][1]== listLengthB[j] and tlvSet[i][2] == listValueB[j]):
						DispInfo = "TLV Set OK:\t"
						DispInfo += str(tlvSet[i][0])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t\t'
						DispInfo +=  str(tlvSet[i][2])
						DL.setText("Green", DispInfo)
					else:
						DispInfo = "TLV Set Error:\t"
						DispInfo = str(tlvSet[i][0])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][1])
						DispInfo += '\t'
						DispInfo +=  str(tlvSet[i][2])
						DL.setText("Red", DispInfo)
						DL.fails = DL.fails + 1
				else:
					DispInfo = "TLV Set Warning:\t"
					DispInfo += str(tlvSet[i][0])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][1])
					DispInfo += '\t'
					DispInfo +=  str(tlvSet[i][2])
					DL.setText("Red", DispInfo)
					DL.warnings = DL.warnings + 1
			
	
		if(0 < (DL.fails + DL.warnings)):
			DL.setText("RED", "Pro_GlobalConfig : SetConfig - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
			return False
		else:
			DL.setText("GREEN", "Pro_GlobalConfig : SetConfig - PASS\r\n Warning:0\r\n Fail:0" )
			return True