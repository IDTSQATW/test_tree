#Pro_Transaction Py - Command Exchange
import sys
import time
import System
class Tra_Type_1:
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Active transaction 02-40' + Smsg + '\n'
		strRunTest = strRunTest + 'CMD:02 40 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:02\n'
		strRunTest = strRunTest + 'ROBOT:REMOVECARD' + '\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		#DL.SetWindowText("BLACK",strRunTest)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(0.01)#
			strResponse = strResponse.replace(" ", "")
			return strResponse

	#Not remove card after transaction
	def Run_1(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Active transaction 02-40' + Smsg + '\n'
		strRunTest = strRunTest + 'CMD:02 40 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:02\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		#DL.SetWindowText('Black',"Active transaction 02-40")
		#DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class Tra_Type_2:
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Active transaction 02-01' + Smsg + '\n'
		strRunTest = strRunTest + 'CMD:02 01 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:02\n'
		strRunTest = strRunTest + 'ROBOT:REMOVECARD' + '\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		#DL.SetWindowText('Black',"Active transaction 02-40")
		#DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class Tra_Type_3:
	Notification_CardComingt=""
	CardData=""
	Notification_CardLeavingt=""

	
	def Run(self,cardnumber,Robot,Burst,One,Timeout,DL):
		self.Notification_CardComingt=""
		self.CardData=""
		self.Notification_CardLeavingt=""


		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card", 'Please Tap the Card Number is' + str(cardnumber), Timeout)
			else:
				DL.Robot_SwipeorTapCard(cardnumber)
			
			while(True):
				if(bRet):
					self.Notification_CardComing = DL.GetResponse()
					if(self.Notification_CardComing != ""):
						DL.SetWindowText("green",'Card Coming Notification:' + self.Notification_CardComing)
						break
					time.sleep(0.1)
				else:
					DL.SetWindowText('RED', 'Device Open Failed!')
					break
					
			if(Burst == True):
				while(True):
					self.CardData= DL.GetResponse()
					if(self.CardData != ""):
						DL.SetWindowText("green",'Card Data: ' + self.CardData)
						break
					time.sleep(0.1)

			bRet = DL.Robot_RemoveCard()
			if(One == True):
				while(True):
					self.Notification_CardLeaving = DL.GetResponse()
					if(self.Notification_CardLeaving != ""):
						DL.SetWindowText("green",'Card Leaving Notification: ' + self.Notification_CardLeaving)
						break
					time.sleep(0.1)

			bRet = DL.CloseDevice()

	def GetNotificationCardComing(self):
		return self.Notification_CardComing
		
	def GetCardData(self):
		return self.CardData
		
	def GetNotificationCardLeaving(self):
		return self.Notification_CardLeaving

class Tra_Type_4: # 0240 MSR swipe //Borg 10/31
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Robot,Timeout,Interval,DL):
		Reslist = []
		if(Robot == False):
			DL.ShowMessageBox("Swipe MSR Card", Smsg, 1000)
			DL.SetWindowText('Black',"Swipe MSR Card ...")
		else:
			DL.SetWindowText('Black',"Robot not ready")
			Reslist.append("Error: MSR Robot N/I")
			return Reslist
		DL.SetWindowText('Black',"Active transaction 02-40")
		DL.SetWindowText('Black', Smsg)
		SCMD = "0240" + Para
		DL.SendIOCommand("IDG",SCMD,Timeout,ResIndex)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			Reslist.append(strResponse)
		return Reslist

class Tra_Type_5: #  //2019/1/29 Vivian
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,cardnumber,Robot,Timeout,Interval,DL):
		Reslist = []
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		else:
			DL.Robot_SwipeorTapCard(cardnumber)
		SCMD = "0240" + Para
		DL.SendIOCommand("IDG",SCMD,Timeout,ResIndex)
		DL.Robot_RemoveCard()
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			Reslist.append(strResponse)
		return Reslist


class Tra_Type_6: #  //2019/1/29 Vivian
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,cardnumber,Robot,Timeout,Interval,DL):
		Reslist = []
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		else:
			DL.Robot_SwipeorTapCard(cardnumber)
		SCMD = "0240" + Para
		DL.SendIOCommand("IDG",SCMD,Timeout,ResIndex)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			Reslist.append(strResponse)
		return Reslist

