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

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set tags DFED20/ DFED21/ DFED22
if (Result):
	DL.SetWindowText("black", "*** Set tags DFED20/ DFED21/ DFED22")
	DL.SendIOCommand("IDG", "04 00 df ed 20 06 53 6c 69 6d 43 44 df ed 21 03 11 02 18 df ed 22 0a 31 2e 33 7c 30 34 32 33 31 38", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# Set CT terminal data = 5C w/ tag DFEF5A.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF5A")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DF EF 5A 09 DF ED 20 DF ED 21 DF ED 22", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):       
    DL.SetWindowText("black", "*** Insert EMV T=0 card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFED2006536C696D4344DFED2103110218DFED220A312E337C303432333138')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
    # for JIRA#CS-3869
    DL.SetWindowText("black", "*** Tap any CL card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFED2006536C696D4344DFED2103110218DFED220A312E337C303432333138')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1