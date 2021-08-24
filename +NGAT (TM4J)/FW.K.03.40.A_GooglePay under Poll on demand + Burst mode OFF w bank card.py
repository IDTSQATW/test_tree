#!/usr/bin/env pythonF
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Poll On Demand/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Poll On Demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# Reset to default, cmd 04-09
if (Result):
	DL.SetWindowText("black", "*** Reset to default, cmd 04-09")
	DL.SendIOCommand("IDG", "04 09", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")		
	
# cmd 02-01
if (Result):
	DL.SetWindowText("black", "*** cmd 02-01, Please tap AndroidPay bank card..........")
	DL.SendIOCommand("IDG", "02 01 1E 9F 02 06 00 00 00 00 02 00", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- RX status code was incorrect")
	alldata = DL.Get_RXResponse(0)
	DL.GetTLV(alldata,"9F39", 0)
	DL.GetTLV(alldata,"DFEE26", 0)
	DL.GetTLV(alldata,"FFEE01", 0)

	Result = DL.Check_RXResponse("9F 39")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag 9F39 was incorrect")

	Result = DL.Check_RXResponse("DF EE 26")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE26 was incorrect")

	Result = DL.Check_RXResponse("FF EE 01 ** DF EE 30 01 00")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE30 was incorrect")