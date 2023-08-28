#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
	time.sleep(1)
	
# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")
if (Result):
    RetOfStep = DL.SendCommand('DF7D = 02 (NEO2)')
    if (RetOfStep):
        Result = Result and DL.Check_RXResponse("04 00 00 00")

# Check reader is VP3350 or not
modeltype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if modeltype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Poll on Demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00")	

# cmd 02-40, swipe Discover card
if (Result):
	Result = DL.SendCommand('Activate Transaction')
	if (Result):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 4F 6A 00 00 A1 89 01 12")
		sResult=DL.Get_RXResponse(0)
		if Result == True:
			CardData=DL.GetTLV(sResult,"DFEE23",0,1)
			if CardData!=None and CardData!='':
				objectMSR = DL.ParseCardData(CardData,Key)
				EncryptType = DL.Get_EncryptionKeyType_CardData()
				EncryptMode = DL.Get_EncryptionMode_CardData()
				if objectMSR == True:     #Parse MSR data OK
					if len(DL.Get_EncryptTrackN_CardData(1))> 0:
						Track1_CardData = DL.Get_TrackN_CardData(1)
						TRK1DecryptData = DL.Get_DecryptTrackN_CardData(1)
					if len(DL.Get_EncryptTrackN_CardData(2))> 0:
						Track2_CardData = DL.Get_TrackN_CardData(2)
						TRK2DecryptData = DL.Get_DecryptTrackN_CardData(2)
					if len(DL.Get_EncryptTrackN_CardData(3)) > 0:
						Track3_CardData = DL.Get_TrackN_CardData(3)
						TRK3DecryptData = DL.Get_DecryptTrackN_CardData(3)
								
					# Verify specific tags
					if DL.Check_RXResponse("9F39 01 90") == False:
						DL.SetWindowText("red", "Tag9F39: FAIL")	
					if DL.Check_RXResponse("FFEE01 ** DFEE30010C") == False:
						DL.SetWindowText("red", "TagFFEE01: FAIL")	
					if DL.Check_RXResponse("DFEE26 02 EC06") == False:
						DL.SetWindowText("red", "TagDFEE26: FAIL")	

					# Transaction result verification
					TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?;6510********0026=1712****************?"
					TR1plaintextdata = "25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 5E 43 41 52 44 2F 49 4D 41 47 45 20 30 33 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 3B 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 3D 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F"
									
					Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
					if Result != True:
						DL.SetWindowText("red", "TR1maskdata: FAIL")
					Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
					if Result != True:
						DL.SetWindowText("red", "TR1plaintextdata: FAIL")
				
if modeltype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")