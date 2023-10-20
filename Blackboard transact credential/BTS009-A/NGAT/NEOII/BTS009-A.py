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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")
		if Result != True:
			DL.SetWindowText("red", "Data encryption should be enabled...C7-37 = 03")
		
# Get account DUKPT encryption type (C7-33)
if (Result):
	RetOfStep = DL.SendCommand('Get account DUKPT encryption type (C7-33)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")
		if Result == False:
			DL.SetWindowText("red", "Data key should be AES type...C7-33 = 01")

# (C7-6A) Get BlackBoard Private Key Hash
if (Result):
	RetOfStep = DL.SendCommand('(C7-6A) Get BlackBoard Private Key Hash')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 20")
		if Result == False:
			DL.SetWindowText("red", "Reader should load BlackBoard Private Key first...")

# (C7-6A) Get BlackBoard LTPK Hash
if (Result):
	RetOfStep = DL.SendCommand('(C7-6A) Get BlackBoard LTPK Hash')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 20")	
		if Result == False:
			DL.SetWindowText("red", "Reader should load BlackBoard LTPK first...")	
			
# (04-00) DFED3F disable VAS Encryption
if (Result):
	RetOfStep = DL.SendCommand('(04-00) DFED3F disable VAS Encryption')
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
	
if (Result):
	for j in range (1, 5):
		if j == 1:
			RetOfStep = DL.SendCommand('02-40 w/ AppleVAS -- VAS or PAY')
		if j == 2:
			RetOfStep = DL.SendCommand('02-40 w/ AppleVAS -- VAS and PAY')
		if j == 3:
			RetOfStep = DL.SendCommand('02-40 w/ SmartTAP -- VAS or PAY')
		if j == 4:
			RetOfStep = DL.SendCommand('02-40 w/ SmartTAP -- VAS and PAY')		
			
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("02 57 ** E3")
			if (Result):
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
			
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C")
				TagDFEF4D = DL.GetTLV(alldata,"DFEF4D")
				
				TagFFEE06 = DL.GetTLV(alldata,"FFEE06")
				TagFFEE08 = DL.GetTLV(alldata,"FFEE08")
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
				if j <= 2:
				# Tag FFEE06
					if TagFFEE06 != '':
						DL.SetWindowText("blue", "Tag FFEE06: PASS")
					else:
						DL.SetWindowText("red", "Tag FFEE06: FAIL")
						
				# Tag DFEF4C-4D	
					Result = DL.Check_StringAB(TagDFEF4C, '00 00 00 00 10 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
									
					Result = DL.Check_StringAB(TagDFEF4D, '39 39 39 38 37 38 30 30 31 30 30 30 32 33 32 38')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")						
				if j >= 3:
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
									
					Result = DL.Check_StringAB(TagDFEF4D, '39 39 39 38 37 38 30 30 31 30 30')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")										
			# Tags 9F39/ FFEE01/ DFEE26
				if (DL.Check_StringAB(Tag9F39, '07')): 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if (DL.Check_StringAB(TagDFEE26, 'E300')):
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				time.sleep(1)