class Tra_Type_7:#  //2019/3/05 Vivian
	CardData = []

	
	def Run(self,cardnumber,Robot,Burst,One,Timeout,DL):
		self.CardData = []
		
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card", 'Please Tap the Card Number is' + str(cardnumber), Timeout)
			else:
				DL.Robot_SwipeorTapCard(cardnumber)

			
		if(Burst == True):
			N = 0
			while(DL.bIsStopRun == False):
				strResponse = DL.GetResponse()
				if(strResponse != ""):
					N = 0
					DL.SetWindowText("green",'Card Data: ' + strResponse)
					self.CardData.append(strResponse)
					if(len(self.CardData) > 1):
						break
				else:
					N = N + 1
					if(N > 5):
						break
				time.sleep(0.1)

		#bRet = DL.Robot_RemoveCard()

	def GetCardData(self):
		return self.CardData



class Tra_Type_8:#  //2019/3/05 Vivian
	CardData = []

	
	def Run(self,cardnumber,Robot,Burst,One,Timeout,DL):
		self.CardData = []
		
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card", 'Please Tap the Card Number is' + str(cardnumber), Timeout)
			else:
				DL.Robot_SwipeorTapCard(cardnumber)

			
		if(Burst == True):
			N = 0
			while(DL.bIsStopRun == False):
				strResponse = DL.GetResponse()
				if(strResponse != ""):
					N = 0
					DL.SetWindowText("green",'Card Data: ' + strResponse)
					self.CardData.append(strResponse)
#					if(len(self.CardData) > 6):
#						break
				else:
					N = N + 1
					if(N > 5):
						break
				time.sleep(0.1)

		#bRet = DL.Robot_RemoveCard()

	def GetCardData(self):
		return self.CardData


class Tra_Type_9: #  //2019/3/05 Vivian
	#Smsg - info
	#ResIndex - read response times
	def Run(self,Smsg,ResIndex,SCMD,Timeout,Interval,DL):
		Reslist = []
		DL.SendIOCommand("IDG",SCMD,Timeout,ResIndex)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			Reslist.append(strResponse)
		return Reslist


		
class P4T_Type_1:
#Tap card, not remove
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Poll for token\n'
		strRunTest = strRunTest + 'CMD:2C 02 ' + Para +'\n'
		strRunTest = strRunTest + Action + 'CM0\n'
		strRunTest = strRunTest + 'EXR:2C\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		DL.SetWindowText('Black',"Poll for token 2C-02")
		DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class P4T_Type_2:
#Tap card, remove after response
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Poll for token\n'
		strRunTest = strRunTest + 'CMD:2C 02 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:2C\n'
		strRunTest = strRunTest + 'ROBOT:REMOVECARD' + '\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		DL.SetWindowText('Black',"Poll for token 2C-02")
		DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class P4T_Type_3:
#Tap card, remove after response
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Poll for token\n'
		strRunTest = strRunTest + 'CMD:2C 0C ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:2C\n'
		strRunTest = strRunTest + 'ROBOT:REMOVECARD' + '\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		DL.SetWindowText('Black',"Poll for token 2C-0C")
		DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class P4T2C40_Type_1:
#Tap card, not remove
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Poll for token\n'
		strRunTest = strRunTest + 'CMD:2C 40 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:2C\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		DL.SetWindowText('Black',"Poll for token 2C-40")
		DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class P4T2C40_Type_2:
#Tap card, remove
	#Smsg - info
	#ResIndex - read response times
	#Para - 0240 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Action,Robot,Timeout,Interval,DL):
		if(Robot == False):
			DL.ShowMessageBox("Poll Card", Smsg, Timeout)
		strRunTest = 'TID:Poll for token\n'
		strRunTest = strRunTest + 'CMD:2C 40 ' + Para +'\n'
		strRunTest = strRunTest + Action + '\n'
		strRunTest = strRunTest + 'EXR:2C\n'
		strRunTest = strRunTest + 'ROBOT:REMOVECARD' + '\n'
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		DL.RunTest(strRunTest)
		DL.SetWindowText('Black',"Poll for token 2C-40")
		DL.SetWindowText('Black', Smsg)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			return strResponse

