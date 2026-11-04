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

#Objective: Encryption OFF, CL test under Quick Chip Mode. (Discover/ VISA MSD/ VISA qVSDC (EMV)/ MasterCard (MSD)/ MChip (EMV)/ INTERAC)

#-----------------------------------------------------------------
# # Check output interface
# interfacecheck1 = DL.ShowMessageBox("", "Current output interface = USB-HID?", 0)
# if interfacecheck1 == 1:
    # DL.SetWindowText("Green", "*** output interface = USB-HID ***")
    # # Output = USB-HID, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
    # DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
    # DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
    # DL.Check_RXResponse("04 00 00 00")	
# else:
    # interfacecheck2 = DL.ShowMessageBox("", "Current output interface = RS232?", 0)
    # if interfacecheck2 == 1:
        # DL.SetWindowText("Green", "*** output interface = RS232 ***")
        # # Output = RS232, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
        # DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
        # DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
        # DL.Check_RXResponse("04 00 00 00")	
    # else:
        # DL.fails=DL.fails+1
        # Result = False
#-----------------------------------------------------------------
def cl_data_analysis(strCardData):
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
#-----------------------------------------------------------------
# # Poll on demand
# if (Result):
	# DL.SetWindowText("black", "*** Poll on demand")
	# DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	# Result = DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(5)
        
# # DF7D = 01 (NEO2)
# if (Result):
	# DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	# DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	# DL.Check_RXResponse("04 00 00 00")	
    
# # Get Data Encryption (C7-37) = encryption OFF
# if (Result):
	# DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	# DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	# DL.Check_RXResponse("C7 00 00 01 03")
	# time.sleep(0.5)

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
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
    for i in range (1, 8):
        if i == 1:
            DL.ShowMessageBox("Notice", "Tap Discover #84 card --> Click OK")
        if i == 2:
            DL.ShowMessageBox("Notice", "Tap INTERAC card --> Click OK")
        if i == 3:
            DL.ShowMessageBox("Notice", "Tap VISA #97 card --> Click OK")
        if i == 4:
            DL.ShowMessageBox("Notice", "Tap MasterCard MC21 card --> Click OK")
        if i == 5:
            DL.ShowMessageBox("Notice", "Tap AMEX XP8 #86 card --> Click OK")
        if i == 6:
            DL.ShowMessageBox("Notice", "Tap JCB #136 card --> Click OK")
        if i == 7:
            DL.ShowMessageBox("Notice", "Tap CUP #69 card --> Click OK")
        # time.sleep(0.2)
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)
        
        # call function: ct_data_analysis(strCardData)
        dec57, dec5A = ct_data_analysis(strCardData)
        
        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02',
            '9F 39 01 07',
            'FF EE 01 05 DF EE 30 01 00',
            'E1 DF EE 26 02 E1 00',
            '9F 02 06 00 00 00 00 04 44',
            '9A 03',
            '9F 21 03',]
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
        if i == 1:#Discover #84----------------------------------------
            target_patterns1 = [
                'DF EF 5D 12 36 07 CC CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC',
                'DF EF 5B 08 36 07 CC CC CC C0 00 1F',
                '84 07 A0 00 00 01 52 30 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "Discover #84 PASS")
            else:
                DL.SetWindowText("red", "Discover #84 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01"
            expect5A_Pdata = "5A 08 36 07 05 00 00 00 00 1F"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
        
        if i == 2:#INTERAC----------------------------------------
            target_patterns1 = [
                'DF EF 5B 08 54 13 CC CC CC CC 15 13',
                'DF EF 5D 11 54 13 CC CC CC CC 15 13 D0 51 2C CC CC CC CC CC CC',
                '84 07 A0 00 00 02 77 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "INTERAC PASS")
            else:
                DL.SetWindowText("red", "INTERAC FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57115413339000001513D05122200123456789"
            expect5A_Pdata = "5A085413339000001513"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
        
        if i == 3:#VISA #97----------------------------------------
            target_patterns1 = [
                'DF EF 5B 07 47 61 CC CC CC 01 00',
                'DF EF 5D 12 47 61 CC CC CC 01 00 D2 01 2C CC CC CC CC CC CC CC CC',
                '84 07 A0 00 00 00 03 10 10',]
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "VISA #97 PASS")
            else:
                DL.SetWindowText("red", "VISA #97 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "571247617390010100D20121200012339900031F"
            expect5A_Pdata = "5A0747617390010100"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                
        if i == 4:#MasterCard MC21----------------------------------------
            target_patterns1 = [
                'DF EF 5B 08 54 13 CC CC CC CC 00 10',
                'DF EF 5D 11 54 13 CC CC CC CC 00 10 D1 41 2C CC',
                '84 07 A0 00 00 00 04 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "MasterCard MC21 PASS")
            else:
                DL.SetWindowText("red", "MasterCard MC21 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57 11 54 13 33 00 89 60 00 10 D1 41 22 01"
            expect5A_Pdata = "5A 08 54 13 33 00 89 60 00 10"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                
        if i == 5:#AMEX XP8 #86----------------------------------------
            target_patterns1 = [
                'DF EF 5D 13 37 42 CC CC CC C0 00 1D 14 10 CC C',
                'DF EF 5B 08 37 42 CC CC CC C0 00 1F',
                '84',
                'A0 00 00 00 25 01',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "AMEX XP8 #86 PASS")
            else:
                DL.SetWindowText("red", "AMEX XP8 #86 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57 13 37 42 45 45 54 00 00 1D 14 10"
            expect5A_Pdata = "5A 08 37 42 45 45 54 00 00 1F"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                
        if i == 6:#JCB #136----------------------------------------
            target_patterns1 = [
                'DF EF 5B',
                'DF EF 5D',
                '84 07 A0 00 00 00 65 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "JCB #136 PASS")
            else:
                DL.SetWindowText("red", "JCB #136 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57"
            expect5A_Pdata = "5A 08"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                
        if i == 7:#CUP #69----------------------------------------
            target_patterns1 = [
                'DF EF 5D 13 62 28 CC CC CC CC 11 17 D2 01 2C CC',
                'DF EF 5B 08 62 28 CC CC CC CC 11 17',
                '84 10 A0 00 00 03 33 01 01 01 01 01 01 01 01 01 01 01',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "CUP #69 PASS")
            else:
                DL.SetWindowText("red", "CUP #69 FAIL")
                DL.fails=DL.fails+1
                
            expect57_Pdata = "57 13 62 28 00 01 00 00 11 17 D2 01 21 20"
            expect5A_Pdata = "5A 08 62 28 00 01 00 00 11 17"
            tracks = [
                (expect57_Pdata, dec57, "Decrypt 57"),
                (expect5A_Pdata, dec5A, "Decrypt 5A"),]
            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Change to default

#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )