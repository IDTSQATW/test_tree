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

# Enable encryption (02)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")

# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")		

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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 73 DF EE 12")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		
		maskDFEF17 = DL.GetTLV(alldata,"DFEF17", 0)
		encDFEF17 = DL.GetTLV(alldata,"DFEF17", 1)
		decDFEF17 = DL.DecryptDLL(0,2, strKey, ksn, encDFEF17)	
		
		maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
		encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
		decDFEF18 = DL.DecryptDLL(0,2, strKey, ksn, encDFEF18)	
		
		FF8105 = DL.GetTLV(alldata,"FF8105", 0)
		mask56 = DL.GetTLV(FF8105,"56", 0)
		enc56 = DL.GetTLV(FF8105,"56", 1)
		dec56 = DL.DecryptDLL(0,2, strKey, ksn, enc56)	
		
		mask57 = DL.GetTLV(FF8105,"57", 0)
		enc57 = DL.GetTLV(FF8105,"57", 1)
		dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
	# Tag DFEF17
		r1 = DL.Check_StringAB(maskDFEF17, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
		r2 = DL.Check_StringAB(maskDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
		r3 = DL.Check_StringAB(maskDFEF17, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse("DF EF 17 A1 41"):
			DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
			
		r1 = DL.Check_StringAB(decDFEF17, 'DF EF 17 41 42 36 35 31 30 30 30 30 30 30 30 30 30')
		r2 = DL.Check_StringAB(decDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
		r3 = DL.Check_StringAB(decDFEF17, '5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30')
		if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse("DF EF 17 C1 50"):
			DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

	# Tag DFEF18
		r1 = DL.Check_StringAB(maskDFEF18, '36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
		r2 = DL.Check_StringAB(maskDFEF18, '3D 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if r1 == True and r2 == True and DL.Check_RXResponse("DF EF 18 A1 25"):
			DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
			
		r1 = DL.Check_StringAB(decDFEF18, 'DF EF 18 25 36 35 31 30 30 30 30 30 30 30 30 30')
		r2 = DL.Check_StringAB(decDFEF18, '3D 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30')
		if r1 == True and r2 == True and DL.Check_RXResponse("DF EF 18 C1 30"):
			DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
			
	# Tag 56
		r1 = DL.Check_StringAB(mask56, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
		r2 = DL.Check_StringAB(mask56, '5E 43 41 52 44 2F 49 4D 41 47 45')
		r3 = DL.Check_StringAB(mask56, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse("56 A1 41"):
			DL.SetWindowText("blue", "Tag 56_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Mask: FAIL")
			
		r1 = DL.Check_StringAB(dec56, '56 41 42 36 35 31 30 30 30 30 30 30 30 30 30')
		r2 = DL.Check_StringAB(dec56, '5E 43 41 52 44 2F 49 4D 41 47 45')
		r3 = DL.Check_StringAB(dec56, '5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30')
		if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse("56 C1 50"):
			DL.SetWindowText("blue", "Tag 56_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Enc: FAIL")
			
	# Tag 57
		r1 = DL.Check_StringAB(mask57, '65 10 CC CC CC CC')
		r2 = DL.Check_StringAB(mask57, 'D1 71 2C CC CC CC CC CC CC')
		if r1 == True and r2 == True and DL.Check_RXResponse("57 A1 13"):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		r1 = DL.Check_StringAB(dec57, '57 13 65 10 00 00 00 00')
		r2 = DL.Check_StringAB(dec57, 'D1 71 22 01')
		if r1 == True and r2 == True and DL.Check_RXResponse("57 C1 20"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if Tag9F39 == "91": 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if TagDFEE26 == "7300": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")