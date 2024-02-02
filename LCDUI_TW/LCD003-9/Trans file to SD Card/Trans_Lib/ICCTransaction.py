#Transaction for ICC Card
import sys
import time
import System
class ICCTransaction:
	#msg 			- info
	#Para 			- paramaters of command '60 10'
	#Action			- paramaters of robot action, valid only when isRobot=True
	#isRobot 		- is it a robot test
	#Timeout 		- Timeout for 1st Resp
	#Interval 		- interval gap timing with 2 RespCount
	#listExpResp 	- the expected response list
	
	def Run(self,msg,Para,Action,isRobot,Timeout,Interval,listExpResp,DL):
		if(isRobot == False):
			DL.ShowMessageBox("Insert ICC Card:", msg, Timeout)
		
		strRunTest = 'TID:ICC Transaction 60-10\n'
		strRunTest = strRunTest + 'CMD:' + Para +'\n'
		for index in range(0,len(listExpResp)):
			strRunTest = strRunTest +'EXR:' + listExpResp[index] + '\n'
		
		if(isRobot == True):	
			strRunTest = strRunTest + Action + '\n'
			
		strRunTest = strRunTest + 'TIMEOUT:' + str(Timeout) + '\n'
		strRunTest = strRunTest + 'PROTOCOL:IDG\n'
		
		DL.RunTest(strRunTest)
		DL.SetWindowText("BLACK",strRunTest)
		listRealResp = []
		for index in range(0,len(listExpResp)):
			strResponse = DL.Get_RXResponse(index)
			strResponse = strResponse.replace(" ", "")
			listRealResp.append(strResponse)
		return listRealResp
		
	def RunCK(self,listIn,listOut,DL):
		if(len(listIn) != len(listOut)):
			DL.SetWindowText('RED','The expect response number is not equal to the real response number.')
			return False
		index =0
		Result = True
		while(index < len(listIn)):
			Result=DL.Check_RXResponse(index,str(listOut[index].replace(" ", "")),True) and Result
			index = index+1
		return Result
	