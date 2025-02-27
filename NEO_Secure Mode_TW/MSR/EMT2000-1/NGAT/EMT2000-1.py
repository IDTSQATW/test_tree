#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Objective: Decrypted data for transarmorRSA should contain TID and tag data with the value from card.
		
# Check TransAmor RSA test cert
certcheck = DL.ShowMessageBox("", "Does the reader had TransAmor RSA test cert? (If NO, pls load it from NGAT toolbar -- RSA-TransAmor, and then restart test)", 0)
if certcheck == 1:
    Result= True
else:
    Result= False
        
########################### Start test ###########################
if (Result):
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
            
    # DF7D = 02 (NEO2)
    if (Result):
        RetOfStep = DL.SendCommand('DF7D = 02 (NEO2)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00")	
            
    # cmd 02-40, swipe Discover card
    if (Result):
        Result = DL.SendCommand('Activate Transaction')
        if (Result):
            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 5F 43 27 00 A3 9B 01 02")
            sResult=DL.Get_RXResponse(0)
            
            if (Result):
                CardData=DL.GetTLV(sResult,"DFEE23",0,1)
                if CardData!=None and CardData!='':
                    objectMSR = DL.ParseCardData(CardData,Key)
                    if objectMSR == True:     #Parse MSR data OK
                        if len(DL.Get_EncryptTrackN_CardData(1))> 0:
                            Track1_CardData = DL.Get_TrackN_CardData(1)
                            TRK1DecryptData = DL.DecryptTransAmorData(DL.Get_EncryptTrackN_CardData(1))
                        if len(DL.Get_EncryptTrackN_CardData(2))> 0:
                            Track2_CardData = DL.Get_TrackN_CardData(2)
                            TRK2DecryptData = DL.DecryptTransAmorData(DL.Get_EncryptTrackN_CardData(2))
                        # if len(DL.Get_EncryptTrackN_CardData(3)) > 0:
                            # Track3_CardData = DL.Get_TrackN_CardData(3)
                            # TRK3DecryptData = DL.DecryptTransAmorData(DL.Get_EncryptTrackN_CardData(3))
                                    
                        # Verify specific tags
                        if DL.Check_RXResponse("9F39 01 90") == False:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "Tag9F39: FAIL")	
                        if DL.Check_RXResponse("FFEE01 ** DFEE30010C") == False:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TagFFEE01: FAIL")	
                        if DL.Check_RXResponse("DFEE26 02 EC02") == False:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TagDFEE26: FAIL")	

                        # Transaction result verification
                        #Track 1
                        TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?"
                        TR1plaintextdata = "87654321B6510000000000026^CARD/IMAGE 03             ^17122011000021000000"
                                        
                        if TR1maskdata != Track1_CardData:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TR1maskdata: FAIL")
                        if TR1plaintextdata != TRK1DecryptData:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TR1plaintextdata: FAIL")
                            
                        #Track 2
                        TR2maskdata = ";6510********0026=1712****************?"
                        TR2plaintextdata = "876543216510000000000026=17122011000021000000"
                                        
                        if TR2maskdata != Track2_CardData:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TR2maskdata: FAIL")
                        if TR2plaintextdata != TRK2DecryptData:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("red", "TR2plaintextdata: FAIL")
            else:
                DL.fails=DL.fails+1

    if modeltype == 1:
        RetOfStep = DL.SendCommand('0105 default (VP3350)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("01 00 00 00")
else:
    DL.fails=DL.fails+1
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )