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
	
# 04-03 set g80 (DF811B =  00) (NEO2)
if (Result):
	DL.SetWindowText("black", "*** 04-03 set g80 (DF811B =  00) (NEO2)")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 80 9F 01 00 9F 1A 02 08 40 9F 1C 00 9F 1D 08 6C FF 00 00 00 00 00 00 5F 57 00 DF 60 00 DF 62 00 DF 63 00 DF 81 08 00 DF 81 09 00 DF 81 0A 00 DF 81 0D 00 DF 81 17 01 00 DF 81 18 01 60 DF 81 19 01 08 DF 81 1A 03 9F 6A 04 DF 81 1B 01 00 DF 81 1C 02 00 00 DF 81 1D 01 00 DF 81 1E 01 10 DF 81 1F 01 08 DF 81 20 05 00 00 00 00 00 DF 81 22 05 00 00 00 00 00 DF 81 21 05 00 00 00 00 00 DF 81 23 06 00 00 00 01 00 00 DF 81 24 06 00 00 00 03 00 00 DF 81 25 06 00 00 00 05 00 00 DF 81 26 06 00 00 00 00 10 00 DF 81 2C 01 00 9F 09 02 00 02 9F 15 02 11 11 9F 16 00 9F 1E 08 30 30 30 30 30 30 30 30 9F 33 00 9F 35 01 22 9F 40 05 00 00 00 00 00 9F 4E 00 9F 6D 02 00 01 9F 7E 00 DF EE 0F 01 01 DF EE 37 01 03 DF EE 38 01 00 9F 53 01 00 DF EF 46 02 9F 41 DF EF 4F 02 9F 41 DF EF 4E 02 9F 41", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
#########################################################################
	
if (Result):
	DL.OpenDevice()	

	DL.ShowMessageBox("Reader", "Please tap MasterCard (PAN = xxxx....1488) and then click OK")
	alldata = DL.GetResponse()	
	DL.SetWindowText("black",'Card Data: ' + alldata)
	Result = DL.Check_StringAB(alldata, '01 00 01')
	if Result == False:
		DL.SetWindowText("red","******* FAIL: data is incorrect!!")
	else:
		DL.SetWindowText("green","******* PASS: data is correct!!")