class  MPE8341_Type_1:# 83 41 Manual PAN Entry //Borg 10/31
	#Smsg - info
	#ResIndex - read response times
	#Para - 8341 paramaters
	#Robot - Robot txt command
	#Timeout - Timeout for 1st Res
	#Interval - interval gap timing with 2 ResIndex
	def Run(self,Smsg,ResIndex,Para,Robot,Timeout,Interval,DL):
		Reslist = []
		if(Robot == False):
			DL.ShowMessageBox("Manual PAN Entry", Smsg, 3000)
			DL.SetWindowText('Black',Smsg)
		else:
			DL.SetWindowText('Black',"Robot not ready")
			Reslist.append("Error: MSR Robot N/I")
			return Reslist
		SCMD = "8341" + Para
		DL.SendIOCommand("IDG",SCMD,Timeout)
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			Reslist.append(strResponse)
		return Reslist
		
		
class Tra_Type_Auto:#Auto receive 
#ResIndex: response number for receiving
#msg: Box message when manual
#Cardnumber: card number
#Robot: whether auto test
#Timeout: timeout
#Run : tap card, auto receive, remove card at the end
	def Run(self,ResIndex,msg,cardnumber,Robot,Timeout,DL):
		listResponse = []
		index = 0
		Data = ""
		strSRes = ""
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card", msg, 0)
			else:
				DL.Robot_SwipeorTapCard(cardnumber)
			#starttime=
			while(True):
				Data = DL.GetResponse()
				Data = Data.replace(" ", "")
				if(Data != ""):
					DL.SetWindowText("BLUE",'REsponse Data: ' + Data)
					index = index + 1
					listResponse.append(Data)
					if(index == ResIndex): break
				time.sleep(0.1)	
			bRet = DL.Robot_RemoveCard()
			bRet = DL.CloseDevice()
			return listResponse
			
#Run_1 : tap card, auto receive, not remove card at the end
	def Run_1(self,ResIndex,msg,cardnumber,Robot,Timeout,DL):
		listResponse = []
		index = 0
		Data = ""
		strSRes = ""
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card", msg, 0)
			else:
				DL.Robot_SwipeorTapCard(cardnumber)
			#starttime=
			while(True):
				Data = DL.GetResponse()
				Data = Data.replace(" ", "")
				if(Data != ""):
					DL.SetWindowText("BLUE",'REsponse Data: ' + Data)
					index = index + 1
					listResponse.append(Data)
					if(index == ResIndex): break
				time.sleep(0.1)	
			bRet = DL.CloseDevice()
			#return listResponse
			for index in range(0,ResIndex):
				strResponse = listResponse[index]
				return strResponse



#Run_2 : remove card, auto receive
	def Run_2(self,ResIndex,Robot,Timeout,DL):
		listResponse = []
		index = 0
		Data = ""
		strSRes = ""
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				DL.ShowMessageBox("Poll Card","Remove card after clicking", 0)
			else:
				DL.Robot_RemoveCard()
			#starttime=
			while(True):
				Data = DL.GetResponse()
				Data = Data.replace(" ", "")
				if(Data != ""):
					DL.SetWindowText("BLUE",'REsponse Data: ' + Data)
					index = index + 1
					listResponse.append(Data)
					if(index == ResIndex): break
				time.sleep(0.1)	
			bRet = DL.CloseDevice()
			return listResponse			
	
#Run_3 : no robot, auto receive
	def Run_3(self,ResIndex,MesPre,Message,Robot,Timeout,DL):
		listResponse = []
		index = 0
		Data = ""
		strSRes = ""
		bRet = DL.OpenDevice()
		if(bRet):
			if(Robot == False):
				if(MesPre == True):
					DL.ShowMessageBox("Message",Message, 5000)
			#starttime=
			while(True):
				Data = DL.GetResponse()
				Data = Data.replace(" ", "")
				if(Data != ""):
					DL.SetWindowText("BLUE",'REsponse Data: ' + Data)
					index = index + 1
					listResponse.append(Data)
					if(index == ResIndex): break
				time.sleep(0.1)	
			bRet = DL.CloseDevice()
			return listResponse			
					

