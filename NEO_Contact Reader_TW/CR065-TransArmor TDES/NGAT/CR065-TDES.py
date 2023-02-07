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

# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
	time.sleep(1)
	
# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")	
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

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
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")			
		
# cmd 60-10, insert card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(4)	
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
		
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
			# Tag 57
				Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(alldata, '57 A1 11'):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec57, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39 3F')
				if Result == True and DL.Check_StringAB(alldata, '57 C1 28'):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
				if Result == True and DL.Check_StringAB(alldata, '5A A1 08'):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec5A, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
				if Result == True and DL.Check_StringAB(alldata, '5A C1 10'):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 != "05": 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E406": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")

# cmd 60-11					
if  CTresultcode == "0010":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(2)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 != "05": 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E406": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				
# cmd 60-12
if  CTresultcode == "0004":
	Result = True
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(2)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
					
				# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 != "05": 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E406": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			