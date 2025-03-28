#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
CTresultcode = 0

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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")	
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# DFED59 =  00 (Send First Response 0x63)
if (Result):
	RetOfStep = DL.SendCommand('DFED59 =  00 (Send First Response 0x63)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (04)')
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
		
# 4C config (FastEMV ON) + cmd 60-10 (Normal)
# 4C config (FastEMV ON) + cmd 60-10 (FastEMV OFF)
if (Result):
	RetOfStep = DL.SendCommand('60-06 4C config - DFED46 = 0F (FastEMV ON)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
		
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('1. 60-10 Normal --1_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('1. 60-10 Normal --1_w/o LCD')
		rx = 8	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if lcdtype == 0:
			Result = Result and DL.Check_RXResponse(9, "61 01 ** 03 00 00 02 00 ** 03 00 ** 03 1C")
			if (Result):
				Result = Result and DL.Check_RXResponse(10, "61 01 ** 03 00 00 02 00 ** 03 00 ** 27 1C")
				if (Result):
					Result = Result and DL.Check_RXResponse(11, "61 01 ** 03 00 00 02 00 ** 03 00 ** 23 1C")
		if (Result) and CTresultcode == "0003":
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				DL.SetWindowText("blue", "FastEMV: PASS")
			else:
				DL.SetWindowText("red", "FastEMV: FAIL")

			if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
				DL.SetWindowText("Red", "Tag 9F39: FAIL")	
			if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
				DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
			if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")				

if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('3. 60-10 FastEMV OFF_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('3. 60-10 FastEMV OFF_w/o LCD')	
		rx = 7
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
		
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
		
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
		
			# Tag 57
				Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_RXResponse(rx, '57 A1 11'):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
				if Result == True and DL.Check_RXResponse(rx, '57 C1 20'):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
				if Result == True and DL.Check_RXResponse(rx, '5A A1 08'):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
				if Result == True and DL.Check_RXResponse(rx, '5A C1 10'):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
if  CTresultcode == "0010":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')	
		rx = 3
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):					
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
if  CTresultcode == "0004":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/ LCD')
		rx = 1		
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')	
		rx = 2
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):								
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
					
# 4C config (FastEMV OFF) + cmd 60-10 (Normal)
# 4C config 4C config (FastEMV OFF) + cmd 60-10 (FastEMV ON)
if (Result):
	RetOfStep = DL.SendCommand('60-06 4C config - DFED46 = 0E (FastEMV OFF)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	

if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('1. 60-10 Normal --2_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('1. 60-10 Normal --2_w/o LCD')	
		rx = 7	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
		
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
		
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
		
			# Tag 57
				Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_RXResponse(rx, '57 A1 11'):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
				if Result == True and DL.Check_RXResponse(rx, '57 C1 20'):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
				if Result == True and DL.Check_RXResponse(rx, '5A A1 08'):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
				if Result == True and DL.Check_RXResponse(rx, '5A C1 10'):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
if  CTresultcode == "0010":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')	
		rx = 3	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):						
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
if  CTresultcode == "0004":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/ LCD')
		rx = 1		
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')	
		rx = 2	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):								
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")	
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		

if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('2. 60-10 FastEMV ON_w/ LCD')
		rx = 1
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('2. 60-10 FastEMV ON_w/o LCD')
		rx = 8	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(rx)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if lcdtype == 0:
			Result = Result and DL.Check_RXResponse(9, "61 01 ** 03 00 00 02 00 ** 03 00 ** 03 1C")
			if (Result):
				Result = Result and DL.Check_RXResponse(10, "61 01 ** 03 00 00 02 00 ** 03 00 ** 27 1C")
				if (Result):
					Result = Result and DL.Check_RXResponse(11, "61 01 ** 03 00 00 02 00 ** 03 00 ** 23 1C")		
		if (Result) and CTresultcode == "0003":
			Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				DL.SetWindowText("blue", "FastEMV: PASS")
			else:
				DL.SetWindowText("red", "FastEMV: FAIL")
				
			if DL.Check_RXResponse(rx, "9F39 01 05") == False: 
				DL.SetWindowText("Red", "Tag 9F39: FAIL")	
			if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
				DL.SetWindowText("Red", "Tag FFEE01: FAIL")		
			if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")		