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

# Objective: to verify Tag DFEF6E (Carriage Return)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 04 00 DF EF 6E 01 0D
if (Result):
	DL.SetWindowText("black", "*** 04 00 DF EF 6E 01 0D")
	DL.SendIOCommand("IDG", "04 00 DF EF 6E 01 0D", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):
    DL.ShowMessageBox("", "/// Must remain only 1 connection w/ PC, USB or Bluetooth", 0)
    speedcheck = DL.ShowMessageBox("", "Open 'Notepad_win10.exe' -> tap any CL card 3 times -> notice the cursor position", 0)
    speedcheck = DL.ShowMessageBox("", "The cursor will be moved to the beginning of next line (CR) per tap?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "DF EF 6E 01 0D >> PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 04 00 DF EF 6E 02 0D 0A
if (Result):
	DL.SetWindowText("black", "*** 04 00 DF EF 6E 02 0D 0A")
	DL.SendIOCommand("IDG", "04 00 DF EF 6E 02 0D 0A", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):
    DL.ShowMessageBox("", "/// Must remain only 1 connection w/ PC, USB or Bluetooth", 0)
    speedcheck = DL.ShowMessageBox("", "Open 'Notepad_win10.exe' -> tap any CL card 3 times -> notice the cursor position", 0)
    speedcheck = DL.ShowMessageBox("", "The cursor will be skipped a new line and was moved to the beginning of the next line (CR + LF) per tap?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "DF EF 6E 02 0D 0A >> PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )