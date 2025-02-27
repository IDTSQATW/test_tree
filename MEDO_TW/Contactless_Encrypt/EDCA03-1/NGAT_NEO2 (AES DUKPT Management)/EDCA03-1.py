#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Please load AES key first.....")	
		
# cmd 02-40, tap VISA qVSDC card
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
			for k in range (1, 2):
				if k == 1:
					RetOfStep = DL.SendCommand('Poll on Demand')
					if (RetOfStep):
						Result = DL.Check_RXResponse("01 00 00 00")
						if (Result):
							RetOfStep = DL.SendCommand('Activate Transaction')	
							if (RetOfStep):
								alldata=DL.Get_RXResponse(0)
								Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")	
								
				ksn = DL.GetTLV(alldata,"DFEE12", 0)				
				TagDFEF4C = DL.GetTLV(alldata,"DFEF4C", 0)
				encDFEF4D = DL.GetTLV(alldata,"DFEF4D", 0)
				DL.SetWindowText("blue", "Tag DFEF4D Decryption data:")
				decDFEF4D = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDFEF4D)

				#1 Tag DFEF4C-4D	
				if i == 1:
					Result = DL.Check_RXResponse('DFEF4C 06 00 00 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 10'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
					
				#2 Tag DFEF4C-4D	
				if i == 2:
					Result = DL.Check_RXResponse('DFEF4C 06 00 25 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == False:
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 40'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#3 Tag DFEF4C-4D	
				if i == 3:
					Result = DL.Check_RXResponse('DFEF4C 06 00 00 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 10'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#4 Tag DFEF4C-4D	
				if i == 4:
					Result = DL.Check_RXResponse('DFEF4C 06 00 25 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == False:
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 40'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
								
				#5 Tag DFEF4C-4D	
				if i == 5:
					Result = DL.Check_RXResponse('DFEF4C 06 00 00 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 10'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#6 Tag DFEF4C-4D	
				if i == 6:
					Result = DL.Check_RXResponse('DFEF4C 06 00 25 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == False:
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 40'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")

				#7 Tag DFEF4C-4D	
				if i == 7:
					Result = DL.Check_RXResponse('DFEF4C 06 00 25 00 10 00 00')
					if Result == True:
						DL.SetWindowText("blue", "Tag DFEF4C: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4C: FAIL")
								
					Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == False:
						Result = DL.Check_StringAB(decDFEF4D, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
					if Result == True and DL.Check_RXResponse('DF EF 4D 40'):
						DL.SetWindowText("blue", "Tag DFEF4D: PASS")
					else:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag DFEF4D: FAIL")
else:
	DL.fails=DL.fails+1
                        
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")							
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )