#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
readertype = 0

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check if reader support auto poll mode or not
pollmodetype = DL.ShowMessageBox("", "Does the reader support auto poll mode?", 0)
if pollmodetype == 1:
	DL.SetWindowText("Green", "*** The reader support auto poll mode ***")
	pollmode = 3
else:
	DL.SetWindowText("Green", "*** The reader did NOT support auto poll mode ***")
	pollmode = 2

# Check reader is VP3350 or not
readermodel = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readermodel == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	
	
# Poll on Demand
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")	
	
# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Please load AES key first.....")
	
# Set group 80 -- DF 81 1B = 40
if (Result):
	RetOfStep = DL.SendCommand('Set group 80 -- DF 81 1B = 40')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			

# cmd 02-40, tap MChip card
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
								alldata=DL.Get_RXResponse(0)
								Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")	
								
				if k == 2:
					RetOfStep = DL.SendCommand('Auto poll')
					if (RetOfStep):
						Result = DL.Check_RXResponse("01 00 00 00")
						time.sleep(1)
						if (Result):
							RetOfStep = DL.SendCommand('Get Transaction Result')
							time.sleep(3)	
							if (RetOfStep):
								alldata = DL.Get_RXResponse(1)
								Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 03 23')
								
				ksn = DL.GetTLV(alldata,"DFEE12")				
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				DL.SetWindowText("blue", "Tag DFEF4D Decryption data:")
				decDFEF4D = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDFEF4D)	

				#1 Tag DFEF4C-4D	
				if i == 1:
					Result = DL.Check_StringAB(TagDFEF4C, '2B 00 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '25 42 35 31 32 38 35 37 30 31 30 30 30 33 ')
					R2 = DL.Check_StringAB(decDFEF4D, '5E 20 2F 5E 31 38 30 33 36 32 32 30 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
					
				#2 Tag DFEF4C-4D	
				if i == 2:
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '3B 35 31 32 38 35 37 30 31 30 30 30 33 ')
					R2 = DL.Check_StringAB(decDFEF4D, '3D 31 38 30 33 36 32 32 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#3 Tag DFEF4C-4D	
				if i == 3:
					if TagDFEF4C == "" or TagDFEF4C == "000000000000":
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
					if encDFEF4D == "":
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#4 Tag DFEF4C-4D	
				if i == 4:
					Result = DL.Check_StringAB(TagDFEF4C, '2B 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '25 42 35 31 32 38 35 37 30 31 30 30 30 33')
					R2 = DL.Check_StringAB(decDFEF4D, '5E 20 2F 5E 31 38 30 33 36 32 32 30 30')
					if R1 == True and R2 == True:
						R1 = DL.Check_StringAB(decDFEF4D, '3F 3B 35 31 32 38 35 37 30 31 30 30 30 33')
						R2 = DL.Check_StringAB(decDFEF4D, '3D 31 38 30 33 36 32 32 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 60'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#5 Tag DFEF4C-4D	
				if i == 5:
					Result = DL.Check_StringAB(TagDFEF4C, '2B 00 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '25 42 35 31 32 38 35 37 30 31 30 30 30 33')
					R2 = DL.Check_StringAB(decDFEF4D, '5E 20 2F 5E 31 38 30 33 36 32 32 30 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#6 Tag DFEF4C-4D	
				if i == 6:
					Result = DL.Check_StringAB(TagDFEF4C, '00 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '3B 35 31 32 38 35 37 30 31 30 30 30 33')
					R2 = DL.Check_StringAB(decDFEF4D, '3D 31 38 30 33 36 32 32 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 30'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#7 Tag DFEF4C-4D	
				if i == 7:
					Result = DL.Check_StringAB(TagDFEF4C, '2B 27 00 00 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					R1 = DL.Check_StringAB(decDFEF4D, '25 42 35 31 32 38 35 37 30 31 30 30 30 33 ')
					R2 = DL.Check_StringAB(decDFEF4D, '5E 20 2F 5E 31 38 30 33 36 32 32 30 30')
					if R1 == True and R2 == True:
						R1 = DL.Check_StringAB(decDFEF4D, '3F 3B 35 31 32 38 35 37 30 31 30 30 30 33 ')
						R2 = DL.Check_StringAB(decDFEF4D, '3D 31 38 30 33 36 32 32 30')
					if R1 == True and R2 == True and DL.Check_StringAB(alldata, 'DF EF 4D 60'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
else:
	DL.fails=DL.fails+1
						
if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")						
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )