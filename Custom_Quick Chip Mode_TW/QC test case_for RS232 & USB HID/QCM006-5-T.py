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

#Objective: Encryption OFF, CT + Fallback to CT + Fallback to MSR test under Quick Chip Mode. (T=0/ Discover)

#-----------------------------------------------------------------
def msr_data_analysis(strCardData):
	global Key
    
	Track1_CardData = ""
	Track2_CardData = ""
	Track3_CardData = ""
	TRK1DecryptData = ""
	TRK2DecryptData = ""
	TRK3DecryptData = ""
    
	if strCardData!=None and strCardData!="":
		strCardData=strCardData.replace(" ","")
		CardData=DL.GetTLV(strCardData,"DFEE23")
		DL.SetWindowText("red", CardData)
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
	return Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData
#-----------------------------------------------------------------
def ct_data_analysis(strCardData):
    global strKey
    
    dec57 = ""
    dec5A = ""
    
    ksn = DL.GetTLV(strCardData,"DFEE12")	
		
    enc57 = DL.GetTLV(strCardData,"57", 0)
    if ksn and enc57:
        dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
    enc5A = DL.GetTLV(strCardData,"5A", 0)
    if ksn and enc5A:
        dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		    
    return dec57, dec5A
#---------------------------------------------------------Define main test, use subroutine
def read_card():
    if (Result):       
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
        for i in range (1, 4):
            if i == 1:
                DL.ShowMessageBox("Notice", "Insert T=0 card --> (read over, remove card) --> Click OK")
            if i == 2:
                DL.ShowMessageBox("Notice", "Swipe Discover card (PAN = xxxx....0026) --> Click OK")
            if i == 3:
                DL.ShowMessageBox("Notice", "Insert MSR card: the 1st time (remove card) --> Click OK")
                
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
            
            target_patterns = [
                '56 69 56 4F 74 65 63 68 32 00 02',]
            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
                
            if i == 1:#T=0 card
                # call function: ct_data_analysis(strCardData)
                dec57, dec5A = ct_data_analysis(strCardData)
                
                target_patterns1 = [
                    'E0 DF EE 26 02 E0 00',
                    'DF EE 25 02 00 03',
                    'DF EF 5D 11 47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC',
                    'DF EF 5B 08 47 61 CC CC CC CC 00 10',
                    '9F 39 01',
                    '4F',
                    '50',
                    '82 02',
                    '84 07 A0 00 00 00 03 10 10',
                    '8A',
                    '8C',
                    '8D',
                    '8E',
                    '95 05',
                    '99',
                    '9B',
                    '9C',
                    '5F 20',
                    '5F 24',
                    '5F 25',
                    '5F 28',
                    '5F 2A',
                    '5F 2D',
                    '5F 34',
                    '5F 57',
                    '9F 02',
                    '9F 03',
                    '9F 10',
                    '9F 13',
                    '9F 20',
                    '9F 26',
                    '9F 27',
                    '9F 34',
                    '9F 36',
                    '9F 37',
                    '9F 38',
                    '9F 4D',
                    '9F 4F',
                    '9F 53',
                    '9F 5B',
                    'DF EF 57',
                    'DF EC 18',
                    'DF EE 30 01 01',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Tags PASS")
                else:
                    DL.SetWindowText("red", "Tags FAIL")
                    DL.fails = DL.fails + 1
                    
                expect57_Pdata = "57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89"
                expect5A_Pdata = "5A 08 47 61 73 90 01 01 00 10"
                tracks = [
                    (expect57_Pdata, dec57, "Decrypt 57"),
                    (expect5A_Pdata, dec5A, "Decrypt 5A")
                ]
                for mask, card, label in tracks:
                    if not DL.Check_StringAB(mask, card):
                        DL.fails += 1
                        DL.SetWindowText("red", label + ": FAIL")
                    
            if i == 2:#Discover card (PAN = xxxx....0026)
                # call function: msr_data_analysis(strCardData)
                Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData = msr_data_analysis(strCardData)
                
                target_patterns1 = [
                    'E8 DF EE 25 02 00 11', 
                    'DF EE 23',
                    '80 1F 44 28 00 A3 9B',
                    '9F 39 01 90',
                    'FF EE 01 05 DF EE 30 01 0C',
                    'DF EE 26 02 E8 00',
                    '9F 02 06 00 00 00 00 04 44',
                    '9A 03',
                    '9F 21 03',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Tags PASS")
                else:
                    DL.SetWindowText("red", "Tags FAIL")
                    DL.fails=DL.fails+1
                    
                TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?*"
                TR2maskdata = ";6510********0026=1712****************?*"
                TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F25"
                TR2plaintextdata = "3B363531303030303030303030303032363D31373132323031313030303032313030303030303F3B"
                tracks = [
                    (TR1maskdata, Track1_CardData, "TR1maskdata"),
                    (TR2maskdata, Track2_CardData, "TR2maskdata"),
                    (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                    (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),]
                for mask, card, label in tracks:
                    if not DL.Check_StringAB(mask, card):
                        DL.fails += 1
                        DL.SetWindowText("red", label + ": FAIL")
            
            if i == 3:#Fallback to MSR transaction, Discover card (PAN = xxxx....0026)
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 50',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                
                DL.ShowMessageBox("Notice", "Insert MSR card: the 2nd time (remove card) --> Click OK")
                
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 50',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                    
                DL.ShowMessageBox("Notice", "Insert MSR card: the 3rd time (remove card) --> Click OK")
                
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 22',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                
                DL.ShowMessageBox("Notice", "Swipe Discover card (PAN = xxxx....0026) --> Click OK")
                
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                
                # call function: msr_data_analysis(strCardData)
                Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData = msr_data_analysis(strCardData)
                
                target_patterns1 = [
                    'E8 DF EE 25 02 00 07', 
                    'DF EE 23',
                    '80 1F 44 28 00 A3 9B',
                    '9F 39 01 80',
                    'FF EE 01 05 DF EE 30 01 0C',
                    'DF EE 26 02 E8 00',
                    '9F 02 06 00 00 00 00 04 44',
                    '9A 03',
                    '9F 21 03']
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Tags PASS")
                    ledcheck = DL.ShowMessageBox("LED", "When fall back to MSR reader, green LED 4 was turned FLASH ON?", 0)
                    if ledcheck == 0: 
                        DL.SetWindowText("red", "LED behavior FAIL")
                        DL.fails=DL.fails+1
                else:
                    DL.SetWindowText("red", "Tags FAIL")
                    DL.fails=DL.fails+1
                        
                TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?*"
                TR2maskdata = ";6510********0026=1712****************?*"
                TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F25"
                TR2plaintextdata = "3B363531303030303030303030303032363D31373132323031313030303032313030303030303F3B"
                tracks = [
                    (TR1maskdata, Track1_CardData, "TR1maskdata"),
                    (TR2maskdata, Track2_CardData, "TR2maskdata"),
                    (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                    (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),]
                for mask, card, label in tracks:
                    if not DL.Check_StringAB(mask, card):
                        DL.fails += 1
                        DL.SetWindowText("red", label + ": FAIL")
    else:
        DL.fails=DL.fails+1
#---------------------------------------------------------Set 5C CT termianl data
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
        
# Set CT ICS Identification = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT ICS Identification = 5C")
	DL.SendIOCommand("IDG", "60 16 05", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set CT terminal data = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 16 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# Set transaction interface = ALL
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = ALL")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# DF7D = 01 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Get Data Encryption (C7-37) = encryption ON
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	DL.Check_RXResponse("C7 00 00 01 03")
	time.sleep(0.5)

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)
#---------------------------------------------------------Start main test
read_card()
#---------------------------------------------------------Set 4C CT termianl data
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
        
# Set CT ICS Identification = 4C
if (Result):
	DL.SetWindowText("black", "*** Set CT ICS Identification = 4C")
	DL.SendIOCommand("IDG", "60 16 04", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set CT terminal data = 4C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 4C")
	DL.SendIOCommand("IDG", "6006 16009f33036008c89f3501259f40056000f05001df110101df260101df270100dfee1e08d09c20f0c20e16005f3601029f1a0208409f1e085465726d696e616c9f150212349f160f3030303030303030303030303030309f1c0838373635343332319f4e2231303732312057616c6b65722053742e20437970726573732c204341202c5553412edfee150101dfee160100dfee170105dfee180180dfee1f0180dfee1b083030303135313030dfee2203323c3cdf1008656e667265737a68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)
#---------------------------------------------------------Start main test
read_card()
#---------------------------------------------------------Change to default

#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )