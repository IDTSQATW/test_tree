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

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
# Poll on demand		
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
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
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
				
		if lcdtype == 1:					
			RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
			rx = 1
		if lcdtype == 0:
			RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')	
			rx = 5
		if (RetOfStep):
			Result = DL.Check_RXResponse("60 63 00 00")
			alldata = DL.Get_RXResponse(rx)
			CTresultcode = DL.GetTLV(alldata,"DFEE25")
			if (Result):
				Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')
				if (Result):
					ksn = DL.GetTLV(alldata,"DFEE12")	
				
					TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
					encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
					decDFEF4D = DL.DecryptDLL(0,1, strKey, ksn, encDFEF4D)	
				
				#1 Tag DFEF4C-4D	
					if i == 1:
						if TagDFEF4C == "" or TagDFEF4C == "000000000000":
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						if encDFEF4D == "":
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
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), 'DF EF 4D 28'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
				#3 Tag DFEF4C-4D	
					if i == 3:
						if TagDFEF4C == "" or TagDFEF4C == "000000000000":
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						if encDFEF4D == "":
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
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), 'DF EF 4D 28'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
				#5 Tag DFEF4C-4D	
					if i == 5:
						if TagDFEF4C == "" or TagDFEF4C == "000000000000":
							DL.SetWindowText("blue", "Tag DFEF4C: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
						if encDFEF4D == "":
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
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), 'DF EF 4D 28'):
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
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), 'DF EF 4D 28'):
							DL.SetWindowText("blue", "Tag DFEF4D: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF4D: FAIL")							
			# cmd 60-11					
			if  CTresultcode == "0010":
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w LCD')
					rx = 1
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')
					rx = 2
				if (RetOfStep):
					Result = DL.Check_RXResponse("60 63 00 00")
					alldata = DL.Get_RXResponse(rx)
					CTresultcode = DL.GetTLV(alldata,"DFEE25")	
					if (Result):
						Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')
								
			# cmd 60-12
			if  CTresultcode == "0004":
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w LCD')
					rx = 1
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')
					rx = 2
				if (RetOfStep):
					Result = DL.Check_RXResponse("60 63 00 00")
					alldata = DL.Get_RXResponse(rx)
					CTresultcode = DL.GetTLV(alldata,"DFEE25")
					if (Result):
						Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')	