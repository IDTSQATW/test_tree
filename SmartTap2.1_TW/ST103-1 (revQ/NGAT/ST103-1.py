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

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# C7-65 set private key	
if (Result):
	RetOfStep = DL.SendCommand('C7-65 set private key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		
# 04-00 w/ tag DFED3F = 01 (VAS data encryption ON)
if (Result):
	RetOfStep = DL.SendCommand('04-00 w/ tag DFED3F = 01 (VAS data encryption ON)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")

# cmd 02-40, tap card
if (Result):
	for i in range(1, 5):
		if i == 1:
			RetOfStep = DL.SendCommand('case 1.1')
		if i == 2:
			RetOfStep = DL.SendCommand('case 3.1')	
		if i == 3:
			RetOfStep = DL.SendCommand('case 5.1')	
		if i == 4:
			RetOfStep = DL.SendCommand('case 0.6')				
			
		if (RetOfStep):
			if i == 1:
				RetOfStep = DL.SendCommand('02-40 case 1.1')
			if i == 2:
				time.sleep(1)
				RetOfStep = DL.SendCommand('02-40 case 3.1')	
			if i == 3:
				time.sleep(1)
				RetOfStep = DL.SendCommand('02-40 case 5.1')	
			if i == 4:
				time.sleep(1)
				RetOfStep = DL.SendCommand('02-40 case 0.6')		
			
			if (RetOfStep):		
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
				FFEE08 = DL.GetTLV(alldata,"FFEE08", 0)
				if i != 3:
					encDFEF76 = DL.GetTLV(FFEE08,"DFEF76", 0)
					decDFEF76 = DL.DecryptDLL(0,1, strKey, ksn, encDFEF76)	
				
				if i <= 2:
					DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 57 ** E1 ** DFEE12 0A ** FF EE 08")
				if i == 3:
					DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 57 ** E1 ** FF EE 08")
				if i == 4:
					DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** F1 ** DFEE12 0A **")	
					TagFF8105 = DL.GetTLV(alldata,"FF8105", 0)
					mask56 = DL.GetTLV(TagFF8105,"56", 0)
					enc56 = DL.GetTLV(TagFF8105,"56", 1)
					dec56 = DL.DecryptDLL(0,1, strKey, ksn, enc56)		
					mask9F6B = DL.GetTLV(TagFF8105,"9F6B", 0)
					enc9F6B = DL.GetTLV(TagFF8105,"9F6B", 1)
					dec9F6B = DL.DecryptDLL(0,1, strKey, ksn, enc9F6B)	
					
				# Tag FFEE08	
				if i != 3:
					Result = DL.Check_StringAB(decDFEF76, '94 03 2F 61 73 76 94 01 06 69 04 02 71 79 79 71 54 03 1F 63 75 73 94 03 06 63 69 64 04 12 34 56 78 90 19 01 03 03 54 63 70 6C 00')
					if (Result):
						Result = DL.Check_StringAB(decDFEF76, '54 03 02 63 75 74 04 7B 54 03 27 61 73 76 94 01 05 69 05 01 F7 97 98 54 02 19 6C 79 94 03 09 6F 69 64 04')
						if (Result):
							Result = DL.Check_StringAB(decDFEF76, '54 01 06 6E 05 F3 24 23 42 34')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF76_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF76_Enc: FAIL")	

				if i == 3:			
					Result = DL.Check_StringAB(FFEE08, 'FF EE 08 04 DF EF 76 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag FFEE08: PASS")
					else:
						DL.SetWindowText("red", "Tag FFEE08: FAIL")						
						
				if i == 4:
					# Tag 56
					Result = DL.Check_StringAB(mask56, '2A 35 34 31 33 2A 2A 2A 2A 2A 2A 2A 2A 34 38 30 30 5E 53 55 50 50 4C 49 45 44 2F 4E 4F 54 5E 31 39 30 36 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
					if Result == True and DL.Check_RXResponse("56 A1 3E"):
						DL.SetWindowText("blue", "Tag 56_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag 56_Mask: FAIL")						
					Result = DL.Check_StringAB(dec56, '56 3E 42 35 34 31 33 31 32 33 34 35 36 37 38 34 38 30 30 5E 53 55 50 50 4C 49 45 44 2F 4E 4F 54 5E 31 39 30 36 31 30 31')
					if Result == True and DL.Check_RXResponse("56 C1"):
						DL.SetWindowText("blue", "Tag 56_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag 56_Enc: FAIL")	
					# Tag 9F6B
					Result = DL.Check_StringAB(mask9F6B, '54 13 CC CC CC CC 48 00 D1 90 6C CC CC CC CC CC CC CC CC')
					if Result == True and DL.Check_RXResponse("9F 6B A1 13"):
						DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")						
					Result = DL.Check_StringAB(dec9F6B, '9F 6B 13 54 13 12 34 56 78 48 00 D1 90 61 01')
					if Result == True and DL.Check_RXResponse("9F 6B C1"):
						DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
						
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")								