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

#Objective: Encryption ON, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

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
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
	time.sleep(0.5)
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    for i in range (1, 7):
        if i == 1:
            DL.SetWindowText("black", "*** Swipe IDT test card")
        if i == 2:
            DL.SetWindowText("black", "*** Swipe AAMVA card")
        if i == 3:
            DL.SetWindowText("black", "*** Swipe JIS 1 card")
        if i == 4:
            DL.SetWindowText("black", "*** Swipe JIS 2 card")
        if i == 5:
            DL.SetWindowText("black", "*** Swipe VISA MSD card")
        if i == 6:
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
            
        strCardData = DL.ReadKeyBoardCardData(60000)
        
        if i == 1:#IDT
            if(-1 != strCardData.find('020A01837F4F286B8700021600%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?C;2121212121767676070707767676762121212?0;33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?2')):
                DL.SetWindowText("blue", "IDT PASS")
            else:
                DL.SetWindowText("red", "IDT FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#AAMVA
            if(-1 != strCardData.find('02CD00817F3023528700021600%NYNEW YORK^LEE$BRUCE$JR^655 N. BERRY ST., #K^?R;3555551111111111111=000919770303??%##92821-00440AABBBBBBBBBBTTTTF507125BRWBLK0123456789                CCCCCCSSSSS?%')):
                DL.SetWindowText("blue", "AAMVA PASS")
            else:
                DL.SetWindowText("red", "AAMVA FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#JIS 1
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:138])+ strCardData[138:524]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:636]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:630])
            checksum = DL.GetSUM(rawdata[6:630])
            #Final MSR data
            rawdata = rawdata[0:630] + lrc + checksum + rawdata[634:636]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            
            # Check MSR format
            if(-1 != strCardData.find('805F482800A39B021600')):
                DL.SetWindowText("blue", "MSR format PASS")
            else:
                DL.SetWindowText("red", "MSR format FAIL")
                DL.fails=DL.fails+1
                
            # Check mask data
            if(-1 != strCardData.find(';a900*************************************************************0000?')):
                DL.SetWindowText("blue", "Mask1 data PASS")
            else:
                DL.SetWindowText("red", "Mask1 data FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != strCardData.find(';4322********2833=1108****************?*')):
                DL.SetWindowText("blue", "Mask2 data PASS")
            else:
                DL.SetWindowText("red", "Mask2 data FAIL")
                DL.fails=DL.fails+1
                
            # Check decryption data
            if(-1 != TRK1DecryptData.find('7F6139303030303030303231313131313233343536373839303132323232323333333333343434343435353535353636363636373737373738383838383939393939303030307F15')):
                DL.SetWindowText("blue", "TRK1DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK1DecryptData FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != TRK2DecryptData.find('3B343332323036313030303837323833333D31313038323031383836343038323531303030303F3B')):
                DL.SetWindowText("blue", "TRK2DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK2DecryptData FAIL")
                DL.fails=DL.fails+1
        
        if i == 4:#JIS 2
            if(-1 != strCardData.find('02700085570048008200021600;123456789012345678901234567890123456789012345678901234567890123456789?')):
                DL.SetWindowText("blue", "JIS 2 PASS")
            else:
                DL.SetWindowText("red", "JIS 2 FAIL")
                DL.fails=DL.fails+1
            
        if i == 5:#VISA MSD
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:66])+ strCardData[66:252]
            #Length update
            l = str(0)+str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:292]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:286])
            checksum = DL.GetSUM(rawdata[6:286])
            #Final MSR data
            rawdata = rawdata[0:286] + lrc + checksum + rawdata[290:292]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            
            # Check MSR format
            if(-1 != strCardData.find('80570028008292021600')):
                DL.SetWindowText("blue", "MSR format PASS")
            else:
                DL.SetWindowText("red", "MSR format FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != strCardData.find(';4761********0010=2012****************?')):
                DL.SetWindowText("blue", "Mask2 data PASS")
            else:
                DL.SetWindowText("red", "Mask2 data FAIL")
                DL.fails=DL.fails+1
                
            if(-1 != TRK2DecryptData.find('3B343736313733393030313031303031303D32303132313230303031323333393930303033313F')):
                DL.SetWindowText("blue", "TRK2DecryptData PASS")
            else:
                DL.SetWindowText("red", "TRK2DecryptData FAIL")
                DL.fails=DL.fails+1
                
        if i == 6:#ISO 4909 (3T)
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:247])+ strCardData[247:897]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:1118]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:1112])
            checksum = DL.GetSUM(rawdata[6:1112])
            #Final MSR data
            rawdata = rawdata[0:1112] + lrc + checksum + rawdata[1116:1118]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
            
            # Check MSR format
            if(-1 != strCardData.find('807F4D276987BF021600')):
                DL.SetWindowText("blue", "MSR format PASS")
            else:
                DL.SetWindowText("red", "MSR format FAIL")
                DL.fails=DL.fails+1
                
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
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )