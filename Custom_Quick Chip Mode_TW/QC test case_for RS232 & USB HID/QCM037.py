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

# Objective: Verify tag DFEF7E
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (w/ DFEF7E = 5005)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (w/ DFEF7E = 5005)")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DFEF7E 02 5005", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)

# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.ShowMessageBox("Card", "Insert card (P/N: 80005206-002) --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EF 61 02 F2 21',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Fall back to MSR: PASS")
        speedcheck = DL.ShowMessageBox("", "After inserted card, LED 4 was turned ON (flash)?", 0)
        if speedcheck != 1:
            DL.SetWindowText("Red", "LED FAIL")
            DL.fails=DL.fails+1
    else:
        DL.SetWindowText("red", "Fall back to MSR: FAIL")
        DL.fails=DL.fails+1

    DL.ShowMessageBox("Card", "Swipe any card --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EE 25 02 00 07',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "MSR Data PASS")
    else:
        DL.SetWindowText("red", "MSR Data FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (w/ DFEF7E = 0203)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (w/ DFEF7E = 0203)")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DFEF7E 02 0203", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)

# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.ShowMessageBox("Card", "Insert card (P/N: 80005206-002) --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EE 25 02 50 05',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "No fallback: PASS")
        speedcheck = DL.ShowMessageBox("", "After inserted card, LED 4 did NOT be turned ON?", 0)
        if speedcheck != 1:
            DL.SetWindowText("Red", "LED FAIL")
            DL.fails=DL.fails+1
    else:
        DL.SetWindowText("red", "No fallback: FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------reset default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 16 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(1)

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )