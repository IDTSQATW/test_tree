#Pro_PKI Py - Activate, Master Reset, Erase All Keys
import sys
import time
import System
#################Get UTC###################
def int_to_bcd(x):
	"""
	This translates an integer into
	binary coded decimal
	"""
	if x < 0:
		raise ValueError("Cannot be a negative integer")
	bcdstring = ''
	while (x > 0):
		nibble = x % 16
		if (nibble <= 9):
			bcdstring = str(nibble) + bcdstring

		if (nibble == 10):
			bcdstring = 'A' + bcdstring

		if (nibble == 11):
			bcdstring = 'B' + bcdstring

		if (nibble == 12):
			bcdstring = 'C' + bcdstring

		if (nibble == 13):
			bcdstring = 'D' + bcdstring

		if (nibble == 14):
			bcdstring = 'E' + bcdstring

		if (nibble == 15):
			bcdstring = 'F' + bcdstring

		x >>= 4

	if (len(bcdstring) == 1):
		return  '0' + bcdstring
	else:
		return bcdstring


#!  This Method get current OS time.
#!  return a list of below:
#!                  [year, month, day, hour, minute, second]
#!
def getDateTime():
	strYMD = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	Year = strYMD[0:4]
	Month = strYMD[5:7]
	Day = strYMD[8:10]
	Hour = strYMD[11:13]
	Minute = strYMD[14:16]
	Second = strYMD[17:19]
	Data_List=[]
	Data_List.append(Year)
	Data_List.append(Month)
	Data_List.append(Day)
	Data_List.append(Hour)
	Data_List.append(Minute)
	Data_List.append(Second)
	return Data_List
#!  This Method get current OS time and convert it to BCD Code Format.
#!  Data Item	Length bytes	    Description
#!  Minutes     1                   mm 2-digit,BCD,Range 00-59
#!  Hour	    1	                HH 2-digit, BCD, Range 00-23
#!  Year1	    1	                YY1 (Higher Century Byte)  2-digit, BCD, Range 00-99
#!  Year2	    1	                YY2 (Lower Century Byte)  2-digit, BCD, Range 00-99
#!  Month	    1	                MM  2-digit, BCD, Range 01-12
#!  Date	    1	                DD  2-digit, BCD, Range 01-31
#!  return a string of below:
#!                  nHour + nMinute + nYear1 + nYear2 + nMonth + nDate
def getUTCCommandTime_BCD():
	MyTime = getDateTime()
	Hour = MyTime[3]
	nHour = int_to_bcd(int(Hour,10))

	Minute = MyTime[4]
	nMinute = int_to_bcd(int(Minute,10))

	Year1 = MyTime[0][0:2]
	nYear1 = int_to_bcd(int(Year1,10))

	Year2 = MyTime[0][2:4]
	nYear2 = int_to_bcd(int(Year2,10))

	Month = MyTime[1]
	nMonth = int_to_bcd(int(Month,10))

	Date = MyTime[2]
	nDate = int_to_bcd(int(Date,10))
	print (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)
	return (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)
###########################################


