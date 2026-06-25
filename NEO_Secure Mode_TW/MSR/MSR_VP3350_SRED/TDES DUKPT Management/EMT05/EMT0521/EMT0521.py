#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")
    
readertype = DL.ShowMessageBox("", "Is this NSRED project?", 0)

if readertype == 1:
    # Set DFec60, mask/ truncate mode selection = 2
    if (Result):
        RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 2')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")

    # Check data encryption TYPE is TDES	
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
            
    if (Result):
        RetOfStep = DL.SendCommand('DF7D = 02 (NEO2)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00 00 00")
        
    # Enable encryption (03)
    if (Result):
        RetOfStep = DL.SendCommand('Enable Encryption (03)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")
            
    # Poll on demand
    if (Result):
        RetOfStep = DL.SendCommand('Poll on Demand')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("01 00 00 00")

    # Burst mode OFF		
    if (Result):
        RetOfStep = DL.SendCommand('Burst mode Off')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00 00 00")	

    # cmd 02-40, swipe Discover card
    if (Result):
        for i in range(1, 4):
            if i == 1 or i == 3:     #test PAN15 & PAN14 card
                RetOfStep = DL.SendCommand('DFEC4A--08 04 2A 0C 31')
            if i == 2:     #test PAN15 card
                RetOfStep = DL.SendCommand('DFEE1D--06 04 2A 0C 31')
            if (RetOfStep):
                Result = Result and DL.Check_RXResponse("C7 00 00 00")	
            if (Result):
                time.sleep(1)
                if i <= 2:
                    RetOfStep = DL.SendCommand('Activate Transaction-15')
                if i == 3:
                    RetOfStep = DL.SendCommand('Activate Transaction-14')
                if (RetOfStep):
                    Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** DF EE 25 02 00 11 DF EE 23")
                    sResult=DL.Get_RXResponse(0)
                    if Result == True and sResult!=None and sResult!="":
                        sResult=sResult.replace(" ","")
                        CardData=DL.GetTLV(sResult,"DFEE23")
                        bresult = False
                        if CardData!=None and CardData!='':
                            objectMSR = DL.ParseCardData(CardData, Key)
                            EncryptType = DL.Get_EncryptionKeyType_CardData()
                            EncryptMode = DL.Get_EncryptionMode_CardData()
                            if objectMSR!=None:
                                DL.SetWindowText("blue", "Track 1:")
                                Track1_CardData = DL.Get_TrackN_CardData(1)
                                DL.SetWindowText("blue", "Track 2:")
                                Track2_CardData = DL.Get_TrackN_CardData(2)
                                DL.SetWindowText("blue", "Track 3:")
                                Track3_CardData = DL.Get_TrackN_CardData(3)
                                DL.SetWindowText("blue", "Track 1_Enc:")
                                TRK1 = DL.Get_EncryptTrackN_CardData(1)
                                DL.SetWindowText("blue", "Track 2_Enc:")
                                TRK2 = DL.Get_EncryptTrackN_CardData(2)
                                DL.SetWindowText("blue", "Track 3_Enc:")
                                TRK3 = DL.Get_EncryptTrackN_CardData(3)
                                DL.SetWindowText("blue", "KSN:")
                                KSN=DL.Get_KSN_CardData()
                                if len(TRK1)> 0:
                                    DL.SetWindowText("blue", "Track 1:")
                                    TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
                                if len(TRK2)> 0:
                                    DL.SetWindowText("blue", "Track 2:")
                                    TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
                                if len(TRK3) > 0:
                                    DL.SetWindowText("blue", "Track 3:")
                                    TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)

                                if i == 1:     #PAN = 15
                                    TR1maskdata = "%*407166*****9123^DOW/JOHN ^1711***************************?"
                                    TR1plaintextdata = "25423430373136363231303436393132335E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F29"
                                        
                                    Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1maskdata: FAIL")
                                        DL.fails=DL.fails+1
                                        
                                    Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1plaintextdata: FAIL")
                                        DL.fails=DL.fails+1
                                        
                                if i == 2:     #PAN = 15
                                    TR1maskdata = "%*40716******9123^DOW/JOHN ^1711***************************?"
                                    TR1plaintextdata = "25423430373136363231303436393132335E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F29"
                                        
                                    Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1maskdata: FAIL")
                                        DL.fails=DL.fails+1
                                        
                                    Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1plaintextdata: FAIL")
                                        DL.fails=DL.fails+1
                                        
                                if i == 3:     #PAN = 14
                                    TR1maskdata = "%*407166****6912^DOW/JOHN ^1711***************************?"
                                    TR1plaintextdata = "254234303731363632313034363931325E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F3A"
                                        
                                    Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1maskdata: FAIL")
                                        DL.fails=DL.fails+1
                                        
                                    Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
                                    if Result != True:
                                        DL.SetWindowText("red", "TR1plaintextdata: FAIL")
                                        DL.fails=DL.fails+1
                    else:
                        DL.fails=DL.fails+1
else:
    DL.SetWindowText("red", "Please use NSRED reader to test...")
    DL.fails=DL.fails+1
    
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
        
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
    DL.Check_RXResponse("04 00 00 00")
        
# Set DFec60, mask/ truncate mode selection = default
RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = default')
if (RetOfStep):
    DL.Check_RXResponse("C7 00 00 00")
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )