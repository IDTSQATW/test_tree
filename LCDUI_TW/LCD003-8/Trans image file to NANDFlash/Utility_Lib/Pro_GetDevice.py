#Pro_GetDevice Py - use for get device type ?
import sys
import time
import System
strK310 = '4B696F736B204949492056312E31302E'
strK310S = '4B696F736B204949492056312E31302E??????2E53'
strK320 = '4B696F736B204949492056312E32302E'
strK320S = '4B696F736B204949492056312E32302E??????2E53'
strK420 = '4B696F736B2049562056312E32302E'
strK420 = '4B696F736B2049562056312E32302E??????2E53'
SRED = '2E53'

Reader = [["Kiosk III",0],["Kiosk IV",7],["VP3600", 11],['VP6800', 12],['VP5300',13],['VP3320',14],['VP3320S',15]]
class Pro_GetDevice:
#Get Reader FW
	def Run(self,DL):
		self.DL = DL
		Result = True
		self.DL.setText("GREEN", 'Get Device Firmware Version:')
		self.DL.SendIOCommand("IDG", "29 00", 30000)
		Result = self.DL.Check_RXResponse("29 00")
		strResponse = self.DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		strResponse = strResponse[28:len(strResponse)-4]
		strFW =self. DL.getASCIIArray(strResponse)
		self.DL.setText("BLACK", strFW)
		a = -1
		for listn in Reader:
		#self.DL.setText("GREEN", listn[0] + str(strFW.find(listn[0])))
			if(strFW.find(listn[0]) >= 0):a = listn[1]
			
		if (a == 0):
		#K3V1.10.S=1,V1.10.sta=2,V1.10.NCR=3;
		#K3V1.20.S=4,V1.20.sta=5,V1.20.NCR=6
			if (strResponse.find(SRED)>=0):
				if(strResponse.find(strK310)>=0): return 1
				elif(strResponse.find(strK320)>=0): return 4
				else: return -1
			elif (strResponse.find(strK310)>=0):
				strVersion = strResponse[32:len(strResponse)]
				if ( int(strVersion)%2 == 0): return 3
				else: return 2
			elif(strResponse.find(strK320)>=0):
				strVersion = strResponse[32:len(strResponse)]
				if ( int(strVersion)%2 == 0): return 6
				else: return 5
			else: return -1
		elif( a == 7):	
		#K4V1.20.sta=7,V1.20.NCR=8
			if (DL.Check_RXResponse(strResponse,strK420)):
				strVersion = strResponse[30:len(strResponse)]
				if ( int(strVersion)%2 == 0): return 8
				else: return 7
		else: return a

#!Get Reader SN
	def RunSN(self,DL):
		self.DL = DL
		Result = True
		self.DL.setText("GREEN", 'Get Device Serial Number:')
		self.DL.SendIOCommand("IDG", "1201", 3000)
		strResponse = self.DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
		self.DL.setText("GREEN", strSN)
		return strSN