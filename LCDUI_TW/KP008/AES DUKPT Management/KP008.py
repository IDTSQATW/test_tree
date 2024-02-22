#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'
rx = 0

#Objective: to verify cmd 83-41, Get PAN.

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

# cmd 83-41, Get PAN
if (Result):
    RetOfStep = DL.SendCommand('83-41')
    if (RetOfStep):
        Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 83 00 ** E3 ** DF EE 25 02 00 11 ** DF EE 23")
        if (Result):
            sResult=DL.Get_RXResponse(0)
            sResult=sResult.replace(" ","")
            CardData=DL.GetTLV(sResult,"DFEE23")
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
                    TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
                if len(TRK2)> 0:
                    DL.SetWindowText("blue", "Track 2:")
                    TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
                if len(TRK3) > 0:
                    DL.SetWindowText("blue", "Track 3:")
                    TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
                        
                TR2maskdata = ";1234********5678=1111:****?*"
                TR3maskdata = "1108032=0330010"
                TR2plaintextdata = "3B313233343536373831323334353637383D313131313A323232323F33000000"
                    
                Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
                if Result != True:
                    DL.SetWindowText("red", "TR2maskdata: FAIL")
                    DL.fails=DL.fails+1
                        
                Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
                if Result != True:
                    DL.SetWindowText("red", "TR3maskdata: FAIL")
                    DL.fails=DL.fails+1
                    
                Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
                if Result != True:
                    DL.SetWindowText("red", "TR2plaintextdata: FAIL")
                    DL.fails=DL.fails+1
        else:
            DL.fails=DL.fails+1
if(0 < (DL.fails + DL.warnings)):
    DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
    DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )