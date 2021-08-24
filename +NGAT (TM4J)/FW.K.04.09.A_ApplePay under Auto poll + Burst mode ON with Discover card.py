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
	
# Set group B0 (9F66 = 80 00 40 00)
if (Result):
	DL.SetWindowText("black", "*** Set group B0 (9F66 = 80 00 40 00)")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 B0 9C 01 00 5F 2A 02 08 40 5F 36 01 02 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 9F 09 02 01 00 9F 1A 02 08 40 9F 1B 04 00 00 00 00 9F 33 03 00 08 08 9F 35 01 25 9F 66 04 80 00 40 00 DF EE 74 01 03 DF EE 34 06 00 00 00 03 00 00 DF EE 35 03 03 07 01 DF 81 26 06 00 00 00 00 20 00 DF 81 22 05 FC E0 9C F8 00 DF 81 20 05 DC 00 00 20 00 DF 81 21 05 01 10 00 00 00 DF 81 23 06 00 00 00 00 00 00 DF 81 24 06 00 00 00 03 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
#########################################################################
	
if (Result):
	DL.OpenDevice()	

	DL.ShowMessageBox("Reader", "Please tap Discover (PAN = xxxx....8741) and then click OK")
	alldata = DL.GetResponse()	
	DL.SetWindowText("black",'Card Data: ' + alldata)
	Result = DL.Check_StringAB(alldata, '01 00 04 25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 31 38 5E 44 6F 6E 61 6C 64 20 45 20 41 76 65 72 69 6C 6C 20 20 20 20 20 20 20 20 20 20 5E 32 31 30 31 32 39 31 30 31 30 30 31')
	if Result == False:
		DL.SetWindowText("red","******* FAIL: data is incorrect!!")
	else:
		DL.SetWindowText("green","******* PASS: data is correct!!")