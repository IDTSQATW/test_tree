#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Objective: Encryption ON, CT (& Fallback to CT) test under Quick Chip Mode. (T=0/ Discover)

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
	time.sleep(0.5)

# if (Result):
	# DL.SetWindowText("black", "*** C7-38")
	# DL.SendIOCommand("IDG", "C7 38 DF DE 04 01 08", 3000, 1)
	# Result = DL.Check_RXResponse("C7 00 00 00")
#-----------------------------------------------------------------
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    
    ################# CT transaction #################
    DL.SetWindowText("black", "*** Click OK --> Insert T=0 card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    ksn = DL.GetTLV(strCardData, "DFEE12")
    
    # Check mask 5A = DFEF5B
    if(-1 != strCardData.find('DFEF5B084761CCCCCCCC0010')):
        DL.SetWindowText("blue", "DFEF5B PASS")
    else:
        DL.SetWindowText("red", "DFEF5B FAIL")
        DL.fails=DL.fails+1
    # Check enc 5A
    enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
    dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
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
    dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
    if DL.Check_StringAB(dec57, '57114761739001010010D20122010123456789'):
        DL.SetWindowText("blue", "57 PASS")
    else:
        DL.SetWindowText("red", "57 FAIL")
        DL.fails=DL.fails+1
        
    # Check DFEF57
    if(-1 != strCardData.find('DFEF57')):
        DL.SetWindowText("blue", "DFEF57 PASS")
    else:
        DL.SetWindowText("red", "DFEF57 FAIL")
        DL.fails=DL.fails+1
        
    # Check DFEC18
    if(-1 != strCardData.find('DFEC181D454D5620436F6D6D6F6E2047656E2033204C322056312E33302E303339')):
        DL.SetWindowText("blue", "DFEC18 PASS")
    else:
        DL.SetWindowText("red", "DFEC18 FAIL")
        DL.fails=DL.fails+1

    ################# Fallback to CT transaction (default: disable) #################
    DL.SetWindowText("black", "*** Swipe Discover card (PAN = 6510000000000125)")
    strCardData = DL.ReadKeyBoardCardData(20000)
    #Tracks data, ASCII convert to HEX 
    rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:134])+ strCardData[134:520]
    #Length update
    l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
    l = l[2:]+l[0:2]
    rawdata = rawdata[0:2] + l + rawdata[6:628]
    rawdata = rawdata.upper()
    #LRC/ check sum update
    lrc = DL.GetLRC(rawdata[6:622])
    checksum = DL.GetSUM(rawdata[6:622])
    #Final MSR data
    rawdata = rawdata[0:622] + lrc + checksum + rawdata[626:628]
    objectMSR = DL.ParseCardData(rawdata, Key)
    KSN = DL.Get_KSN_CardData()
    TRK1 = DL.Get_EncryptTrackN_CardData(1)
    TRK2 = DL.Get_EncryptTrackN_CardData(2)
    TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
    TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
    
    # Check MSR format
    if(-1 != strCardData.find('805F442800A39B021600')):
        DL.SetWindowText("blue", "MSR format PASS")
    else:
        DL.SetWindowText("red", "MSR format FAIL")
        DL.fails=DL.fails+1
        
    # Check mask data
    if(-1 != strCardData.find('%*6510********0125^CARD/IMAGE 08             ^1712****************?')):
        DL.SetWindowText("blue", "Mask1 data PASS")
    else:
        DL.SetWindowText("red", "Mask1 data FAIL")
        DL.fails=DL.fails+1
        
    if(-1 != strCardData.find(';6510********0125=1712****************?')):
        DL.SetWindowText("blue", "Mask2 data PASS")
    else:
        DL.SetWindowText("red", "Mask2 data FAIL")
        DL.fails=DL.fails+1
        
    # Check decryption data
    if(-1 != TRK1DecryptData.find('2542363531303030303030303030303132355E434152442F494D414745203038202020202020202020202020205E31373132323031313030303039353030303030303F')):
        DL.SetWindowText("blue", "TRK1DecryptData PASS")
    else:
        DL.SetWindowText("red", "TRK1DecryptData FAIL")
        DL.fails=DL.fails+1
        
    if(-1 != TRK2DecryptData.find('3B363531303030303030303030303132353D31373132323031313030303039353030303030303F')):
        DL.SetWindowText("blue", "TRK2DecryptData PASS")
    else:
        DL.SetWindowText("red", "TRK2DecryptData FAIL")
        DL.fails=DL.fails+1

    ################# Fallback to MSR transaction (default: can retry ICC card 3 times) #################
    DL.SetWindowText("black", "*** Fallback to MSR transaction (Insert MSR card 3 times --> (Green LED 3 is flash ON) Swipe card")
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F220')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F222')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    DL.SetWindowText("black", "*** Swipe Discover card (PAN = 6510000000000125)")
    strCardData = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData.find('DFEE25')):
        if(-1 != strCardData.find('9F390180')):          
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[32:58] + DL.stringToHexString(strCardData[58:166])+ strCardData[166:552]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:628]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:622])
            checksum = DL.GetSUM(rawdata[6:622])
            #Final MSR data
            rawdata = rawdata[0:622] + lrc + checksum + rawdata[626:628]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            
            # Check MSR format
            if(-1 != strCardData.find('805F442800A39B021600')):
                DL.SetWindowText("blue", "MSR format PASS")
            else:
                DL.SetWindowText("red", "MSR format FAIL")
                DL.fails=DL.fails+1
                
            # Check mask data
            if(-1 != strCardData.find('%*6510********0125^CARD/IMAGE 08             ^1712****************?')):
                DL.SetWindowText("blue", "Mask1 data PASS")
            else:
                DL.SetWindowText("red", "Mask1 data FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != strCardData.find(';6510********0125=1712****************?')):
                DL.SetWindowText("blue", "Mask2 data PASS")
            else:
                DL.SetWindowText("red", "Mask2 data FAIL")
                DL.fails=DL.fails+1
                
            # Check decryption data
            if(-1 != TRK1DecryptData.find('2542363531303030303030303030303132355E434152442F494D414745203038202020202020202020202020205E31373132323031313030303039353030303030303F')):
                DL.SetWindowText("blue", "TRK1DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK1DecryptData FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != TRK2DecryptData.find('3B363531303030303030303030303132353D31373132323031313030303039353030303030303F')):
                DL.SetWindowText("blue", "TRK2DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK2DecryptData FAIL")
                DL.fails=DL.fails+1
        else:
            DL.SetWindowText("red", "9F39 FAIL")
            DL.fails=DL.fails+1
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        
    speedcheck = DL.ShowMessageBox("", "When fallback to MSR reader, LED 3 was turned ON (flash status)?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1

DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )