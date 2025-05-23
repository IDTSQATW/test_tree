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
	time.sleep(6)
    
# AT Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
if (Result):
	DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
	if ointerface == 0: #USB KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 00 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #Bluetooth KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 02 00 00 00 00 00 00 00", 3000, 1) 
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
            
        strCardData = DL.ReadKeyBoardCardData(60000)
        
        if i == 1:#IDT
            if(-1 != strCardData.find('%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?;2121212121767676070707767676762121212?;33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?')):
                DL.SetWindowText("blue", "IDT PASS")
            else:
                DL.SetWindowText("red", "IDT FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#VISA MSD
            if(-1 != strCardData.find(';4761739001010010=20121200012339900031?')):
                DL.SetWindowText("blue", "VISA MSD PASS")
            else:
                DL.SetWindowText("red", "VISA MSD FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#AAMVA
            if(-1 != strCardData.find('%NYNEW YORK^LEE$BRUCE$JR^655 N. BERRY ST., #K^?;3555551111111111111=000919770303?%##92821-00440AABBBBBBBBBBTTTTF507125BRWBLK0123456789                CCCCCCSSSSS?')):
                DL.SetWindowText("blue", "AAMVA PASS")
            else:
                DL.SetWindowText("red", "AAMVA FAIL")
                DL.fails=DL.fails+1
                
        if i == 4:#JIS 1
            if(-1 != strCardData.find(';a90000000211111234567890122222333334444455555666667777788888999990000?;4322061000872833=11082018864082510000?')):
                DL.SetWindowText("blue", "JIS 1 PASS")
            else:
                DL.SetWindowText("red", "JIS 1 FAIL")
                DL.fails=DL.fails+1
                
        if i == 5:#JIS 2
            if(-1 != strCardData.find(';123456789012345678901234567890123456789012345678901234567890123456789?')):
                DL.SetWindowText("blue", "JIS 2 PASS")
            else:
                DL.SetWindowText("red", "JIS 2 FAIL")
                DL.fails=DL.fails+1
                
        if i == 6:#ISO 4909 (3T)
            if(-1 != strCardData.find('%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?;4547570001070000=1102101000003060000?;014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?')):
                DL.SetWindowText("blue", "ISO 4909 (3T) PASS")
            else:
                DL.SetWindowText("red", "ISO 4909 (3T) FAIL")
                DL.fails=DL.fails+1

else:
    DL.fails=DL.fails+1
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )