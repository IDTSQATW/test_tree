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

#Objective: Encryption OFF, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

#-----------------------------------------------------------------
# Check output interface
interfacecheck1 = DL.ShowMessageBox("", "Current output interface = USB-HID?", 0)
if interfacecheck1 == 1:
    DL.SetWindowText("Green", "*** output interface = USB-HID ***")
    # Output = USB-HID, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
    DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
    DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
    DL.Check_RXResponse("04 00 00 00")	
else:
    interfacecheck2 = DL.ShowMessageBox("", "Current output interface = RS232?", 0)
    if interfacecheck2 == 1:
        DL.SetWindowText("Green", "*** output interface = RS232 ***")
        # Output = RS232, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
        DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	
    else:
        DL.fails=DL.fails+1
        Result = False
    
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
	# DL.Check_RXResponse("C7 00 00 01 00")
	# time.sleep(0.5)

# # QuickChip mode
# if (Result):
	# DL.SetWindowText("black", "*** QuickChip mode (02)")
	# DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	# DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(6)
    
# # 18-01 to let NGAT to reconnect
# if (Result):
	# DL.SetWindowText("black", "*** Ping the reader")
	# DL.SendIOCommand("IDG", "1801", 3000, 1) 
	# DL.Check_RXResponse("18 00 00 00")	
	# time.sleep(0.2)
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
    for i in range (1, 8):
        if i == 1:
            DL.SetWindowText("black", "*** Tap Discover #84 card")
        if i == 2:
            DL.SetWindowText("black", "*** Tap INTERAC card")
        if i == 3:
            DL.SetWindowText("black", "*** Tap VISA #97 card")
        if i == 4:
            DL.SetWindowText("black", "*** Tap MasterCard MC21 card")
        if i == 5:
            DL.SetWindowText("black", "*** Tap AMEX XP8 #86 card")
        if i == 6:
            DL.SetWindowText("black", "*** Tap JCB #136 card")
        if i == 7:
            DL.SetWindowText("black", "*** Tap CUP #69 card")
        time.sleep(8)
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)
        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02',
            '9F 39 01 07',
            'FF EE 01 05 DF EE 30 01 00',
            'DF EE 26 02 21 00',
            '9F 02 06 00 00 00 00 04 44',
            '9A 03',
            '9F 21 03',]
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
        if i == 1:#Discover #84
            target_patterns1 = [
                '57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01',
                '5A 08 36 07 05 00 00 00 00 1F',
                '84 07 A0 00 00 01 52 30 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "Discover #84 PASS")
            else:
                DL.SetWindowText("red", "Discover #84 FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#INTERAC
            target_patterns1 = [
                '5A 08 54 13 33 90 00 00 15 13',
                '57 11 54 13 33 90 00 00 15 13 D0 51 22 20 01 23 45 67 89',
                '84 07 A0 00 00 02 77 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "INTERAC PASS")
            else:
                DL.SetWindowText("red", "INTERAC FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#VISA #97
            target_patterns1 = [
                '5A 07 47 61 73 90 01 01 00',
                '57 12 47 61 73 90 01 01 00 D2 01 21 20 00 12 33 99 00 03 1F',
                '84 07 A0 00 00 00 03 10 10',]
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "VISA #97 PASS")
            else:
                DL.SetWindowText("red", "VISA #97 FAIL")
                DL.fails=DL.fails+1
                
        if i == 4:#MasterCard MC21
            target_patterns1 = [
                '5A 08 54 13 33 00 89 60 00 10',
                '57 11 54 13 33 00 89 60 00 10 D1 41 22 01',
                '84 07 A0 00 00 00 04 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "MasterCard MC21 PASS")
            else:
                DL.SetWindowText("red", "MasterCard MC21 FAIL")
                DL.fails=DL.fails+1
                
        if i == 5:#AMEX XP8 #86
            target_patterns1 = [
                '57 13 37 42 45 45 54 00 00 1D 14 10',
                '5A 08 37 42 45 45 54 00 00 1F',
                '84',
                'A0 00 00 00 25 01',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "AMEX XP8 #86 PASS")
            else:
                DL.SetWindowText("red", "AMEX XP8 #86 FAIL")
                DL.fails=DL.fails+1
                
        if i == 6:#JCB #136
            target_patterns1 = [
                '5A',
                '57',
                '84 07 A0 00 00 00 65 10 10',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "JCB #136 PASS")
            else:
                DL.SetWindowText("red", "JCB #136 FAIL")
                DL.fails=DL.fails+1
                
        if i == 7:#CUP #69
            target_patterns1 = [
                '57 13 62 28 00 01 00 00 11 17 D2 01 21 20',
                '5A 08 62 28 00 01 00 00 11 17',
                '84 10 A0 00 00 03 33 01 01 01 01 01 01 01 01 01 01 01',
                'DF EC 18',
                'DF EF 57']
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "CUP #69 PASS")
            else:
                DL.SetWindowText("red", "CUP #69 FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Change to default
# # Poll on demand
# if (Result):
	# DL.SetWindowText("black", "*** Poll on demand")
	# DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	# Result = DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(5)
    
# # Enable 3 interfaces
# if (Result):
	# DL.SetWindowText("black", "*** Enable All interfaces")
	# DL.SendIOCommand("IDG", "04 00 DF EF 37 01 03", 3000, 1)     #VP6328 only can enable CL +MSR
	# time.sleep(0.2)    
	# DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1)     #VP6328 can not accept this cmd 
	# time.sleep(0.2) 
    
# # QuickChip mode
# if (Result):
	# DL.SetWindowText("black", "*** QuickChip mode (02)")
	# DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	# DL.Check_RXResponse("01 00 00 00")	
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )