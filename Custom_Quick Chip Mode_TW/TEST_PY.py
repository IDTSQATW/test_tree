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

if (Result):       
    DL.SetWindowText("black", "*** Insert EMV T=0 card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
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
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)