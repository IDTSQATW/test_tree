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

##### tag DFEC14 = 01
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):
	DL.SetWindowText("black", "*** Set tag DFEC14 = 01")
	DL.SendIOCommand("IDG", "0400 DFEC14 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
if (Result):
	DL.SetWindowText("black", "*** Set tag DFEC15 data")
	DL.SendIOCommand("IDG", "0400 DFEC15 2B 7C312E31302E3033377C312E307C312E30347C342E302E327C312E377C3830313439313233205265762E41", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Tap VISA card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEC1535')) and (-1 != strCardData.find('7C312E31302E3033377C312E307C312E30347C342E302E327C312E377C3830313439313233205265762E41')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
if (Result): 
    DL.SetWindowText("black", "*** Tap MC card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEC1535')) and (-1 != strCardData.find('7C312E31302E3033377C312E307C312E30347C342E302E327C312E377C3830313439313233205265762E41')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
if (Result): 
    DL.SetWindowText("black", "*** Tap Discover card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEC1535')) and (-1 != strCardData.find('7C312E31302E3033377C312E307C312E30347C342E302E327C312E377C3830313439313233205265762E41')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
####### tag DFEC14 = 00
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
   
if (Result):
	DL.SetWindowText("black", "*** Set tag DFEC14 = 00")
	DL.SendIOCommand("IDG", "0400 DFEC14 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Tap VISA card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEC15')):
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    else:
        DL.SetWindowText("blue", "PASS")
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )