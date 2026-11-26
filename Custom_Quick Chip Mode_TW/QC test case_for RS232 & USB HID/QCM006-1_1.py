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
ointerface = DL.ShowMessageBox("Check output interface", "Do u test USB-HID output interface?", 0)

# Salt key check
if (Result):
	DL.SetWindowText("black", "*** Salt key check")
	DL.SendIOCommand("IDG", "81 0C", 3000, 1) 
	Result = DL.Check_RXResponse("51 00 00")
	if Result == 0:
		DL.SetWindowText("Red", "Pls load salt key first......")

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Enable MSR Additional Tags (Pure and Fallback)
if (Result):
	DL.SetWindowText("black", "*** MSR Additional Tags (Pure and Fallback) = Enable")
	if ointerface == 0: #RS232
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 01 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #USB-HID
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 01 00 00 00 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# DFEF4B = 3F
if (Result):
	DL.SetWindowText("black", "*** DFEF4B = 3F")
	DL.SendIOCommand("IDG", "04 00 DF EF 4B 03 3F 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# DF7D = 01 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# Get Data Encryption (C7-37) = encryption OFF
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 01 00")
	time.sleep(0.5)

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	Result = DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)    
#-----------------------------------------------------------------
if (Result):       
    ctcheck = DL.ShowMessageBox("Check HW", "Does the project support CT reader?", 0)
    if ctcheck == 1: #w/ CT reader
        n = 3
    if ctcheck == 0: #w/o CT reader
        n = 2
    for i in range (1, n):
        if i == 1:
            DL.ShowMessageBox("black", "Swipe ISO 4909 (3T) card --> Click OK")
            
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
                
            target_patterns = [
                '56 69 56 4F 74 65 63 68 32 00 02',
                'DF EE 23',]
            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
                
        if i == 2:
            DL.ShowMessageBox("Notice", "Insert MSR card: the 1st time (remove card) --> Click OK")
            
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)

        if i == 1:#ISO 4909 (3T)-------------------------------
            if(-1 != strCardData.find('80 3F 4C 26 68 87 00 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F')):
                if(-1 != strCardData.find('DF EC 11 20')):
                    if(-1 != strCardData.find('DF EF 4C 06 4C 26 68 00 00 00 DF EF 4D 81 DA 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F')):
                        DL.SetWindowText("blue", "DFEF4C/4D PASS")
                    else:
                        DL.SetWindowText("red", "DFEF4C/4D FAIL")
                        DL.fails=DL.fails+1
                else:
                    DL.SetWindowText("red", "DFEC11 FAIL")
                    DL.fails=DL.fails+1
            else:
                DL.SetWindowText("red", "DFEE23 FAIL")
                DL.fails=DL.fails+1
                
        if i == 2:#ISO 4909 (3T) (Fallback)-------------------------------
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
                
            DL.ShowMessageBox("black", "Swipe ISO 4909 (3T) card --> Click OK")
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)            
            if(-1 != strCardData.find('80 3F 4C 26 68 87 00 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F')):
                if(-1 != strCardData.find('DF EC 11 20')):
                    if(-1 != strCardData.find('DF EF 4C 06 4C 26 68 00 00 00 DF EF 4D 81 DA 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F')):
                        DL.SetWindowText("blue", "DFEF4C/4D PASS")
                    else:
                        DL.SetWindowText("red", "DFEF4C/4D FAIL")
                        DL.fails=DL.fails+1
                else:
                    DL.SetWindowText("red", "DFEC11 FAIL")
                    DL.fails=DL.fails+1
            else:
                DL.SetWindowText("red", "DFEE23 FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Back to default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Disable MSR Additional Tags (Pure and Fallback)
if (Result):
	DL.SetWindowText("black", "*** MSR Additional Tags (Pure and Fallback) = Disable")
	if ointerface == 0: #RS232
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #USB-HID
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(1)
    
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )