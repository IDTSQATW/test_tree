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
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
    
# Output = RS232, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
if (Result):
	DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
	DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# DF7D = 01 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# enable MSR only
if (Result):
	DL.SetWindowText("black", "*** DFEF37 = 01 = enable MSR only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 01", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Get Data Encryption (C7-37) = encryption OFF
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	DL.Check_RXResponse("C7 00 00 01 00")
	time.sleep(0.5)

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232")
    for i in range (1, 7):
        if i == 1:
            DL.SetWindowText("black", "*** Swipe IDT test card")
        if i == 2:
            DL.SetWindowText("black", "*** Swipe VISA MSD card")
        if i == 3:
            DL.SetWindowText("black", "*** Swipe AAMVA card")
        if i == 4:
            DL.SetWindowText("black", "*** Swipe JIS 1 card")
        if i == 5:
            DL.SetWindowText("black", "*** Swipe JIS 2 card")
        if i == 6:
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
        time.sleep(5)
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)
        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02 00',
            'DF EE 25 02 00 11', 
            'DF EE 23',
            '9F 39 01 90',
            'FF EE 01 05 DF EE 30 01 0C',
            'DF EE 26 02 28 00',
            '9F 02 06 00 00 00 00 04 44',
            '9A 03',
            '9F 21 03']
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
        if i == 1:#IDT
            if(-1 != strCardData.find('83 3F 4E 27 6A 87 00 25 54 52 41 43 4B 31 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 3F 3B 32 31 32 31 32 31 32 31 32 31 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 37 36 32 31 32 31 32 31 32 3F 3B 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 3F')):
                DL.SetWindowText("GREEN", "IDT PASS")
            else:
                DL.SetWindowText("red", "IDT FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#VISA MSD
            if(-1 != strCardData.find('80 17 00 27 00 82 00 3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')):
                DL.SetWindowText("GREEN", "VISA MSD PASS")
            else:
                DL.SetWindowText("red", "VISA MSD FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#AAMVA
            if(-1 != strCardData.find('81 3F 2F 22 51 87 00 25 4E 59 4E 45 57 20 59 4F 52 4B 5E 4C 45 45 24 42 52 55 43 45 24 4A 52 5E 36 35 35 20 4E 2E 20 42 45 52 52 59 20 53 54 2E 2C 20 23 4B 5E 3F 3B 33 35 35 35 35 35 31 31 31 31 31 31 31 31 31 31 31 31 31 3D 30 30 30 39 31 39 37 37 30 33 30 33 3F 25 23 23 39 32 38 32 31 2D 30 30 34 34 30 41 41 42 42 42 42 42 42 42 42 42 42 54 54 54 54 46 35 30 37 31 32 35 42 52 57 42 4C 4B 30 31 32 33 34 35 36 37 38 39 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 43 43 43 43 43 43 53 53 53 53 53 3F')):
                DL.SetWindowText("GREEN", "AAMVA PASS")
            else:
                DL.SetWindowText("red", "AAMVA FAIL")
                DL.fails=DL.fails+1
                
        if i == 4:#JIS 1
            if(-1 != strCardData.find('80 1F 47 27 00 A3 00 7F 61 39 30 30 30 30 30 30 30 32 31 31 31 31 31 32 33 34 35 36 37 38 39 30 31 32 32 32 32 32 33 33 33 33 33 34 34 34 34 34 35 35 35 35 35 36 36 36 36 36 37 37 37 37 37 38 38 38 38 38 39 39 39 39 39 30 30 30 30 7F 3B 34 33 32 32 30 36 31 30 30 30 38 37 32 38 33 33 3D 31 31 30 38 32 30 31 38 38 36 34 30 38 32 35 31 30 30 30 30 3F')):
                DL.SetWindowText("GREEN", "JIS 1 PASS")
            else:
                DL.SetWindowText("red", "JIS 1 FAIL")
                DL.fails=DL.fails+1
                
        if i == 5:#JIS 2
            if(-1 != strCardData.find('85 17 00 47 00 82 00 7F 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 7F')):
                DL.SetWindowText("GREEN", "JIS 2 PASS")
            else:
                DL.SetWindowText("red", "JIS 2 FAIL")
                DL.fails=DL.fails+1
                
        if i == 6:#ISO 4909 (3T)
            if(-1 != strCardData.find('80 3F 4C 26 68 87 00 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F')):
                DL.SetWindowText("GREEN", "ISO 4909 (3T) PASS")
            else:
                DL.SetWindowText("red", "ISO 4909 (3T) FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Change to default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
    
# Enable 3 interfaces
if (Result):
	DL.SetWindowText("black", "*** Enable All interfaces")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 03", 3000, 1)     #VP6328 only can enable CL +MSR
	time.sleep(0.2)    
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1)     #VP6328 can not accept this cmd 
	time.sleep(0.2) 
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )