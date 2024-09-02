#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

#Objective: Encryption ON, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
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
            
        strCardData = DL.ReadKeyBoardCardData(20000)
        
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

        
        if i == 4:#JIS 2
            if(-1 != strCardData.find('02700085570048008200021600;a90000000211111234567890122222333334444455555666667777788888999990000?333434543136383430307DC303')):
                DL.SetWindowText("blue", "JIS 2 PASS")
            else:
                DL.SetWindowText("red", "JIS 2 FAIL")
                DL.fails=DL.fails+1
            
        if i == 5:#VISA MSD

            
        if i == 6:#ISO 4909 (3T)

                
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )