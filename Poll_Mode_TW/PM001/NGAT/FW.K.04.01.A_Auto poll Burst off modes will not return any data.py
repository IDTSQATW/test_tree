#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Auto Poll/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Auto Poll")
	DL.SendIOCommand("IDG", "01 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
DL.OpenDevice()	

DL.SetWindowText("black",'Please tap VISA card...')
time.sleep(8)
alldata = DL.GetResponse()	
DL.SetWindowText("black",'Card Data: ' + alldata)
if (alldata != ""):
	DL.SetWindowText("red","** FAIL: should not return data!!")

DL.SetWindowText("black",'Please tap MasterCard card...')
time.sleep(5)
alldata = DL.GetResponse()	
DL.SetWindowText("black",'Card Data: ' + alldata)
if (alldata != ""):
	DL.SetWindowText("red","** FAIL: should not return data!!")