#Pro_GetDevice Py - use for get device type ?
import sys
import time
import System

Reader = \
	[["Kiosk III",0],["Kiosk IV",7],["VP3600", 11],['VP6800', 12],['VP5300',13],['VP3320',14],['VP3320S',15],['VP6300',16],['VP3350',17]]

class Pro_GetDevice:
# get reader firmware version
	def Run(self, DL):
		self.DL = DL
		Result = True
		self.DL.SendIOCommand("IDG", "29 00", 30000)
		Result = self.DL.Check_RXResponse("29 00")
		strResponse = self.DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) <= 32):
			return -1
		strResponse = strResponse[28:len(strResponse) - 4]
		strFW = self.DL.getASCIIArray(strResponse)
		self.DL.setText("GREEN", 'Get Device Firmware Version:' + strFW)
		a = -1
		for listn in Reader:
			if(strFW.find(listn[0]) >= 0):
				a = listn[1]
		if (a>10):self.DL.SendIOCommand("IDG", "C7 3F", 30000)
		if (a == 13):self.DL.SendIOCommand("IDG", "C7 C7 FF FF", 30000)
		return a

# get reader SN
	def RunSN(self,DL):
		self.DL = DL
		Result = True
		self.DL.SendIOCommand("IDG", "1201", 3000)
		strResponse = self.DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if (len(strResponse) <= 32):
			self.DL.setText("Red", 'Get Device Serial Number Failed!')
			return ""
		strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
		self.DL.setText("GREEN", 'Get Device Serial Number:' + strSN)
		return strSN