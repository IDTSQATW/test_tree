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
		
# Encryption type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")
		
# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

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
			for k in range (1, 3):
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
					RetOfStep = DL.SendCommand('Auto poll')
					if (RetOfStep):
						Result = DL.Check_RXResponse("01 00 00 00")
						time.sleep(1)
						if (Result):
							RetOfStep = DL.SendCommand('Get Transaction Result')
							time.sleep(2)
							if (RetOfStep):
								alldata = DL.Get_RXResponse(1)
								Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 03 23')
								
				KSN = DL.GetTLV(alldata,"DFEE12")				
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				decDFEF4D = DL.DecryptDLL(0,2, strKey, KSN, encDFEF4D)	

				#1 Tag DFEF4C-4D	
				if i == 1:
					Result = DL.Check_StringAB(TagDFEF4C, '43 00 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF4D, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '5E 43 41 52 44 2F 49 4D 41 47 45 20 30 38 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 50'):
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
								
					r1 = DL.Check_StringAB(decDFEF4D, '3B 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '3D 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#3 Tag DFEF4C-4D	
				if i == 3:
					Result = DL.Check_StringAB(TagDFEF4C, '00 00 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '')
					if Result == True and DL.Check_StringAB(alldata, 'DF EF 4D 00'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#4 Tag DFEF4C-4D	
				if i == 4:
					Result = DL.Check_StringAB(TagDFEF4C, '43 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF4D, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '5E 43 41 52 44 2F 49 4D 41 47 45 20 30 38 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F 3B 36 35 31 30 30 30 30 30 30 30 30 30')
					r3 = DL.Check_StringAB(decDFEF4D, '3D 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, 'DF EF 4D 70'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#5 Tag DFEF4C-4D	
				if i == 5:
					Result = DL.Check_StringAB(TagDFEF4C, '43 00 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF4D, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '5E 43 41 52 44 2F 49 4D 41 47 45 20 30 38 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 50'):
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
								
					r1 = DL.Check_StringAB(decDFEF4D, '3B 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '3D 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#7 Tag DFEF4C-4D	
				if i == 7:
					Result = DL.Check_StringAB(TagDFEF4C, '43 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF4D, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
					r2 = DL.Check_StringAB(decDFEF4D, '5E 43 41 52 44 2F 49 4D 41 47 45 20 30 38 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F 3B 36 35 31 30 30 30 30 30 30 30 30 30')
					r3 = DL.Check_StringAB(decDFEF4D, '3D 31 37 31 32 32 30 31 31 30 30 30 30 39 35 30 30 30 30 30 30 3F')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, 'DF EF 4D 70'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
						
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")	