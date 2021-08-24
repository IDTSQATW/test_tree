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
	
# Set group A0	
if (Result):
	DL.SetWindowText("black", "*** Set group A0")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 A0 9F 1E 08 00 00 00 00 00 00 00 00 9F 41 04 00 00 00 00 DF EE 5C 04 01 50 00 00 9C 01 00 5F 2A 02 08 40 9F 1A 02 08 40 5F 36 01 02 DF 81 22 05 F8 50 AC F8 00 DF 81 20 05 F8 50 AC A0 00 DF 81 21 05 00 00 00 00 00 DF 81 23 06 00 00 00 00 60 00 DF 81 26 06 00 00 00 00 80 00 9F 02 06 00 00 00 00 00 01 9F 03 06 00 00 00 00 00 00 9F 09 02 00 02 9F 15 02 00 00 9F 33 03 00 08 E8 9F 35 01 25 9F 40 05 60 00 00 30 00 9F 6D 01 C0 9F 6E 04 58 80 00 00 DF EE 34 06 00 00 00 01 00 00 DF EF 46 08 5F 24 5F 30 9F 41 9F 6E DF EF 4F 04 5F 30 9F 41 DF EF 4E 08 5F 24 5F 30 9F 41 9F 6E", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")		
	
# cmd 02-01
if (Result):
	DL.SetWindowText("black", "*** cmd 02-01, Please tap ApplePay AMEX card (PAN = xxxx....2212)..........")
	DL.SendIOCommand("IDG", "02 01 1E 9F 02 06 00 00 00 00 02 00", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 3C 42 33 37 30 32 39 35 37 35 37 31 36 30 39 35 35 5E 56 41 4C 55 45 44 20 43 55 53 54 4F 4D 45 52 20 20 20 20 20 20 ** 5E 32 30 30 37 37 32 38 ** 25 33 37 30 32 39 35 37 ** 3D 32 30 30 37 37 32 38 ** 00 00")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- track data was incorrect")
	alldata = DL.Get_RXResponse(0)
	DL.GetTLV(alldata,"9F39", 0)
	DL.GetTLV(alldata,"DFEE26", 0)
	DL.GetTLV(alldata,"FFEE01", 0)

	Result = DL.Check_RXResponse("9F 39 01 91")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag 9F39 was incorrect")

	Result = DL.Check_RXResponse("DF EE 26 02 31 00")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE26 was incorrect")

	Result = DL.Check_RXResponse("FF EE 01 ** DF EE 30 01 00")
	if Result != True:
		DL.SetWindowText("red", "FAIL -- Tag DFEE30 was incorrect")