#!/usr/bin/env python
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
	
# NEO2 CT config
if (Result):
	DL.SetWindowText("black", "*** 60-06 4C config")
	DL.SendIOCommand("IDG", "60 06 18 00 5F 36 01 02 9F 1A 02 08 40 9F 35 01 25 9F 33 03 60 08 C8 9F 40 05 60 00 F0 50 01 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF 26 01 01 DF 10 08 65 6E 66 72 65 73 7A 68 DF 11 01 01 DF 27 01 00 DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1E 08 D0 9C 20 F0 C2 0E 14 00 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 30 35 30 30 DF EE 20 01 3C DF EE 21 01 0A DF EE 22 03 32 3C 3C", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** 60-03 Contact Set Application Data (VISA)")
	DL.SendIOCommand("IDG", "60 03 07 00 A0 00 00 00 03 10 10 0F 00 9F 01 06 56 49 53 41 30 30 5F 57 01 00 5F 2A 02 08 40 9F 09 02 00 96 5F 36 01 02 9F 1B 04 00 00 3A 98 DF 25 03 9F 37 04 DF 28 03 9F 08 02 DF EE 15 01 01 DF 13 05 00 00 00 00 00 DF 14 05 00 00 00 00 00 DF 15 05 00 00 00 00 00 DF 18 01 00 DF 17 04 00 00 27 10 DF 19 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** First response control = Send First Response 0x63")
	DL.SendIOCommand("IDG", "04 00 DF ED 59 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")
	
########################################################################################	

# cmd 02-40 w/ tag_MSR only
if (Result):
	DL.SetWindowText("black", "*** cmd 02-40, Please TAP card -> SWIPE card..........")
	DL.SendIOCommand("IDG", "02 40 0A 9F 02 06 00 00 00 00 10 00 DF EF 37 01 01", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00")
if (Result):
	readercheck = DL.ShowMessageBox("Reader", "Does LCD/ LED indicate this transaction for MSR ONLY?", 0)
	if readercheck == 0:
		DL.SetWindowText("red", "****** FAIL: reader status was incorrect!!")
		
# cmd 02-40 w/ tag_CL only
if (Result):
	DL.SetWindowText("black", "*** cmd 02-40, Please SWIPE card -> TAP card..........")
	DL.SendIOCommand("IDG", "02 40 0A 9F 02 06 00 00 00 00 10 00 DF EF 37 01 02", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
if (Result):
	readercheck = DL.ShowMessageBox("Reader", "Does LCD/ LED indicate this transaction for CL ONLY?", 0)
	if readercheck == 0:
		DL.SetWindowText("red", "****** FAIL: reader status was incorrect!!")
		
# cmd 02-40 w/ tag_CT only
if (Result):
	DL.SetWindowText("black", "*** cmd 60-10, Please TAP card -> INSERT card (EMV Test Card V2 T=0)..........")
	DL.SendIOCommand("IDG", "02 40 3C 9F 02 06 00 00 00 00 10 00 DF EF 37 01 04 DF EF 3C 03 01 00 60", 32000, 2) 
	Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EE 25 02 00 10')
	if (Result):
		DL.SetWindowText("black", "*** 60-11 CT Authenticate Transaction (NEO)..........")
		DL.SendIOCommand("IDG", "60 11 00 00 78", 32000, 2) 
		Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EE 25 02 00 04')
		if (Result):
			DL.SetWindowText("black", "*** 60-12 CT Apply Host Response (NEO)..........")
			DL.SendIOCommand("IDG", "60 12 01 8A 02 30 30 91 0A 11 22 33 44 55 66 77 88 30 30", 32000, 2) 
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EE 25 02 00 02')
if (Result):
	readercheck = DL.ShowMessageBox("Reader", "Does LCD/ LED indicate this transaction for CT ONLY?", 0)
	if readercheck == 0:
		DL.SetWindowText("red", "****** FAIL: reader status was incorrect!!")