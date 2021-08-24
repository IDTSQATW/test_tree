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
	
# 04-03 set g80 (DF811B =  00)
if (Result):
	DL.SetWindowText("black", "*** 04-03 set g80 (DF811B =  00)")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 80 9F 01 00 9F 1A 02 08 40 9F 1C 00 9F 1D 08 6C FF 00 00 00 00 00 00 5F 57 00 DF 60 00 DF 62 00 DF 63 00 DF 81 08 00 DF 81 09 00 DF 81 0A 00 DF 81 0D 00 DF 81 17 01 00 DF 81 18 01 60 DF 81 19 01 08 DF 81 1A 03 9F 6A 04 DF 81 1B 01 00 DF 81 1C 02 00 00 DF 81 1D 01 00 DF 81 1E 01 10 DF 81 1F 01 08 DF 81 20 05 00 00 00 00 00 DF 81 22 05 00 00 00 00 00 DF 81 21 05 00 00 00 00 00 DF 81 23 06 00 00 00 01 00 00 DF 81 24 06 00 00 00 03 00 00 DF 81 25 06 00 00 00 05 00 00 DF 81 26 06 00 00 00 00 10 00 DF 81 2C 01 00 9F 09 02 00 02 9F 15 02 11 11 9F 16 00 9F 1E 08 30 30 30 30 30 30 30 30 9F 33 00 9F 35 01 22 9F 40 05 00 00 00 00 00 9F 4E 00 9F 6D 02 00 01 9F 7E 00 DF EE 0F 01 01 DF EE 37 01 03 DF EE 38 01 00 9F 53 01 00 DF EF 46 02 9F 41 DF EF 4F 02 9F 41 DF EF 4E 02 9F 41", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")		
	
# cmd 02-01
if (Result):
	DL.SetWindowText("black", "*** cmd 02-01, Please tap ApplePay MasterCard card (PAN = xxxx....1488)..........")
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

	Result = DL.Check_RXResponse("DF EE 26 02")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE26 was incorrect")

	Result = DL.Check_RXResponse("FF EE 01 ** DF EE 30 01 00")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE30 was incorrect")