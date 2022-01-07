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
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
#########################################################################
	
if (Result):
	DL.OpenDevice()	

	DL.ShowMessageBox("Reader", "Please tap VISA card (PAN = xxxx....0492) and then click OK")
	alldata = DL.GetResponse()	
	DL.SetWindowText("black",'Card Data: ' + alldata)
	Result = DL.Check_StringAB(alldata, '03 00 02')
	if Result == False:
		DL.SetWindowText("red","******* FAIL: data is incorrect!!")
	else:
		DL.SetWindowText("green","******* PASS: data is correct!!")