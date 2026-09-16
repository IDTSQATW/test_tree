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
		
# (C7-6D) Del Key Block
RetOfStep = DL.SendCommand('(C7-6D) Del Key Block')
time.sleep(0.5)
        
# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 C7 00 00 01 00")
        
# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
		
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
	
if (Result):
	for j in range (1, 2):
		if j == 1:
			RetOfStep = DL.SendCommand('(02-40) Apple VAS (NEO2)')
			
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("02 57 ** 23")
			if (Result):
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
			
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C")
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				decDFEF4D = DL.DecryptDLL(0,2, strKey, ksn, encDFEF4D)	
				
				TagFFEE06 = DL.GetTLV(alldata,"FFEE06")
				TagFFEE08 = DL.GetTLV(alldata,"FFEE08")
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
				if j == 1:
				# Tag FFEE06
					if TagFFEE06 != '':
						DL.SetWindowText("blue", "Tag FFEE06: PASS")
					else:
						DL.SetWindowText("red", "Tag FFEE06: FAIL")
						DL.fails=DL.fails+1
						
				# Tag DFEF4C-4D	
					Result = DL.Check_StringAB(TagDFEF4C, '00 00 00 00 10 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
						DL.fails=DL.fails+1
									
					Result = DL.Check_StringAB(decDFEF4D, '39 39 39 38 37 38 30 30 31 30 30 30 32 33 32 38')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
						DL.fails=DL.fails+1
			# Tags 9F39/ FFEE01/ DFEE26
				if (DL.Check_StringAB(Tag9F39, '07')): 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
					DL.fails=DL.fails+1
				
				if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
					DL.fails=DL.fails+1
				
				if (DL.Check_StringAB(TagDFEE26, '2300')):
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					DL.fails=DL.fails+1
				time.sleep(1)
			else:
				DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1
                
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )