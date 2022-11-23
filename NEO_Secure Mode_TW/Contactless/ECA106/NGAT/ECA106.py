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
	DL.SendIOCommand("IDG", "04 00 DF EE 38 01 01 DF EE 44 02 FF FF DF EE 34 06 00 00 00 03 00 00 5F 2A 02 01 56 DF ED 5B 04 01 06 00 08 DF ED 5A 08 01 00 00 00 00 00 00 00 DF EE 0C 01 08 DF EE 6B 08 54 65 72 6D 30 30 30 30", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# Set Configurable Group
if (Result):
	DL.SetWindowText("black", "*** Set Configurable Group")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 A0 DF 81 26 06 00 00 00 01 20 00 DF EE 34 06 00 00 00 03 00 00 9F 1B 04 00 00 3A 98 9F 66 04 37 00 40 80 9F 33 03 00 68 C8 9F 4E 14 42 61 6E 6B 54 65 73 74 20 20 20 20 20 20 20 20 20 20 30 31 9F 09 02 00 30 9F 1A 02 01 56 5F 2A 02 01 56 9F 16 0F 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 9F 35 01 25 9C 01 00 DF EE 6B 08 54 65 72 6D 30 30 30 30", 3000, 1) 
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
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 A0 9F 06 07 A0 00 00 03 33 01 01 DF EE 4B 01 01 DF EE 4D 01 54 DF EE 2E 01 10 DF EE 54 0C 07 00 A0 07 01 A0 07 09 A0 07 20 A0 DF EE 59 01 07 DF EE 53 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 A0 9F 06 08 A0 00 00 03 33 01 01 01 DF EE 4B 01 01 DF EE 4D 01 54 DF EE 2E 01 10 DF EE 54 0C 07 00 A0 07 01 A0 07 09 A0 07 20 A0 DF EE 59 01 07 DF EE 53 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 A0 9F 06 08 A0 00 00 03 33 01 01 02 DF EE 4B 01 01 DF EE 4D 01 54 DF EE 2E 01 10 DF EE 54 0C 07 00 A0 07 01 A0 07 09 A0 07 20 A0 DF EE 59 01 07 DF EE 53 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# Contact Set ICS Identification (60-16)
if (Result):
	DL.SetWindowText("black", "*** Contact Set ICS Identification (60-16)")
	DL.SendIOCommand("IDG", "60 16 01", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")		
	
# Contact Set Application Data (60-03)
if (Result):
	DL.SetWindowText("black", "*** Contact Set Application Data (60-03)")
	DL.SendIOCommand("IDG", "60 03 05 00 A0 00 00 03 33 14 00 9F 01 06 01 23 45 67 89 10 5F 57 01 00 5F 2A 02 08 40 9F 09 02 00 96 5F 36 01 02 9F 15 02 12 34 9F 1C 08 46 72 6F 6E 74 31 32 33 9F 4E 06 53 48 4F 50 20 31 9F 1B 04 00 00 3A 98 9F 3C 02 08 40 9F 3D 01 02 DF 25 03 9F 37 04 DF 28 03 9F 08 02 DF EE 15 01 01 DF 13 05 00 00 00 00 00 DF 14 05 FF FF FF FF FF DF 15 05 00 00 00 00 00 DF 18 01 00 DF 17 04 00 00 27 10 DF 19 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# Contact Set Terminal Data (60-06)
if (Result):
	DL.SetWindowText("black", "*** Contact Set Terminal Data (60-06)")
	DL.SendIOCommand("IDG", "60 06 18 00 5F 36 01 02 9F 1A 02 08 40 9F 35 01 22 9F 33 03 60 F8 C8 9F 40 05 F0 00 F0 A0 01 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF 26 01 01 DF 10 08 65 6E 66 72 65 73 7A 68 DF 11 01 01 DF 27 01 00 DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1E 08 F0 DC 3C F0 C2 9E 94 00 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 20 01 3C DF EE 21 01 0A DF EE 22 03 32 3C 3C", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

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
		if DL.Check_RXResponse(rx, '57A1136228CCCCCCCC1117D2012CCCCCCCCCCCCCCCCC') == False:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
		if DL.Check_StringAB(dec57, '57136228000100001117D20121200012339900031F0000000000000000000000') == False:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		# 5A
		DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
		mask5A = DL.GetTLV(TagFF8105,"5A", 0)
		enc5A = DL.GetTLV(TagFF8105,"5A", 1)
		DL.SetWindowText("blue", "Tag 5A Decryption data:")
		dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)	
		if DL.Check_RXResponse(rx, '5AA108 6228CCCCCCCC1117') == False:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
		if DL.Check_StringAB(dec5A, '5A086228000100001117000000000000') == False:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")

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