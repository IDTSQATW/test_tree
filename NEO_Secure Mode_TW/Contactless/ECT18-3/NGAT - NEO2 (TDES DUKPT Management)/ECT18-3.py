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

# cmd 02-40/ 03-40, tap card
if (Result):
	for i in range(1, 3):
		if i == 1:
			RetOfStep = DL.SendCommand('Poll on Demand')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")
		if i == 2:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Auto Poll w/ LCD')
				rx = 0
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('Auto Poll w/o LCD')
				rx = 1
			if (RetOfStep):
				Result = DL.Check_RXResponse(rx, "01 00 00 00")
		
		if (Result):
			if i == 1:
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('AT Transaction w/ LCD')
					rx = 0
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('AT Transaction w/o LCD')
					rx = 3
			if i == 2:
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('Get Transaction Result w/ LCD')
					rx = 1
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('Get Transaction Result w/o LCD')
					rx = 1
			if (RetOfStep):
				if i == 1:
					DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12')
					if lcdtype == 1:
						alldata = DL.Get_RXResponse(rx)
					if lcdtype == 0:
						alldata = DL.GetTLV(DL.Get_RXResponse(rx),"FF8105")
				if i == 2:
					alldata = DL.Get_RXResponse(rx)	
					DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 03 23 ** E1 ** DF EE 12')
				
				ksn = DL.GetTLV(DL.Get_RXResponse(rx),"DFEE12")	
				
				maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
				encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
				decDFEF18 = DL.DecryptDLL(0,1, strKey, ksn, encDFEF18)	
				
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
				
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)					

			# Tag DFEF18
				if lcdtype == 1:
					Result = DL.Check_StringAB(maskDFEF18, '35 34 31 33 2A 2A 2A 2A 2A 2A 2A 2A 31 35 31 33 3D 30 35 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
					if Result == True and DL.Check_StringAB(alldata, "DF EF 18 A1 22"):
						DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
						
					Result = DL.Check_StringAB(decDFEF18, 'DF EF 18 22 35 34 31 33 33 33 39 30 30 30 30 30 31 35 31 33 3D 30 35 31 32 32 32 30 30 31 32 33 34 35 36 37 38 39')
					if Result == True and DL.Check_StringAB(alldata, "DF EF 18 C1 28"):
						DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
									
			# Tag 57
				Result = DL.Check_StringAB(mask57, '54 13 CC CC CC CC 15 13 D0 51 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(alldata, "57 A1 11"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '57 11 54 13 33 90 00 00 15 13 D0 51 22 20 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(alldata, "57 C1 18"):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
					
			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '54 13 CC CC CC CC 15 13')
				if Result == True and DL.Check_StringAB(alldata, "5A A1 08"):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec5A, '5A 08 54 13 33 90 00 00 15 13')
				if Result == True and DL.Check_StringAB(alldata, "5A C1 10"):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
		
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('03-03 w/ LCD')
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('03-03 w/o LCD')	
				time.sleep(3)