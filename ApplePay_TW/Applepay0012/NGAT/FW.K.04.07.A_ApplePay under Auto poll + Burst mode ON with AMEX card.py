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
	
# Set group A0
if (Result):
	DL.SetWindowText("black", "*** Set group A0")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 A0 9F 1E 08 00 00 00 00 00 00 00 00 9F 41 04 00 00 00 00 DF EE 5C 04 01 50 00 00 9C 01 00 5F 2A 02 08 40 9F 1A 02 08 40 5F 36 01 02 DF 81 22 05 F8 50 AC F8 00 DF 81 20 05 F8 50 AC A0 00 DF 81 21 05 00 00 00 00 00 DF 81 23 06 00 00 00 00 60 00 DF 81 26 06 00 00 00 00 80 00 9F 02 06 00 00 00 00 00 01 9F 03 06 00 00 00 00 00 00 9F 09 02 00 02 9F 15 02 00 00 9F 33 03 00 08 E8 9F 35 01 25 9F 40 05 60 00 00 30 00 9F 6D 01 C0 9F 6E 04 58 80 00 00 DF EE 34 06 00 00 00 01 00 00 DF EF 46 08 5F 24 5F 30 9F 41 9F 6E DF EF 4F 04 5F 30 9F 41 DF EF 4E 08 5F 24 5F 30 9F 41 9F 6E", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
#########################################################################
	
if (Result):
	DL.OpenDevice()	

	DL.ShowMessageBox("Reader", "Please tap AMEX card (PAN = xxxx....2212) and then click OK")
	alldata = DL.GetResponse()	
	DL.SetWindowText("black",'Card Data: ' + alldata)
	Result = DL.Check_StringAB(alldata, '01 00 03 25 42 33 37 30 32 39 35 37 35 37 31 36 30 39 35 35 5E 56 41 4C 55 45 44 20 43 55 53 54 4F 4D 45 52 20 20 20 20 20 20')
	if Result == False:
		DL.SetWindowText("red","******* FAIL: data is incorrect!!")
	else:
		DL.SetWindowText("green","******* PASS: data is correct!!")