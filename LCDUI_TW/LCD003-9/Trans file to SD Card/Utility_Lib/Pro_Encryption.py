#Pro_Encryption py
import sys
import time
import System

class Pro_Encryption:
	#MKSK DataKey+MKSK SesssionKey, 
	#Scmd1:before C0D0
	#Scmd2:after C0D0
	#TranRes:MKSK Encryption transaction response
	def GenMAC_1(self,Smsg,Scmd1,Scmd2,TranRes,Timeout,DL):
		self.DL = DL
		Result = True		
		self.DL.SendIOCommand("IDG", "63 06"+Scmd1+'C0 D0'+Scmd2, 30000)
		Result = self.DL.Check_RXResponse("63 00 00 08")
		#Get Generate MAC data, transfer to ASCII
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		str1 = strResponse[28:len(strResponse)-4] 
		strMAC = DL.getASCIIArray(str1)
		#Decrypt FOR DATA
		strKey = '22222222222222222222222222222222'#DataSessionKey
		strVector='0000000000000000'#Vector
		strDFEF4C=DL.GetTLV(TranRes,"DFEF4C")
		len1 = strDFEF4C[2:4]
		len1 = int(len1,16)*2
		strDFEF4D= DL.GetTLV(TranRes,"DFEF4D")
		strDeDFEF4D=DL.EncryptionDecryption_TDESCBC(1,1,strKey,strDFEF4D,strVector)
		strTRACK2 = strDeDFEF4D[4:len1+4]
		DL.setText('BLACK',strTRACK2)
		#Encry FOR Generate MAC data
		strKey='0123456789abcdeffedcba9876543210' #MACSessionKey
		strVector='0000000000000000'
		strData1 = Scmd1+strTRACK2+Scmd2
		strEnTrack=DL.EncryptionDecryption_TDESCBC(0,1,strKey,strData1,strVector)
		len2 = len(strEnTrack)-16
		strData3 = strEnTrack[len2:len(strEnTrack)]
		strData4 = strData3[0:8]
		DL.setText('BLACK',strData4)
		#Compare
		Result = DL.Check_StringAB(strData4,strMAC)
		return Result