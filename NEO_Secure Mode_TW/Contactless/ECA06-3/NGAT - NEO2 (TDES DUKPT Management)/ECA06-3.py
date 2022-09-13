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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")		
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, tap card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
		rx = 0
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction w/o LCD')	
		rx = 4
	if (RetOfStep):
		if lcdtype == 1:
			DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** F1 ** DF EE 12")
		if lcdtype == 0:
			DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")	
		alldata = DL.Get_RXResponse(rx)		
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

		if lcdtype == 1:		
		# Tag DFEF17
			r1 = DL.Check_StringAB(maskDFEF17, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
			r2 = DL.Check_StringAB(maskDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
			r3 = DL.Check_StringAB(maskDFEF17, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
			if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "DF EF 17 A1 41"):
				DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
				
			r1 = DL.Check_StringAB(decDFEF17, 'DF EF 17 41 42 36 35 31 30 30 30 30 30 30 30 30 30')
			r2 = DL.Check_StringAB(decDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
			r3 = DL.Check_StringAB(decDFEF17, '5E 31 37 31 32 32 30 31')
			if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "DF EF 17 C1 50"):
				DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

		# Tag DFEF18
			r1 = DL.Check_StringAB(maskDFEF18, '36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
			r2 = DL.Check_StringAB(maskDFEF18, '3D 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
			if r1 == True and r2 == True and DL.Check_RXResponse(rx, "DF EF 18 A1 25"):
				DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
				
			r1 = DL.Check_StringAB(decDFEF18, 'DF EF 18 25 36 35 31 30 30 30 30 30 30 30 30 30')
			r2 = DL.Check_StringAB(decDFEF18, '3D 31 37 31 32 32 30 31')
			if r1 == True and r2 == True and DL.Check_RXResponse(rx, "DF EF 18 C1 30"):
				DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
				
		# Tag 56
			r1 = DL.Check_StringAB(mask56, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
			r2 = DL.Check_StringAB(mask56, '5E 43 41 52 44 2F 49 4D 41 47 45')
			r3 = DL.Check_StringAB(mask56, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
			if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "56 A1 41"):
				DL.SetWindowText("blue", "Tag 56_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 56_Mask: FAIL")
				
			r1 = DL.Check_StringAB(dec56, '56 41 42 36 35 31 30 30 30 30 30 30 30 30 30')
			r2 = DL.Check_StringAB(dec56, '5E 43 41 52 44 2F 49 4D 41 47 45')
			r3 = DL.Check_StringAB(dec56, '5E 31 37 31 32 32 30 31')
			if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "56 C1 50"):
				DL.SetWindowText("blue", "Tag 56_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 56_Enc: FAIL")
				
		# Tag 57
			r1 = DL.Check_StringAB(mask57, '65 10 CC CC CC CC')
			r2 = DL.Check_StringAB(mask57, 'D1 71 2C CC CC CC CC CC CC')
			if r1 == True and r2 == True and DL.Check_RXResponse(rx, "57 A1 13"):
				DL.SetWindowText("blue", "Tag 57_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				
			r1 = DL.Check_StringAB(dec57, '57 13 65 10 00 00 00 00')
			r2 = DL.Check_StringAB(dec57, 'D1 71 22 01')
			if r1 == True and r2 == True and DL.Check_RXResponse(rx, "57 C1 20"):
				DL.SetWindowText("blue", "Tag 57_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Enc: FAIL")
			
		# Tags 9F39/ FFEE01/ DFEE26
			if DL.Check_RXResponse(rx, "9F39 01 91") == False: 
				DL.SetWindowText("Red", "Tag 9F39: FAIL")
					
			if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
				DL.SetWindowText("Red", "Tag FFEE01: FAIL")
					
			if DL.Check_RXResponse(rx, "DFEE26 02 F100") == False: 
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
				
		if lcdtype == 0:					
		# Tag 57
			r1 = DL.Check_StringAB(mask57, '36 07 CC CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC')
			if r1 == True and DL.Check_RXResponse(rx, "57 A1 12"):
				DL.SetWindowText("blue", "Tag 57_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				
			r1 = DL.Check_StringAB(dec57, '57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01 00 00 00 00 00 00 00 00 00 00 00 00')
			if r1 == True and DL.Check_RXResponse(rx, "57 C1 20"):
				DL.SetWindowText("blue", "Tag 57_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Enc: FAIL")
				
		# Tags 9F39/ FFEE01/ DFEE26	
			if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
				DL.SetWindowText("Red", "Tag 9F39: FAIL")
					
			if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
				DL.SetWindowText("Red", "Tag FFEE01: FAIL")
					
			if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")				
			
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")	