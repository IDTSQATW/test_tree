#Pro_SendCmd Py - Command Exchange
import sys
import time
import System
class Pro_SendCmd:
	#Smsg - info
	#Scmd - CMD IN
	#Timeout - Timeout for 1st Res
	#IfAscii - Response Ascii or not
	def Run(self,Smsg,Scmd,Timeout,IfAscii,DL):
		DL.SetWindowText('Black',Smsg)
		DL.SendIOCommand("IDG", Scmd, Timeout)
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(IfAscii):
			return strResponse[28:len(strResponse)-4]
		else:
			return strResponse
	
	#Smsg - info
	#Resindex - get response times
	#Scmd - CMD IN
	#Timeout - Timeout for 1st Res
	#interval - gap timing between 2 times res
	def Run_1(self,ResIndex,Smsg,Scmd,Timeout,Interval,DL):
		DL.SetWindowText('Black',Smsg)
		DL.SendIOCommand("IDG", Scmd, Timeout,ResIndex)
		listResponse = []
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			listResponse.append(strResponse)
		return  listResponse
	#Pro - Protocol exp IDG/RAWIDG
	#Smsg - info
	#Resindex - get response times
	#Scmd - CMD IN
	#Timeout - Timeout for 1st Res
	#interval - gap timing between 2 times res
	def Run_2(self,Pro,ResIndex,Smsg,Scmd,Timeout,Interval,DL):
		DL.SetWindowText('Black',Smsg)
		DL.SendIOCommand(Pro, Scmd, Timeout, ResIndex)
		listResponse = []
		for index in range(0,ResIndex):
			strResponse = DL.Get_RXResponse(index)
			time.sleep(Interval/1000)
			strResponse = strResponse.replace(" ", "")
			listResponse.append(strResponse)
		return  listResponse



	def Run_Raw(self,Smsg,Scmd,Timeout,IfAscii,DL):
		DL.SetWindowText('Black',Smsg)
		DL.SendIOCommand("RAWIDG", Scmd, Timeout)
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(IfAscii):
			return strResponse[28:len(strResponse)-4]
		else:
			return strResponse						

	#Run_3: use for adding parameter in the end of command	
	def Run_3(self,Smsg,Scmd,Spara,Timeout,IfAscii,DL):
		DL.SetWindowText('Black',Smsg)
		DL.SendIOCommand("IDG", Scmd + Spara, Timeout)
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		if(IfAscii):
			return strResponse[28:len(strResponse)-4]
		else:
			return strResponse
	
	#Run_4: SMFG sign command
	#Smsg - info
	#strNonce - get SMFG device Nonce
	#Resindex - get response times
	#Scmd - CMD IN
	#strSerialN - Device SerialNumber
	#Timeout - Timeout for 1st Res
	#IfAscii - Response Ascii or not
	def Run_4(self,Smsg,strNonce,strSerialN,Scmd,Timeout,IfAscii,DL):
		DL.SetWindowText('Black',Smsg)
		Scmd  = Scmd.replace(" ", "")
		if(len(Scmd)<4):
			return "Error: Command Len Fail"
		SSCMD = Scmd[0:2]
		SSubCMD = Scmd[2:4]
		SOther = Scmd[4:len(Scmd)]
		strSignedCommandData = DL.signMFGCommand(strNonce, SSCMD, SSubCMD,strSerialN, SOther)
		#DL.SetWindowText("RED",strSignedCommandData)
		if (strSignedCommandData != ""):
			DL.SendIOCommand("IDG", strSignedCommandData, Timeout)
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			if(IfAscii):
				return strResponse[28:len(strResponse)-4]
			else:
				return strResponse
		else:
			return "Error: signMFGCommand Fail"
            


##### Check result #####
#1 response, 1 expected response related
	def RunCK(self,In,Out,DL):
		Result=DL.Check_RXResponse(0,Out,True)
		#DL.setText("BLACK",In)
		if(Result):
			DL.setText("GREEN","EXR:"+Out)
			return True
		else:
			DL.setText("RED","FAIL")
			DL.setText("RED","EXR:" +Out)
			return False            

#more than 1 response, expected response related
	def RunCK_1(self,listIn,listOut,DL):
		if(len(listIn) != len(listOut)):
			return False
			DL.setText("RED","Please Check EXR")
		fail=0
		index =0
		while(index < len(listIn)):
			Result=DL.Check_RXResponse(index,str(listOut[index].replace(" ", "")),True) 
			#DL.setText("blue",listIn[index])
			if(Result==False):
				fail=fail+1
				DL.setText("RED","EXR: "+listOut[index])
			else:DL.setText("GREEN","EXR: "+listOut[index])
			index = index+1
		if(fail>0):
			return False
			DL.setText("RED","FAIL")
		else:return True

#more than 1 response, pass if one of the response contain expected item	
	def RunCK_2(self,listIn,Out,DL):
		success=0
		DL.setText("GREEN","EXR:"+Out)
		for  index in  range(0, len(listIn)):
			if (listIn[index].find(Out.replace(" ", ""))>=0):success=success+1
		if (success == 1): 
			DL.setText("GREEN","Test PASS")
			return True
		else: 
			DL.setText("RED","Test FAIL")
			return False	
 
#1 respose, more than 1 expected item
	def RunCK_3(self,In,listOut,DL):
		fail=0
		for  index in  range(0, len(listOut)):
			if (In.find(listOut[index].replace(" ", ""))==-1):
				fail=fail+1
				DL.setText("RED","Not find "+listOut[index])
			else:DL.setText("GREEN","Find "+listOut[index])
		if (fail == 0): 
			DL.setText("GREEN","Test PASS")
			return True
		else: 
			DL.setText("RED","Test FAIL")
			return False

#1 response, 1 expected response related, added by Lylia, 20.03.30
	def RunCK_C(self,In,Out,DL):
		Result=DL.CompareString(In,Out)
		#DL.setText("BLACK",In)
		if(Result):
			DL.setText("GREEN","EXR:"+Out)
			return True
		else:
			DL.setText("RED","FAIL")
			DL.setText("RED","EXR:" +Out)
			return False            