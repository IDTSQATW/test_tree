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
ointerface = DL.ShowMessageBox("Check output interface", "Do u test Bluetooth output interface?", 0)

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Enable MSR Additional Tags (Pure and Fallback)
if (Result):
	DL.SetWindowText("black", "*** MSR Additional Tags (Pure and Fallback) = Enable")
	if ointerface == 0: #USB KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 01 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #Bluetooth KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 02 00 01 00 00 00 00 00", 3000, 1) 
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
    
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    for i in range (1, 3):
        if i == 1:
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
            strCardData = DL.ReadKeyBoardCardData(60000)
        if i == 2:
            DL.SetWindowText("black", "*** Fallback to MSR transaction (Insert MSR card 3 times --> (Green LED 3 is flash ON) Swipe ISO 4909 (3T) card")

        if i == 1:#ISO 4909 (3T)
            if(-1 != strCardData.find('DFEE2381DA%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?;4547570001070000=1102101000003060000?;014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?')):
                if(-1 != strCardData.find('DFEC1120')):
                    if(-1 != strCardData.find('DFEF4C064C2668000000DFEF4D81DA2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F3B343534373537303030313037303030303D313130323130313030303030333036303030303F3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F')):
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
                
        if i == 2:#ISO 4909 (3T) (Fallback)
            DL.SetWindowText("black", "*** Insert ISO 4909 (3T) card, @1st time")
            strCardData1 = DL.ReadKeyBoardCardData(10000)
            if(-1 != strCardData1.find('DFEF6102F220')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "Error code FAIL")
                DL.fails=DL.fails+1
            DL.SetWindowText("black", "*** Insert ISO 4909 (3T) card, @2nd time")
            strCardData1 = DL.ReadKeyBoardCardData(10000)
            DL.SetWindowText("black", "*** Insert ISO 4909 (3T) card, @3rd time")
            strCardData1 = DL.ReadKeyBoardCardData(10000)
            if(-1 != strCardData1.find('DFEF6102F222')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "Error code FAIL")
                DL.fails=DL.fails+1
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
            strCardData = DL.ReadKeyBoardCardData(10000)
        
            if(-1 != strCardData.find('DFEE2381DA%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?;4547570001070000=1102101000003060000?;014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?')):
                if(-1 != strCardData.find('DFEC1120')):
                    if(-1 != strCardData.find('DFEF4C064C2668000000DFEF4D81DA2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F3B343534373537303030313037303030303D313130323130313030303030333036303030303F3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F')):
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
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
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
	if ointerface == 0: #USB KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 00 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #Bluetooth KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 02 00 00 00 00 00 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )