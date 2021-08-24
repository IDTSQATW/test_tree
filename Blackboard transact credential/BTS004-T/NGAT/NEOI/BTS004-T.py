#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Data Encrypt disable
if (Result):
	RetOfStep = DL.SendCommand('Data Encrypt disable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Data encryption should be disabled...C7-37 = 00")

# Erase All Key
if (Result):
	RetOfStep = DL.SendCommand('Erase All Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("83 00 00 00")		
if (Result):
	RetOfStep = DL.SendCommand('Set DUKPT Key Encryption Type - TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Get account DUKPT encryption type (C7-33)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")	
if (Result):
	RetOfStep = DL.SendCommand('Load Plan Key 1')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("80 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Load Plan Key 2')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("80 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Load KPK')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("80 00 00 00")				
if (Result):
	RetOfStep = DL.SendCommand('Load Account key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("81 00 00 00")	
			
# (04-00) DFED3F Enable VAS Encryption
if (Result):
	RetOfStep = DL.SendCommand('(04-00) DFED3F Enable VAS Encryption')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# (04-00) DFEF4B Enable Transact Output
if (Result):
	RetOfStep = DL.SendCommand('(04-00) DFEF4B Enable Transact Output')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# Poll on demand
if (Result):
	RetOfStep = DL.SendCommand('Poll on demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")	

# Burst mode off	
if (Result):
	RetOfStep = DL.SendCommand('Burst mode off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			

# (C7-6B) Get the next DEK KSN
if (Result):
	RetOfStep = DL.SendCommand('(C7-6B) Get the next DEK KSN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 0A 62 99 49 01 2C 00 04 60 00 01")	
# (C7-6C) Set KTK Private Key KSN 01h	
if (Result):
	RetOfStep = DL.SendCommand('(C7-6C) Set KTK Private Key KSN 01h')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("c7 00 00 00")	
# (C7-67) Set Card Key - Take about 15 seconds	
if (Result):
	DL.SetWindowText("black", "(C7-67) Set Card Key - Take about 15 seconds")
	DL.SendIOCommand("IDG","C7 67 32 0D 3E A5 3A 36 89 86 D4 16 97 F0 04 62 BD F3 53 E4 EF 05 7F 79 60 B9 05 70 DB 45 C1 D5 47 A1 5B D5 E0 25 0F 25 BA EA E3 03 9A 01 08 1D 97 39 AE 09 0C AC C9 97 21 06 D3 5F C2 23 2C 2F 7F 51 25 74 80 82 B8 25 85 2B E8 FD 01 52 95 87 83 A2 19 80 68 0E 21 7A D7 B6 EB E7 49 0A 54 08 52 20 B2 0D 57 DB 37 86 A9 4A 09 07 50 FB F3 CA 8D 72 19 08 E9 41 93 1D D1 35 82 48 BF 0A 4A B7 C2 AA 73 85 A0 6E 90 35 5C 22 72 AB 5A 9E D6 30 CD A1 AA E1 24 53 E5 81 3B D5 5C 25 23 2C 4A B0 3F 8B 65 1A 5D 07 CB 58 06 ED 50 A8 A3 17 C3 D0 CC DD 7B D7 23 B9 9D A4 83 DA 98 D2 4C FA DE 0E E6 79 26 31 51 1A FF 44 2B 3F C1 D6 BA 0D 16 85 04 9E 27 8E 0A CC 5B 8E 85 CA 49 BD 8B 02 42 34 73 C5 A1 49 FA FA 1F 31 E4 3D C8 F3 F4 A1 D4 89 F1 AC A1 BA 70 16 11 56 EC FC 0F BB 15 19 24 26 B5 19 D9 23 72 3E FC 20 B3 E7 67 DF CE 94 6D 59 82 F5 86 E0 CA 64 2A 4C 78 B2 94 F0 24 CA 45 75 8D 87",17000) 
	
if (Result):
	for j in range (2, 8):
		if j == 2:
			RetOfStep = DL.SendCommand('(02-40 Apple VAS)')
		if j == 3:
			RetOfStep = DL.SendCommand('02-40 w/ AppleVAS -- VAS or PAY')
		if j == 4:
			RetOfStep = DL.SendCommand('02-40 w/ AppleVAS -- VAS and PAY')
		if j == 5:
			RetOfStep = DL.SendCommand('(02 40) SmartTap 2')
		if j == 6:
			RetOfStep = DL.SendCommand('02-40 w/ SmartTAP -- VAS or PAY')
		if j == 7:
			RetOfStep = DL.SendCommand('02-40 w/ SmartTAP -- VAS and PAY')		
			
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("02 00 ** 01")
			if (Result):
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"FFEE12")	
			
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C")
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				decDFEF4D = DL.DecryptDLL(0,1, strKey, ksn, encDFEF4D)	
				
				TagFFEE06 = DL.GetTLV(alldata,"FFEE06")
				TagFFEE08 = DL.GetTLV(alldata,"FFEE08")
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
				if j <= 4:
				# Tag FFEE06
					if TagFFEE06 != '':
						DL.SetWindowText("blue", "Tag FFEE06: PASS")
					else:
						DL.SetWindowText("red", "Tag FFEE06: FAIL")
				
				if j >= 5:
				# Tag FFEE08
					if TagFFEE08 != '':
						DL.SetWindowText("blue", "Tag FFEE08: PASS")
					else:
						DL.SetWindowText("red", "Tag FFEE08: FAIL")					
					
			# Tag DFEF4C-4D	
				Result = DL.Check_StringAB(TagDFEF4C, '00 00 00 00 10 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
				Result = DL.Check_StringAB(decDFEF4D, '39 39 39 38 38 38 31 32 33 34 35 36 37 38 39 31')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if (DL.Check_StringAB(Tag9F39, '07')): 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DF300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if (DL.Check_StringAB(TagDFEE26, '01')):
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				time.sleep(1)