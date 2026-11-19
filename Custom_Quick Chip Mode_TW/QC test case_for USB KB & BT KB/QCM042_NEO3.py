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
        
    if (-1 != strCardData.find('DFEE2602')):
        DL.SetWindowText("blue", "DFEE26 PASS")
    else:
        DL.SetWindowText("red", "DFEE26 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('DFEE120A')):
        DL.SetWindowText("blue", "DFEE12 PASS")
    else:
        DL.SetWindowText("red", "DFEE12 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('4F07')):
        DL.SetWindowText("blue", "4F PASS")
    else:
        DL.SetWindowText("red", "4F FAIL")
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
        
    if (-1 != strCardData.find('8407')):
        DL.SetWindowText("blue", "84 PASS")
    else:
        DL.SetWindowText("red", "84 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9505')):
        DL.SetWindowText("blue", "95 PASS")
    else:
        DL.SetWindowText("red", "95 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9A03')):
        DL.SetWindowText("blue", "9A PASS")
    else:
        DL.SetWindowText("red", "9A FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9C01')):
        DL.SetWindowText("blue", "9C PASS")
    else:
        DL.SetWindowText("red", "9C FAIL")
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
        
    if (-1 != strCardData.find('9F0607')):
        DL.SetWindowText("blue", "9F06 PASS")
    else:
        DL.SetWindowText("red", "9F06 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F1A02')):
        DL.SetWindowText("blue", "9F1A PASS")
    else:
        DL.SetWindowText("red", "9F1A FAIL")
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
        
    if (-1 != strCardData.find('9F3303')):
        DL.SetWindowText("blue", "9F33 PASS")
    else:
        DL.SetWindowText("red", "9F33 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F3501')):
        DL.SetWindowText("blue", "9F35 PASS")
    else:
        DL.SetWindowText("red", "9F35 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F3704')):
        DL.SetWindowText("blue", "9F37 PASS")
    else:
        DL.SetWindowText("red", "9F37 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('500F505043204D43442030312020763230')):
        DL.SetWindowText("blue", "50 PASS")
    else:
        DL.SetWindowText("red", "50 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('8202')):
        DL.SetWindowText("blue", "82 PASS")
    else:
        DL.SetWindowText("red", "82 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('5F2403')):
        DL.SetWindowText("blue", "5F24 PASS")
    else:
        DL.SetWindowText("red", "5F24 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('5F2503')):
        DL.SetWindowText("blue", "5F25 PASS")
    else:
        DL.SetWindowText("red", "5F25 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('5F3401')):
        DL.SetWindowText("blue", "5F34 PASS")
    else:
        DL.SetWindowText("red", "5F34 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F0702')):
        DL.SetWindowText("blue", "9F07 PASS")
    else:
        DL.SetWindowText("red", "9F07 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F0902')):
        DL.SetWindowText("blue", "9F09 PASS")
    else:
        DL.SetWindowText("red", "9F09 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F10')):
        DL.SetWindowText("blue", "9F10 PASS")
    else:
        DL.SetWindowText("red", "9F10 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F1E08')):
        DL.SetWindowText("blue", "9F1E PASS")
    else:
        DL.SetWindowText("red", "9F1E FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F2608')):
        DL.SetWindowText("blue", "9F26 PASS")
    else:
        DL.SetWindowText("red", "9F26 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F2701')):
        DL.SetWindowText("blue", "9F27 PASS")
    else:
        DL.SetWindowText("red", "9F27 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F3403')):
        DL.SetWindowText("blue", "9F34 PASS")
    else:
        DL.SetWindowText("red", "9F34 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F3602')):
        DL.SetWindowText("blue", "9F36 PASS")
    else:
        DL.SetWindowText("red", "9F36 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F390107')):
        DL.SetWindowText("blue", "9F39 PASS")
    else:
        DL.SetWindowText("red", "9F39 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F530100')):
        DL.SetWindowText("blue", "9F53 PASS")
    else:
        DL.SetWindowText("red", "9F53 FAIL")
        DL.fails=DL.fails+1
    if(0 < (DL.fails + DL.warnings)):
        Result = False
        
    if (-1 != strCardData.find('9F6D02')):
        DL.SetWindowText("blue", "9F6D PASS")
    else:
        DL.SetWindowText("red", "9F6D FAIL")
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
