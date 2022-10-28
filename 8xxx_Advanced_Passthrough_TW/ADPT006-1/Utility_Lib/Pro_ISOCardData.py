#Pro_ISOCardData.Py - Parse Card Data
import sys
import time
import System 

class MSRData:
	
	def ISOCreditCard(self,DL):
		DL.SetWindowText("BLUE", sResult)
		if sResult!=None and sResult!="":
		    sResult=sResult.replace(" ","")
		    sResult=sResult[30:len(sResult)-4]
		    DL.SetWindowText("BLUE", sResult)
		    CardData=DL.GetTLV(sResult,"DFEE23")
		    bresult = False
		    if CardData!=None and CardData!='':
		        objectMSR = DL.ParseCardData(CardData,bresult,"0123456789ABCDEFFEDCBA9876543210","0123456789ABCDEFFEDCBA9876543210")
		        if objectMSR!=None:
		            #msrdecode = '\n'.join(['%s:%s' % item for item in objectMSR.__dict__.items()])
		            DL.SetWindowText("blue",str(objectMSR[0].msr_cardType))
		            #if DL.ParseCardData(CardData,Key):
		            #DL.SetWindowText("GREEN", "Parse Card Data PASS")
		            #CardType=DL.GetCardEncodeType()


		            EncryptType = DL.Get_EncryptionKeyType_CardData()
		            EncryptMode = DL.Get_EncryptionMode_CardData()

		            Track1_CardData = DL.Get_TrackN_CardData(1)
		            Track2_CardData = DL.Get_TrackN_CardData(2)
		            Track3_CardData = DL.Get_TrackN_CardData(3)
		            if str(objectMSR[0].msr_cardType)=="CAPTURE_ENCODE_TYPE_ISOABA":
		                if(Track1_CardData!=""):
		                    DL.SetWindowText("blue", Track1_CardData)
		                    #Track1_CardData = DL.getASCIIArray(Track1_CardData)
		                    pattern = re.compile(r'\%\*[0-9]{4}\**[0-9]{4}\^[a-zA-Z0-9]*\s[a-zA-Z0-9]*\-[a-zA-Z0-9]*\s\^[0-9]{4}\**\?\*$')
		                    Match("Track1_CardData", pattern, Track1_CardData)
		                if (Track2_CardData != ""):
		                    DL.SetWindowText("blue", Track2_CardData)
		                    #Track2_CardData = DL.getASCIIArray(Track2_CardData)
		                    pattern = re.compile(r'^\;[0-9]{4}\**[0-9]{4}\=[0-9]{4}\**\?\*$')
		                    Match("Track2_CardData", pattern, Track2_CardData)
		                if (Track3_CardData != ""):
		                    DL.SetWindowText("blue", Track3_CardData)
		                    #Track3_CardData = DL.getASCIIArray(Track3_CardData)
		                    pattern = re.compile(r'^\;[0-9]{6}\**[0-9]{4}\=\**\?\*$')
		                    Match("Track3_CardData", pattern, Track3_CardData)

		                PAN = DL.Get_PAN_CardData()
		                if PAN!='':
		                    pattern = re.compile(r'^[0-9]{12,19}$')
		                    Match("PAN", pattern, PAN)

		                TRK1 = DL.Get_EncryptTrackN_CardData(1)
		                TRK2 = DL.Get_EncryptTrackN_CardData(2)
		                TRK3 = DL.Get_EncryptTrackN_CardData(3)
		                KSN=DL.Get_KSN_CardData()
 

		                if len(TRK1)>0:
		                    TRK1DencryptData=DL.DecryptDLL( EncryptType,EncryptMode , Key ,KSN ,TRK1 )
		                    if(TRK1DencryptData!=''):
		                        TRK1DencryptData = DL.getASCIIArray(TRK1DencryptData[0:objectMSR[0].msr_track1Length*2])
		                        DL.SetWindowText("blue", TRK1DencryptData)
		                        #TRK1DencryptData = '%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?.'
		                        pattern = re.compile(r'^\%B[0-9]{12,19}\^[a-zA-Z0-9]*\s[a-zA-Z0-9]*\-[a-zA-Z0-9]*\s\^[0-9]*\?.*$')
		                        Match("TRK1DencryptData:", pattern, TRK1DencryptData)


		                if len(TRK2) > 0:
		                    TRK2DencryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
		                    if(TRK2DencryptData!=''):
		                        TRK2DencryptData = DL.getASCIIArray(TRK2DencryptData[0:objectMSR[0].msr_track2Length * 2])
		                        DL.SetWindowText("blue", TRK2DencryptData)
		                        #;4547570001070000=1102101000003060000?8
		                        pattern = re.compile(r'^\;[0-9]{12,19}\=[0-9]*\?.*$')
		                        Match("TRK2DencryptData", pattern, TRK2DencryptData)


		                if len(TRK3) > 0:
		                    TRK3DencryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
		                    if (TRK3DencryptData != ''):
		                        TRK3DencryptData = DL.getASCIIArray(TRK3DencryptData[0:objectMSR[0].msr_track3Length * 2])
		                        DL.SetWindowText("blue", TRK3DencryptData)
		                        #;014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?5
		                        pattern = re.compile(r'^\;[0-9]{12,19}\=[0-9]*\=[0-9]*\={2}[0-9]{1}\=[0-9]*\?.*$')
		                        Match("TRK3DencryptData", pattern, TRK3DencryptData)

		        else:
		            DL.SetWindowText("RED", "Parse Card Data FAIL")