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

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")		
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# First response control = Send First Response 0x63
if (Result):
	RetOfStep = DL.SendCommand('First response control = Send First Response 0x63')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00")			
		
# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (23)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")			

		
# cmd 60-10, insert card
if (Result):
	for i in range(1, 8):
		if i == 1:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 1')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 2:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 2')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 3:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 3')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 4:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 4')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 5:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 5')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 6:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 6')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")
		if i == 7:
			RetOfStep = DL.SendCommand('60-06 -----DFEF4B 7')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 00 00 00")			
							
		RetOfStep = DL.SendCommand('Activate Transaction')
		if (RetOfStep):
			Result = DL.Check_RXResponse("60 63 00 00")
			alldata = DL.Get_RXResponse(1)
			CTresultcode = DL.GetTLV(alldata,"DFEE25")
			if (Result):
				Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
				if (Result):
					ksn = DL.GetTLV(alldata,"DFEE12")	
				
					TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
					encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
					decDFEF4D = DL.DecryptDLL(0,2, strKey, ksn, encDFEF4D)	
				
				#1 Tag DFEF4C-4D	
					if i == 1:
						Result = DL.Check_StringAB(TagDFEF4C, '00 22 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
				
				#2 Tag DFEF4C-4D	
					if i == 2:
						Result = DL.Check_StringAB(TagDFEF4C, '00 24 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39 3F')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
				#3 Tag DFEF4C-4D	
					if i == 3:
						Result = DL.Check_StringAB(TagDFEF4C, '00 22 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
				#4 Tag DFEF4C-4D	
					if i == 4:
						Result = DL.Check_StringAB(TagDFEF4C, '00 24 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39 3F')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
				#5 Tag DFEF4C-4D	
					if i == 5:
						Result = DL.Check_StringAB(TagDFEF4C, '00 22 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#6 Tag DFEF4C-4D	
					if i == 6:
						Result = DL.Check_StringAB(TagDFEF4C, '00 24 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39 3F')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#7 Tag DFEF4C-4D	
					if i == 7:
						Result = DL.Check_StringAB(TagDFEF4C, '00 24 00 00 00 00')
						if Result == True:
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39 3F')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), 'DF EF 4D 30'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")						
			# cmd 60-11					
			if  CTresultcode == "0010":
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction')
				if (RetOfStep):
					Result = DL.Check_RXResponse("60 63 00 00")
					alldata = DL.Get_RXResponse(1)
					CTresultcode = DL.GetTLV(alldata,"DFEE25")	
					if (Result):
						Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
								
			# cmd 60-12
			if  CTresultcode == "0004":
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response')
				if (RetOfStep):
					Result = DL.Check_RXResponse("60 63 00 00")
					alldata = DL.Get_RXResponse(1)
					CTresultcode = DL.GetTLV(alldata,"DFEE25")
					if (Result):
						Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')	