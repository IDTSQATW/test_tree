#Pro_Excuse Py - excuse original txt format
#import Pro_PreFile
#from  Pro_PreFile import *
#import Utility_Lib.Pro_MSRData 
#from  Utility_Lib.Pro_MSRData import *

class cardFiled:
	cardType = 0x80;
	track1MaskData = "";
	track2MaskData = "";
	track3MaskData = "";
	track1ClearData = "";
	track2ClearData = "";
	track3ClearData = "";
	track1EncrytionData = "";
	track2EncrytionData = "";
	track3EncrytionData = "";

class Pro_MSR:			
	def StartSwipeAndPrase(self,DL):
		bresult = False
		CardData=DL.getHIDITPCardData(20000)
		#DL.setText("BLUE", "Card Data:"+strCardData):
		if(CardData != None and CardData != ''):
			object = DL.ParseCardData(CardData, bresult, "0123456789ABCDEFFEDCBA9876543210","0123456789ABCDEFFEDCBA9876543210");
			return  object;
		else:
			return None;
	
	def CheckOtherFiled(self,objectMSR,DL):
		if objectMSR != None:
			EncryptType = DL.Get_EncryptionKeyType_CardData()
			EncryptMode = DL.Get_EncryptionMode_CardData()
			cardType=objectMSR[0].msr_cardType;


	def CheckMask(self,objectMSR ,cardFiled,DL):
		DL.SetWindowText("blue", "I am here")
		if objectMSR == None:
			return False;
		else:
			DL.SetWindowText("blue", str(objectMSR[0].msr_cardType))
			Track1_CardData = DL.Get_TrackN_CardData(1)
			Track2_CardData = DL.Get_TrackN_CardData(2)
			Track3_CardData = DL.Get_TrackN_CardData(3)
			DL.SetWindowText("Blue","Myprint:")
			DL.SetWindowText("Blue",Track1_CardData);
			DL.SetWindowText("Blue",cardFiled.track1MaskData);
			if (Track1_CardData != ""):
				if(Track1_CardData!=cardFiled.track1MaskData):
					DL.SetWindowText("RED","Track1 mask data fail");
					return False;

			if (Track2_CardData != ""):
				DL.SetWindowText("Blue",Track2_CardData);
				DL.SetWindowText("Blue",cardFiled.track2MaskData);
				if(Track2_CardData!=cardFiled.track2MaskData):
					DL.SetWindowText("RED", "Track2 mask data fail");
					return False;

			if (Track3_CardData != ""):
				DL.SetWindowText("Blue",Track3_CardData);
				DL.SetWindowText("Blue",cardFiled.track3MaskData);
				if(Track3_CardData!=cardFiled.track3MaskData):
					DL.SetWindowText("RED","Track3 mask data fail");
					return False;
			return True;


	def CheckDEncrypted(self,objectMSR ,cardFiled,DL):
		if objectMSR == None:
			return False
		else:
			DL.SetWindowText("blue", str(objectMSR[0].msr_cardType))
			TRK1 = DL.Get_EncryptTrackN_CardData(1)
			TRK2 = DL.Get_EncryptTrackN_CardData(2)
			TRK3 = DL.Get_EncryptTrackN_CardData(3)
			KSN = DL.Get_KSN_CardData();
			EncryptType = DL.Get_EncryptionKeyType_CardData()
			EncryptMode = DL.Get_EncryptionMode_CardData()
			if len(TRK1) > 0:
				TRK1DencryptData = DL.Get_DecryptTrackN_CardData(1);
				if (TRK1DencryptData != ''):
					TRK1DencryptData = DL.getASCIIArray(TRK1DencryptData[0:objectMSR[0].msr_track1Length * 2])
					DL.SetWindowText("Blue","Myprint:")
					DL.SetWindowText("Blue",TRK1DencryptData);
					DL.SetWindowText("Blue",cardFiled.track1ClearData);
					if(TRK1DencryptData!=cardFiled.track1ClearData):
						DL.SetWindowText("Blue","Track1 DeEncrption data fail");
						return False;

			if len(TRK2) > 0:
				TRK2DencryptData = DL.Get_DecryptTrackN_CardData(2);
				if (TRK2DencryptData != ''):
					DL.SetWindowText("Blue",TRK2DencryptData);
					DL.SetWindowText("Blue",cardFiled.track2ClearData)
					TRK2DencryptData = DL.getASCIIArray(TRK2DencryptData[0:objectMSR[0].msr_track2Length * 2])
					DL.SetWindowText("Blue",TRK2DencryptData);
					if(TRK2DencryptData!=cardFiled.track2ClearData):
						DL.SetWindowText("Red", "Track12 DeEncrption data fail");
						return False;

			if len(TRK3) > 0:
				TRK3DencryptData = DL.Get_DecryptTrackN_CardData(3);
				if (TRK3DencryptData != ''):
					DL.SetWindowText("Blue",TRK3DencryptData);
					DL.SetWindowText("Blue",cardFiled.track3ClearData)
					TRK3DencryptData = DL.getASCIIArray(TRK3DencryptData[0:objectMSR[0].msr_track3Length * 2]);
					DL.SetWindowText("Blue",TRK3DencryptData);
					if(TRK3DencryptData!=cardFiled.track3ClearData):
						DL.SetWindowText("Red","Track3 DeEncrption data fail");
						return False;
			return True;

 

	def SREDKEY2_MSR_Test(self,CardDataObject, CardType,DL):
		CardName=""
		if(CardType==0):CardName="NO.1 4909";
		elif(CardType==1):CardName="NO.2 AAMVA";
		elif(CardType==1):CardName="NO.3 Standard";
		DL.setText("BLUE", "Please swipe card " + CardName + "...")
		objectMSR=self.StartSwipeAndPrase(DL);
		if(objectMSR==None):
			return False;
		if(int(objectMSR[0].msr_cardType)==CardType):
			if(self.CheckMask(objectMSR,CardDataObject,DL)==False):
				return False;
			if(CardType==0):
				if(self.CheckDEncrypted(objectMSR,CardDataObject,DL)==False):
					return False;	
		return True




 

	#Smsg - info
	#Scmd - CMD IN
	#Timeout - Timeout for 1st Res
	#IfAscii - Response Ascii or not

	def NEOII_Card_Test(self,Smsg,Scmd,CardDataObject, CardType,Timeout,IfAscii,DL):
		self.DL=DL;
		DL.SetWindowText('Black',Smsg)
		CardName=""
		if(CardType==0):CardName="NO.1 4909";
		elif(CardType==1):CardName="NO.2 AAMVA";
		elif(CardType==1):CardName="NO.3 Standard";
		DL.setText("BLUE", "Please swipe card " + CardName + "...")
		DL.SendIOCommand("IDG", Scmd, Timeout)
		strResponse = DL.Get_RXResponse(0)
		strResponse = strResponse.replace(" ", "")
		DL.SetWindowText('Black',strResponse[42:len(strResponse)-4])
		MSRData=DL.GetTLV(strResponse[42:len(strResponse)-4],"DFEE23",0,True);
		DL.SetWindowText('Black',MSRData)
		objectMSR=DL.ParseCardData(MSRData,True,"0123456789ABCDEFFEDCBA9876543210","0123456789ABCDEFFEDCBA9876543210")
		if(objectMSR[1]==False):
			return False;
		if(int(objectMSR[0].msr_cardType)==CardType):
			DL.SetWindowText('Black',str(objectMSR))
			DL.SetWindowText('Black',str(objectMSR[1]))
			rep=self.CheckMask(objectMSR,CardDataObject,self.DL)
			if(rep==False):
				DL.SetWindowText('Black',str(int(objectMSR[0].msr_cardType)))
				DL.SetWindowText('Black',str(CardType))
				return False;
			if(CardType==0):
				if(self.CheckDEncrypted(objectMSR,CardDataObject,self.DL)==False):
					return False;	
		return True

