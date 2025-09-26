#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Objective: enable Low Power Card Detection Mode will not break 3 interfaces transaction.

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set DF7D = 02 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** Set DF7D = 02 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 02", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Set DFEE7F = 03 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** Set DFEE7F = 03 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DFEE7F 01 03", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	

# Enable Low Power Card Detection Mode
if (Result):
	DL.SetWindowText("black", "*** Enable Low Power Card Detection Mode")
	DL.SendIOCommand("IDG", "F0 12 03 01 00", 3000, 1) 
	DL.Check_RXResponse("F0 00")
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
#-----------------------------------------------------------------
if (Result):
    for i in range (1, 4):
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
        if i == 1:
            DL.SetWindowText("black", "*** Tap MasterCard MC21 card")
        if i == 2:
            DL.SetWindowText("black", "*** Insert CT card (EMV Test Card V2 T=0)")
        if i == 3:
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
            
        strCardData = DL.ReadKeyBoardCardData(20000)
        ksn = DL.GetTLV(strCardData, "DFEE12")
              
        if i == 1:#MasterCard MC21
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B085413CCCCCCCC0010')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)
            if DL.Check_StringAB(dec5A, '5A085413330089600010'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D115413CCCCCCCC0010D1412CCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)
            if DL.Check_StringAB(dec57, '57115413330089600010D1412201'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
                
        if i == 2:#CT card (EMV Test Card V2 T=0)
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B084761CCCCCCCC0010')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)
            if DL.Check_StringAB(dec5A, '5A084761739001010010'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D114761CCCCCCCC0010D2012CCCCCCCCCCCCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)
            if DL.Check_StringAB(dec57, '57114761739001010010D20122010123456789'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
                
        if i == 3:#ISO 4909 (3T) card
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:20] + DL.stringToHexString(strCardData[20:241])+ strCardData[241:871]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:1092]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:1086])
            checksum = DL.GetSUM(rawdata[6:1086])
            #Final MSR data
            rawdata = rawdata[0:1086] + lrc + checksum + rawdata[1090:1092]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            EncryptType = DL.Get_EncryptionKeyType_CardData()
            EncryptMode = DL.Get_EncryptionMode_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
            TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
            TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
            
            # Check mask data
            if(-1 != strCardData.find('%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*')):
                DL.SetWindowText("blue", "Mask1 data PASS")
            else:
                DL.SetWindowText("red", "Mask1 data FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != strCardData.find(';4547********0000=1102***************?*')):
                DL.SetWindowText("blue", "Mask2 data PASS")
            else:
                DL.SetWindowText("red", "Mask2 data FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != strCardData.find(';**4547********0000=***********************************************************************************?*')):
                DL.SetWindowText("blue", "Mask3 data PASS")
            else:
                DL.SetWindowText("red", "Mask3 data FAIL")
                DL.fails=DL.fails+1
                
            # Check decryption data
            if(-1 != TRK1DecryptData.find('2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F2E')):
                DL.SetWindowText("blue", "TRK1DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK1DecryptData FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != TRK2DecryptData.find('3B343534373537303030313037303030303D313130323130313030303030333036303030303F38')):
                DL.SetWindowText("blue", "TRK2DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK2DecryptData FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != TRK3DecryptData.find('3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F35')):
                DL.SetWindowText("blue", "TRK3DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK3DecryptData FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
    
#-----------------------------------------------------------------
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
DL.SetWindowText("black", "*** Poll on demand")
DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
Result = DL.Check_RXResponse("01 00 00 00")	
time.sleep(10)
# Disable Low Power Card Detection Mode
DL.SetWindowText("black", "*** Disable LPCD mode")
DL.SendIOCommand("IDG", "F0 12 00", 3000, 1) 
Result = DL.Check_RXResponse("F0 00")
# Set DFEE7F = 00 (NEO2)
DL.SetWindowText("black", "*** Set DFEE7F = 00 (NEO2)")
DL.SendIOCommand("IDG", "04 00 DFEE7F 01 00", 3000, 1) 
Result = DL.Check_RXResponse("04 00 00 00")	
# QuickChip mode
DL.SetWindowText("black", "*** QuickChip mode (02)")
DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
Result = DL.Check_RXResponse("01 00 00 00")	
time.sleep(1)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )