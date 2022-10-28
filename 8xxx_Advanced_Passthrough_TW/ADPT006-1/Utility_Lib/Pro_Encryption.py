#Pro_Encryption py
import sys
import time
import System

class Pro_Encryption:     
    #ifSW:SW12 Present; ifMAC:MAC verfication on
	#DATAORPIN:0=data,1=pin variant; EncryptMode:1=TDES,2=AES128
	def DecRAPDU(self,strRes,strKey,DATAORPIN,EncryptMode,ifSW,ifMAC,EXRAPDU,DL):
		DL.setText("BLUE","===Decrypt RAPDU===")
		strRes = strRes.replace(" ","")
		strRes = strRes[28:len(strRes)-4]
		if(strRes==""):
			DL.fails=DL.fails+1
			DL.setText("RED","Response not contain APDU!")
			listDecRAPDU = ["00000000000000000000","",""]
			return listDecRAPDU
		else:	
			LenRAPDU = int(strRes[0:4],16)
			strRAPDU = strRes[4:4+2*LenRAPDU]
			DL.setText("BLUE","Encrypted RAPDU: "+strRAPDU)
			if(ifSW):strRes1 = strRes[4+2*LenRAPDU+4:]
			else:strRes1 = strRes[4+2*LenRAPDU:]
			LenKSN = int(strRes1[0:4],16)
			strKSN = strRes1[4:4+2*LenKSN]
			DL.setText("BLUE","KSN: "+strKSN)
			DecRAPDU = DL.DecryptDLL(DATAORPIN,EncryptMode,strKey,strKSN,strRAPDU)
			if(False==DL.CompareString(DecRAPDU,EXRAPDU)):
				DL.fails=DL.fails+1
				DL.setText("RED","RAPDU encryption wrong, should be: "+EXRAPDU)
			if(ifMAC):
				DL.setText("BLUE","===Check RAPDU MAC===")
				strRes2 = strRes1[4+2*LenKSN:]
				LenMAC = int(strRes2[0:4],16)
				ReaderMAC = strRes2[4:4+2*LenKSN]
				MACstring = strRes[:len(strRes)-2*LenMAC]
				DL.setText("BLUE","ReaderMAC: "+ReaderMAC)
				ActualMAC = DL.CalcMacValueAlgrithm(strKSN, strKey, MACstring)
				if(False==DL.CompareString(ActualMAC,ReaderMAC)):
					DL.fails=DL.fails+1
					DL.setText("RED","MAC wrong, MAC calculated: "+ActualMAC)
			else:ReaderMAC=""
			listDecRAPDU = [strKSN,DecRAPDU,ReaderMAC]
			return listDecRAPDU
            
    