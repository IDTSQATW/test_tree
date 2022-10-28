# Pro_CfgCTL2.py - excuse original txt format
import sys
import time
import System
C2906 = []
C2906.append(["Get Kernal Version","2906","2900"])

C2908 = []
C2908.append(["Get Kernal Check Sum","2908","2900"])

C2909 = []
C2909.append(["Get Cfg Check Sum","2909","2900"])

class Pro_CfgCTL2:
	def KernalVersion(self, DL):
		DL.setText("GREEN", C2906[0][0])
		DL.SendIOCommand("IDG",C2906[0][1], 30000)
		if(DL.Check_RXResponse(C2906[0][2])):
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			strResponse = strResponse[28:len(strResponse) - 4]
			strkernal = DL.getASCIIArray(strResponse)
			DL.setText("BLACK", "Kernal:" + strkernal)
		else:
			strkernal = "Error: Get EMV L2 Kernal Version Fail!"
			DL.setText("RED", "Kernal:" + strkernal)
		return strkernal

	def KernalCheckSum(self, DL):
		DL.setText("GREEN", C2908[0][0])
		DL.SendIOCommand("IDG", C2908[0][1], 30000)
		if (DL.Check_RXResponse(C2908[0][2])):
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			strkernalCS = strResponse[28:len(strResponse) - 4]
			DL.setText("BLACK", "Kernal Check Sum:" + strkernalCS)
		else:
			strkernalCS = "Error: Get EMV L2 Kernal Check SUM Fail!"
			DL.setText("RED", "Kernal Check Sum:" + strkernalCS)
		return strkernalCS

	def KernalCfgCheckSum(self, DL):
		DL.setText("GREEN", C2909[0][0])
		DL.SendIOCommand("IDG", C2909[0][1], 30000)
		if (DL.Check_RXResponse(C2909[0][2])):
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			strConfigCS = strResponse[28:len(strResponse) - 4]
			DL.setText("BLACK", "Config Check Sum:" + strConfigCS)
		else:
			strkernalCS = "Error: Get EMV L2 Config Check SUM Fail!"
			DL.setText("RED", "Kernal Check Sum:" + strConfigCS)
		return strConfigCS

	def IntToHexstring(self, DL,i):
		strx = hex(i).strip().lstrip().upper().replace('0X','')
		if(len(strx) == 1):
			strx = '0'+strx
		return strx

	def TerminalICS1to23C(self,DL, index):
		if (index == 0) or (index > 23):
			strLog = "ICS number shoud be in range [1,23]"
			return strLog
		strLog = "Set ICS :" + str(index)
		DL.SendIOCommand("IDG", '6016' + Pro_CfgCTL2().IntToHexstring(DL,index), 30000)
		strLog += "\r\nSet Terminal Data :"
		return strLog
		
	def GetTerminalICS(self,DL):
		strLog = "Get ICS :\r\n"
		DL.SendIOCommand("IDG", '6015', 30000)
		if (DL.Check_RXResponse('6000')):
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			strICS = strResponse[28:30]
			ICS =  int('0x'+strICS,16)
			strLog = strLog + str(ICS)
		else:
			strLog =  strLog + "Error: Get EMV ICS Fail!"
		strLog += "\r\nSet Terminal Data :"
		return strLog
		