class Pro_PKI:
	#!  This Method get current OS time and convert it to BCD Code Format.
	#!  Data Item	Length bytes	    Description
	#!  Minutes     1                   mm 2-digit,BCD,Range 00-59
	#!  Hour	    1	                HH 2-digit, BCD, Range 00-23
	#!  Year1	    1	                YY1 (Higher Century Byte)  2-digit, BCD, Range 00-99
	#!  Year2	    1	                YY2 (Lower Century Byte)  2-digit, BCD, Range 00-99
	#!  Month	    1	                MM  2-digit, BCD, Range 01-12
	#!  Date	    1	                DD  2-digit, BCD, Range 01-31
	#!  return a string of below:
	#!                  nHour + nMinute + nYear1 + nYear2 + nMonth + nDate
	def getUTCCommandTime_BCD(self,DL):
		MyTime = getDateTime()
		Hour = MyTime[3]
		nHour = int_to_bcd(int(Hour,10))
		Minute = MyTime[4]
		nMinute = int_to_bcd(int(Minute,10))
		Year1 = MyTime[0][0:2]
		nYear1 = int_to_bcd(int(Year1,10))
		Year2 = MyTime[0][2:4]
		nYear2 = int_to_bcd(int(Year2,10))
		Month = MyTime[1]
		nMonth = int_to_bcd(int(Month,10))
		Date = MyTime[2]
		nDate = int_to_bcd(int(Date,10))
		print (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)
		return (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)

	def  MasterReset(self,DL):
		Result = True
		DL.setText("GREEN", 'SMFG Master Reset Prcess:')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		
		DL.SendIOCommand("IDG","91 08",3000)
		strResponse= DL.Get_RXResponse(0)
		Result = DL.Check_RXResponse("91 00")
		if((Result == False) or  len(strResponse) < 32):
			return Result
		strResponse = strResponse.replace(" ", "")
		strNonce = strResponse[28:len(strResponse) - 4]
		
		DL.SendIOCommand("IDG","1201",3000)
		strResponse=  DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) < 48):
			Result = False
			return Result
			
		strSN = DL.getASCIIArray(strResponse[28:48])
		signeddata= DL.signMFGCommand(strNonce, '91', '00', strSN)
		command=signeddata
		DL.SendIOCommand("IDG",command,3000)
		Result =  DL.Check_RXResponse("91 00")
		if(Result == False):
			return Result
			
		DL.SendIOCommand("IDG","90 07 01",3000)
		Result =  DL.Check_RXResponse("90 00")
		time.sleep(2)
		return Result

	def Activate(self,DL):
		Result = True
		DL.SendIOCommand("IDG","2900",3000)
		Ver = DL.Get_RXResponse(0)
		Ver = Ver.replace(" ", "")
		if(len(Ver) < 76):
			Result = False
			return Result
			
		Ver = Ver[68:76]
		DL.setText("GREEN", 'Do UMFG Activating Prcess:')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
			
		DL.SendIOCommand("IDG","90 00",5000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
			
		DL.SendIOCommand("IDG","1201",3000)
		strResponse= DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) < 48):
			Result = False
			return Result
		strSN = DL.getASCIIArray(strResponse[28:48])
		DL.setText("GREEN", 'SN:' + strSN)
		
		mytime = getUTCCommandTime_BCD()
		DL.setText("BLACK", mytime)
		command='9001'+mytime
		DL.SendIOCommand("IDG",command,3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
			
		time.sleep(5)
		DL.SendIOCommand("IDG","90 02",80000)
		Result = DL.Check_RXResponse("90 00")
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
#		if(226 > int(DL.getASCIIArray(Ver))):
#			DL.setText("RED", '[a]')
#			strCerFromDevice = strResponse[28:len(strResponse) - 4]
#		else:
#			DL.setText("RED", '[b]')
		if((Result == False) or  len(strResponse) < 32):
			return Result
			
		strCerFromDevice = strResponse[28:len(strResponse) - 4]
		DL.setText("GREEN", strCerFromDevice)
		time.sleep(2)
		Result = DL.LoadCerts("90 03", strCerFromDevice, strSN)
		if(Result == False):
			return Result

		time.sleep(1)
		DL.SendIOCommand("IDG","90 04",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		time.sleep(1)
#		DL.SendIOCommand("IDG","90 16 30",5000)
#		Result = DL.Check_RXResponse("90 00")
#		time.sleep(1)
		DL.SendIOCommand("IDG","90 05",5000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		time.sleep(1)
		DL.SendIOCommand("IDG","90 07 01",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		DL.SendIOCommand("IDG","18 01",3000)
		Result = DL.Check_RXResponse("18 00")
		time.sleep(2)
		return Result


	def EnsureActive(self,DL):
		DL.setText("GREEN", 'Do UMFG Activating Prcess:')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		DL.SendIOCommand("IDG","90 00",5000)
		Result = DL.Check_RXResponse("90 2A")
		if(Result==False):
			Result = Pro_PKI().MasterReset(DL)
			Result = Pro_PKI().Activate(DL)
		else:
			DL.SendIOCommand("IDG","90 07 01",3000)
			Result = DL.Check_RXResponse("90 00")
		time.sleep(2)
		return Result



	def DeleteAllKeys(self,DL):
		Result = True
		DL.setText("GREEN", 'SMFG Delete All Keys Prcess:')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
		DL.SendIOCommand("IDG","91 08",3000)
		strResponse= DL.Get_RXResponse(0)
		Result = DL.Check_RXResponse("91 00")
		strResponse = strResponse.replace(" ", "")
		if((Result == False) or  len(strResponse) < 32):
			return Result
		strNonce = strResponse[28:len(strResponse) - 4]
		DL.SendIOCommand("IDG","1201",3000)
		strResponse= DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) < 48):
			return Result
		strSN = DL.getASCIIArray(strResponse[28:48])
		signeddata=DL.signMFGCommand(strNonce, '91', '09', strSN)
		if(signeddata != ''):
			command=signeddata
			DL.SendIOCommand("IDG",command,2000)
			Result = DL.Check_RXResponse("91 00")
			if(Result == False):
				return Result
			DL.SendIOCommand("IDG","90 07 01",3000)
			Result = DL.Check_RXResponse("90 00")
		else:
			Result = False
		return Result

	def GetDeviceNonce(self,DL):
		DL.SendIOCommand("IDG","91 08",3000)
		strResponse= DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ","")
		if(strResponse.find("9100") != -1):
			strNonce = strResponse[28:len(strResponse) - 4]
			DL.setText("GREEN", 'Get NONCE Success:[' + strNonce + ']')
			return strNonce
		else:
			ErrorCode = strResponse[22:24]
			DL.setText("RED", 'Get NONCE Fail')
			return "Error:" + ErrorCode

	def SecureTask(self,Flag,DL):
		if(Flag):
			DL.SendIOCommand("IDG","90 07 00",30000)
		else:
			DL.SendIOCommand("IDG","90 07 01",30000)
		return DL.Check_RXResponse("90 00")

	def ReadyforActivated(self,DL):
		if (False == Pro_PKI().SecureTask(True,DL)):
			return False
		DL.SendIOCommand("IDG", "90 00", 5000) #Device Reset
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		
		ErrorCode = strResponse[22:24]
		DL.setText("GREEN", 'UMFG Reset Responsecode:' + ErrorCode)
		if (False ==  Pro_PKI().SecureTask(False,DL)): 
			return False
		if (ErrorCode == '12') | (ErrorCode == '2A'):
			DL.setText("BLACK", "SMFG Mode")
			return True
		if (ErrorCode == '00'):
			if(True == Pro_PKI().Activate(DL)):
				DL.setText("GREEN", "Activate Device to UMFG enable mode")
				return True
			else:
				return False

	def ReadyforDeactivated(self,DL):
		if (False == Pro_PKI().SecureTask(True,DL)):return False
		DL.SendIOCommand("IDG", "90 00", 5000) #Device Reset
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		ErrorCode = strResponse[22:24]
		DL.setText("GREEN", 'UMFG Reset Responsecode:' + ErrorCode)
		if (ErrorCode == '12') | (ErrorCode == '2A'):
			DL.setText("GREEN", str(Pro_PKI().MasterReset(DL)))
			time.sleep(1)
			return True
		if (ErrorCode == '00'):
			if (False ==  Pro_PKI().SecureTask(False,DL)): 
				return False
			else:
				return True

	def WhiteList(self,WhiteList,DL):
		Result = True
		DL.setText("GREEN", 'Set white list')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
			
		DL.SendIOCommand("IDG","91 08",3000)
		strResponse= DL.Get_RXResponse(0)
		Result = DL.Check_RXResponse("91 00")
		strResponse = strResponse.replace(" ", "")
		if((Result == False) or len(strResponse) < 48):
			return Result
		strNonce = strResponse[28:48]
		DL.SendIOCommand("IDG","1201",3000)
		strResponse=  DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) < 48):
			return Result
		strSN = DL.getASCIIArray(strResponse[28:48])
		signeddata= DL.signMFGCommand(strNonce, '91', '13',strSN, WhiteList)
		if(signeddata != ''):
			command=signeddata
			DL.SendIOCommand("IDG",command,2000)
			Result =  DL.Check_RXResponse("91 00")
			if(Result == False):
				return Result
				
			DL.SendIOCommand("IDG","90 07 01",3000)
			Result =  DL.Check_RXResponse("90 00")
		else:
			Result = False
		return Result
		
	def ClearWL(self,DL):
		Result = True
		DL.setText("GREEN", 'Clear white list')
		DL.SendIOCommand("IDG","90 07 00",3000)
		Result = DL.Check_RXResponse("90 00")
		if(Result == False):
			return Result
			
		DL.SendIOCommand("IDG","91 08",3000)
		strResponse= DL.Get_RXResponse(0)
		Result = DL.Check_RXResponse("91 00")
		strResponse = strResponse.replace(" ", "")
		if((Result == False) or len(strResponse) < 32):
			return Result
		strNonce = strResponse[28:len(strResponse) - 4]
		DL.SendIOCommand("IDG","1201",3000)
		strResponse=  DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(len(strResponse) < 42):
			return Result
		strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 14])
		signeddata= DL.signMFGCommand(strNonce, '91', '14',strSN)
		if(signeddata != ''):
			command=signeddata
			DL.SendIOCommand("IDG",command,2000)
			Result =  DL.Check_RXResponse("91 00")
			if(Result == False):
				return Result
			DL.SendIOCommand("IDG","90 07 01",3000)
			Result =  DL.Check_RXResponse("90 00")
		else:
			Result = False
		return Result