#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Pass-through mode OFF
if (Result):
	DL.SetWindowText("black", "*** Pass-through mode OFF")
	DL.SendIOCommand("IDG", "2C 01 00", 3000, 1) 
	time.sleep(1)

# Auto Poll/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Auto Poll")
	DL.SendIOCommand("IDG", "01 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# Set Configuration Global On (NEO2)
if (Result):
	DL.SetWindowText("black", "*** Set Configuration Global On")
	DL.SendIOCommand("IDG", "04 00 DF EE 7C 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# Activate Transaction >>> Mifare Ultralight
if (Result):
	DL.OpenDevice()
	DL.ShowMessageBox("Reader", "Place Mifare Ultralight card on reader --> Click OK", 0)	
	time.sleep(1)
	DL.SetWindowText("black", "*** Mifare Ultralight..........")
	alldata = DL.GetResponse()	
	DL.SetWindowText("black",'RX: ' + alldata)
	Result = DL.Check_StringAB(alldata, '05 50 00')
	
	if Result == False:
		DL.SetWindowText("red","** FAIL: can not auto switch!!")
	else:
		DL.SetWindowText("black", "*** >>> Buzzer >>> Poll For Token >>> PT Stop..........")
		DL.SendIOCommand("IDG", "0B 02 00", 32000, 1) 
		Result = DL.Check_RXResponse("0B 00 00 00")
		if (Result):
			DL.SendIOCommand("IDG", "2C 02 00 C8", 32000, 1) 
			Result = DL.Check_RXResponse("2C 00")	
			if (Result):
				DL.ShowMessageBox("Reader", "Remove card --> Click OK", 0)
				DL.SendIOCommand("IDG", "2C 01 00", 32000, 1) 
				Result = DL.Check_RXResponse("2C 00")				

# Activate Transaction 1 >>> VISA
if (Result):
	DL.ShowMessageBox("Reader", "Click OK --> Place VISA card on reader", 0)

	# cmd 02-40		
	if (Result):
		DL.SetWindowText("black", "*** cmd 02-40, VISA..........")
		DL.SendIOCommand("IDG", "02 40 0A 9F 02 06 00 00 00 00 10 01 5F 2A 02 08 40 9A 03 11 09 27 9F 21 03 10 15 20 9F 1A 02 00 56 9C 01 00", 32000, 1) 
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
					
# Activate Transaction 2 >>> VISA
if (Result):
	DL.ShowMessageBox("Reader", "Click OK --> Place VISA card on reader", 0)

	# cmd 02-40		
	if (Result):
		DL.SetWindowText("black", "*** cmd 02-40, VISA..........")
		DL.SendIOCommand("IDG", "02 40 0A 9F 02 06 00 00 00 00 00 01 5F 2A 02 09 78 9A 03 11 09 27 9F 21 03 10 15 20 9F 1A 02 00 56 9C 01 00", 32000, 1) 
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
		
# Set Configuration Global Off (NEO2)
if (Result):
	DL.SetWindowText("black", "*** Set Configuration Global Off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7C 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")		

# Pass-through mode OFF
if (Result):
	DL.SetWindowText("black", "*** Pass-through mode OFF")
	DL.SendIOCommand("IDG", "2C 01 00", 3000, 1) 
	time.sleep(1)	