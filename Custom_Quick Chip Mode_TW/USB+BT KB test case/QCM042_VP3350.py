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
DL.ShowMessageBox("Connection check", "Must remain only 1 connection w/ PC, USB or Bluetooth", 0)
#-----------------------------------------------------------------
loop = 10000
DL.ShowMessageBox("Precondition", "Click OK --> Place MasterCard MC21 card on the CL reader", 0)

while n <= loop and Result == True:
    DL.SetWindowText("blue", "Test cycles: " + str(n))
    strCardData = DL.ReadKeyBoardCardData(20000)

    if (-1 != strCardData.find('DFEF5B085413CCCCCCCC0010')):
        DL.SetWindowText("blue", "DFEF5B PASS")
    else:
        DL.SetWindowText("red", "DFEF5B FAIL")
        DL.fails=DL.fails+1
        
    if (-1 != strCardData.find('DFEF5D115413CCCCCCCC0010D1412CCC')):
        DL.SetWindowText("blue", "DFEF5D PASS")
    else:
        DL.SetWindowText("red", "DFEF5D FAIL")
        DL.fails=DL.fails+1
        
    if (-1 != strCardData.find('DFEC18174D61737465724361726420332E312E342C2076312E3030')):
        DL.SetWindowText("blue", "DFEC18 PASS")
    else:
        DL.SetWindowText("red", "DFEC18 FAIL")
        DL.fails=DL.fails+1
        
    if (-1 != strCardData.find('DFEF57')):
        DL.SetWindowText("blue", "DFEF57 PASS")
    else:
        DL.SetWindowText("red", "DFEF57 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
    n = n + 1
    if n <= loop and Result == True:
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        time.sleep(0.2)
#-----------------------------------------------------------------
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )
