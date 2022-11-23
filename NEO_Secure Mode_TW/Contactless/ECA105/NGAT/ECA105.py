#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'
rx = 0

#Objective: to verify AES DUKPT Management, AES-128 Working Key encryption/ decryption function

# Set Configuration
if (Result):
	DL.SetWindowText("black", "*** Set Configuration")
	DL.SendIOCommand("IDG", "04 00 DF EE 44 02 FF FF DF EE 37 01 03 DF EE 0C 01 09 DF ED 66 04 F9 C0 00 09 5F 2A 02 03 92", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# Set Configurable Group
if (Result):
	DL.SetWindowText("black", "*** Set Configurable Group")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 D0 DF EF 44 02 7F 00 DF 81 23 06 00 00 00 00 45 00 DF EE 34 06 00 00 00 02 00 00 DF 81 26 06 00 00 00 01 00 00 DF EE 2B 01 00 DF EF 45 02 10 00 DF EE 2C 01 00 DF 81 20 05 90 40 00 80 00 DF 81 21 05 04 10 00 00 00 DF 81 22 05 90 60 00 90 00 9F 53 03 70 00 00 DF EE 2A 06 00 00 00 00 20 00 9F 01 06 00 00 00 00 00 10 9F 15 02 70 32 9F 4E 17 58 58 20 4D 45 52 43 48 41 4E 54 20 59 59 20 4C 4F 43 41 54 49 4F 4E 9F 1A 02 03 92 9F 35 01 22 5F 2A 02 03 92 5F 36 01 02 9F 40 05 F0 00 F0 30 01 DF EF 19 04 00 00 00 3C", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")

# Delete Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Delete Configurable AID")
	DL.SendIOCommand("IDG", "04 04 9F 06 06 A0 00 00 00 25 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")

if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 04 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 04 30 60", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 20 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 30 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 65 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 03 24 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 02 77 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 01 52 30 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 80 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 03 33 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 08 A0 00 00 03 33 01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 08 A0 00 00 03 33 01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 09 A0 00 00 04 76 D0 00 01 11", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 D0 9F 06 07 A0 00 00 00 65 20 20 DF EE 53 01 02 DF EE 4B 01 01 DF EE 2E 01 10 DF EE 54 0C 05 00 D0 05 01 D0 05 09 D0 05 20 D0 DF EE 59 01 05 DF EE 4D 01 54 DF EE 4C 01 0E", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 D0 9F 06 07 A0 00 00 00 65 10 10 DF EE 53 01 02 DF EE 4B 01 01 DF EE 2E 01 10 DF EE 54 06 05 00 D0 05 01 D0 DF EE 59 01 05 DF EE 4D 01 54 DF EF 2C 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# CL test
if (Result):
	RetOfStep = DL.SendCommand('02-40 (enable CL only)')
	rx = 4 # for VP3350
	if (RetOfStep):
		DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 ** DF EE 12")
		alldata = DL.Get_RXResponse(rx)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		TagFF8105 = DL.GetTLV(alldata,"FF8105")
		# 57
		DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
		mask57 = DL.GetTLV(TagFF8105,"57", 0)
		enc57 = DL.GetTLV(TagFF8105,"57", 1)
		DL.SetWindowText("blue", "Tag 57 Decryption data:")
		dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)	
		if DL.Check_RXResponse(rx, '57A1133540CCCCCCCC1012D4912CCCCCCCCCCCCCCCCC') == False:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
		if DL.Check_StringAB(dec57, '57133540829999421012D49122015555555555551F0000000000000000000000') == False:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")

		# Tags 9F39/ DFEE26
		if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		if DL.Check_RXResponse(rx, "DFEE26 02 E301") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
# cmd 03-03
if (Result):
	DL.SetWindowText("black", "*** cmd 03-03, Approve")
	DL.SendIOCommand("IDG", "03 03 00 E3 00 06 31 32 33 34 35 36 9A 03 15 07 30 9F 21 03 10 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("03 00 00 00")				