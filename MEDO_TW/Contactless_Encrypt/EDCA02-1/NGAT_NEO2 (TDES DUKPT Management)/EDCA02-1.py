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

# Check if reader support auto poll mode or not
pollmodetype = DL.ShowMessageBox("", "Does the reader support auto poll mode?", 0)
if pollmodetype == 1:
	DL.SetWindowText("Green", "*** The reader support auto poll mode ***")
    pollmode = 3
else:
	DL.SetWindowText("Green", "*** The reader did NOT support auto poll mode ***")
    pollmode = 2
	
# Check reader is VP3350 or not
modeltype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if modeltype == 1:
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
		Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap Discover card
if (Result):
	for i in range (1, 8):
		if i == 1:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 1')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")		
                time.sleep(1)				
		if i == 2:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 2')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
				time.sleep(1)
		if i == 3:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 3')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
				time.sleep(1)
		if i == 4:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 4')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")		
				time.sleep(1)
		if i == 5:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 5')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
				time.sleep(1)
		if i == 6:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 6')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
				time.sleep(1)
		if i == 7:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 7')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")
                time.sleep(1)				
		
		if (Result):
			for k in range (1, pollmode):
				if k == 1:
					RetOfStep = DL.SendCommand('Poll on Demand')
					if (RetOfStep):
						Result = DL.Check_RXResponse("01 00 00 00")
						time.sleep(1)
						if (Result):
							RetOfStep = DL.SendCommand('Activate Transaction')	
							if (RetOfStep):
								Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 **")	
								alldata=DL.Get_RXResponse(0)
				if k == 2:
					time.sleep(1)
					RetOfStep = DL.SendCommand('Auto poll')
					if (RetOfStep):
						Result = DL.Check_RXResponse("01 00 00 00")
						time.sleep(1)
						if (Result):
							RetOfStep = DL.SendCommand('Get Transaction Result')	
							if (RetOfStep):
								alldata = DL.Get_RXResponse(1)
								Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 03 23')
								
				KSN = DL.GetTLV(alldata,"DFEE12")				
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				decDFEF4D = DL.DecryptDLL(0,2, strKey, KSN, encDFEF4D)	

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
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
					if Result == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
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
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
					if Result == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
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
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
					if Result == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#7 Tag DFEF4C-4D	
				if i == 7:
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
					if Result == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
						
if modeltype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")