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

# Enable encryption (03)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (03)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")		
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap card
if (Result):
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** F1 FF EE 12")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"FFEE12")	
		
		maskFFEE13 = DL.GetTLV(alldata,"FFEE13", 0)
		encFFEE13 = DL.GetTLV(alldata,"FFEE13", 1)
		decFFEE13 = DL.DecryptDLL(0,1, strKey, ksn, encFFEE13)	
		
		maskFFEE14 = DL.GetTLV(alldata,"FFEE14", 0)
		encFFEE14 = DL.GetTLV(alldata,"FFEE14", 1)
		decFFEE14 = DL.DecryptDLL(0,1, strKey, ksn, encFFEE14)	
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
	# Tag FFEE13
		Result = DL.Check_StringAB(maskFFEE13, '2A 34 37 36 31 2A 2A 2A 2A 2A 2A 2A 2A 30 30 31 30 5E 46 55 4C 4C 2F 46 55 4E 43 54 49 4F 4E 41 4C 5E 32 30 31 32 31 32 30 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if Result == True and DL.Check_RXResponse("FF EE 13 A1 4C"):
			DL.SetWindowText("blue", "Tag FFEE13_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag FFEE13_Mask: FAIL")
			
		Result = DL.Check_StringAB(decFFEE13, 'FF EE 13 4C 42 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 5E 46 55 4C 4C 2F 46 55 4E 43 54 49 4F 4E 41 4C 5E 32 30 31 32 31 32 30 30 30 31 32 33 30 31 30 32 30 33 30 34 30 35 30 36 30 37 30 38 30 39 31 30 30 33 39 39 30 33 30 30 30 30')
		if Result == True and DL.Check_RXResponse("FF EE 13 C1"):
			DL.SetWindowText("blue", "Tag FFEE13_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag FFEE13_Enc: FAIL")

	# Tag FFEE14
		Result = DL.Check_StringAB(maskFFEE14, '34 37 36 31 2A 2A 2A 2A 2A 2A 2A 2A 30 30 31 30 3D 32 30 31 32 31 32 30 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if Result == True and DL.Check_RXResponse("FF EE 14 A1 25"):
			DL.SetWindowText("blue", "Tag FFEE14_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag FFEE14_Mask: FAIL")
			
		Result = DL.Check_StringAB(decFFEE14, 'FF EE 14 25 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31')
		if Result == True and DL.Check_RXResponse("FF EE 14 C1"):
			DL.SetWindowText("blue", "Tag FFEE14_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag FFEE14_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if Tag9F39 == "91": 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if (DL.Check_StringAB(TagFFEE01, "DF300100")): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if TagDFEE26 == "F100": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")