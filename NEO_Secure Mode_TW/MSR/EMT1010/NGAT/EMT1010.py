#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
DL.fails = 0
DL.warnings = 0

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Objective: CS-6753, [Vendi] ISO PAN prefixes 6396210 to 6396211 are converted to plaintext.

# Check DUKPT Key  Type (81-02)
if (Result):
    RetOfStep = DL.SendCommand('Check DUKPT Key Type 81-02')
    if (RetOfStep):
        Result = DL.Check_RXResponse("81 00 00 0C FF FF 01 FF FF 01")	
        
# C7-36 -- 03
if (Result):
    RetOfStep = DL.SendCommand('C7-36 -- 03')
    if (RetOfStep):
        Result = DL.Check_RXResponse("C7 00 00 00")	

# Poll on demand	
if (Result):
    RetOfStep = DL.SendCommand('Poll on demand')
    if (RetOfStep):
        Result = DL.Check_RXResponse("01 00 00 00")	

# AT w/ LCD
if (Result):
    for i in range(1, 3):
        if i == 1: RetOfStep = DL.SendCommand('AT w/ LCD')
        if i == 2: RetOfStep = DL.SendCommand('AT w/ LCD 2')
        #Result = DL.Check_RXResponse(0, "56 69 56 4F 74 65 63 68 32 00 02 00 ** DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 1F 44 28 00 A3 00")
        sResult=DL.Get_RXResponse(0)
        if Result == True and sResult!=None and sResult!="":
            sResult=sResult.replace(" ","")
            CardData=DL.GetTLV(sResult,"DFEE23")
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
                    if TRK1 and KSN is not None:
                        TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
                    if TRK2 and KSN is not None:
                        TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
                    if TRK3 and KSN is not None:
                        TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)

                    # Transaction result verification
                    if i == 1:
                        TR1plaintextdata = "%B6396210000000026^CARD/IMAGE 03             ^17122011000021000000?."
                        TR2plaintextdata = ";6396210000000026=17122011000021000000?0"
                                            
                        if Track1_CardData and Track2_CardData:
                            res1 = DL.Check_StringAB(TR1plaintextdata, Track1_CardData)
                            res2 = DL.Check_StringAB(TR2plaintextdata, Track2_CardData)
                            if not res1 or not res2:
                                DL.fails += 1
                                DL.SetWindowText("red", "Plaintext comparison FAIL")
                            else:
                                DL.SetWindowText("blue", "Plaintext comparison PASS")
                        else:
                            DL.fails += 1
                            DL.SetWindowText("red", "Track data is missing (NULL)")
                                
                    if i == 2:
                        TR1plaintextdata = "%B6396211000000026^CARD/IMAGE 03             ^17122011000021000000?/"
                        TR2plaintextdata = ";6396211000000026=17122011000021000000?1"
                                            
                        if Track1_CardData and Track2_CardData:
                            res1 = DL.Check_StringAB(TR1plaintextdata, Track1_CardData)
                            res2 = DL.Check_StringAB(TR2plaintextdata, Track2_CardData)
                            if not res1 or not res2:
                                DL.fails += 1
                                DL.SetWindowText("red", "Plaintext comparison FAIL")
                            else:
                                DL.SetWindowText("blue", "Plaintext comparison PASS")
                        else:
                            DL.fails += 1
                            DL.SetWindowText("red", "Track data is missing (NULL)")
            else:
                DL.fails=DL.fails+1
        else:
            DL.fails=DL.fails+1
            DL.SetWindowText("red", "Card data is wrong")
else:
	DL.fails=DL.fails+1
				
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )