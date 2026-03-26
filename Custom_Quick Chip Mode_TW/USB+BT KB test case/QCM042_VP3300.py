#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
n = 1

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Objective: Stress test (CL)
#-----------------------------------------------------------------
#DL.ShowMessageBox("Connection check", "Must remain only 1 connection w/ PC, USB or Bluetooth", 0)
#-----------------------------------------------------------------
loop = 10000
DL.ShowMessageBox("Precondition", "Click OK --> Place MasterCard MC21 card on the CL reader", 0)

DL.SetWindowText("black", "*** Set FFFC = 02")
DL.SendIOCommand("IDG", "04 03 FF E4 01 01 9F 03 06 00 00 00 00 00 00 9F 53 01 00 9F 6D 02 00 01 9A 03 FF FF FF 9F 21 03 FF FF FF 9C 01 00 5F 2A 02 08 40 5F 36 01 02 9F 09 02 00 02 9F 15 02 11 11 9F 1A 02 08 40 9F 1B 04 00 00 17 70 9F 1C 08 00 00 00 00 00 00 00 00 9F 33 03 00 08 E8 9F 35 01 22 9F 40 05 60 00 00 10 01 9F 7C 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 9F 7E 01 00 DF 28 03 00 08 E8 DF 29 03 00 68 E8 FF F1 06 00 00 00 01 00 00 FF F5 06 00 00 00 00 80 00 FF FC 01 02 FF FD 05 F8 50 AC F8 00 FF FE 05 F8 50 AC A0 00 FF FF 05 00 00 00 00 00 DF 81 1A 03 9F 6A 04 DF 81 1E 01 10 DF 81 24 06 00 00 00 03 00 00 DF 81 25 06 00 00 00 03 00 00 DF 81 2C 01 00 9F 39 01 91", 3000, 1) 
Result = DL.Check_RXResponse("04 00 00 00")
time.sleep(0.5)

while n <= loop and Result == True:
    DL.SetWindowText("blue", "Test cycles: " + str(n))
    strCardData = DL.ReadKeyBoardCardData(20000)

    if (-1 != strCardData.find('DFEF5B085413CCCCCCCC0010')):
        DL.SetWindowText("blue", "DFEF5B PASS")
    else:
        DL.SetWindowText("red", "DFEF5B FAIL")
        DL.fails=DL.fails+1
        
    if (-1 != strCardData.find('DFEF5D115413CCCCCCCC0010D1412')):
        DL.SetWindowText("blue", "DFEF5D PASS")
    else:
        DL.SetWindowText("red", "DFEF5D FAIL")
        DL.fails=DL.fails+1
        
    if (-1 != strCardData.find('DFEF57')):
        DL.SetWindowText("blue", "DFEF57 PASS")
    else:
        DL.SetWindowText("red", "DFEF57 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('DFEE26')):
        DL.SetWindowText("blue", "DFEE26 PASS")
    else:
        DL.SetWindowText("red", "DFEE26 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('DFEE120A')):
        DL.SetWindowText("blue", "DFEE12 PASS")
    else:
        DL.SetWindowText("red", "FFEE12 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('57')):
        DL.SetWindowText("blue", "57 PASS")
    else:
        DL.SetWindowText("red", "57 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('5A')):
        DL.SetWindowText("blue", "5A PASS")
    else:
        DL.SetWindowText("red", "5A FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F0206')):
        DL.SetWindowText("blue", "9F02 PASS")
    else:
        DL.SetWindowText("red", "9F02 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F2103')):
        DL.SetWindowText("blue", "9F21 PASS")
    else:
        DL.SetWindowText("red", "9F21 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False

    n = n + 1
    if n <= loop and Result == True:
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        time.sleep(1)
#-----------------------------------------------------------------
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )
