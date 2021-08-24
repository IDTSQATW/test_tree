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

Result = DL.ShowMessageBox("Data key check", "The case should erase Data key, does the reader meet the requirement?", 20000)

if Result == 1:
	# Burst mode OFF & Poll on demand		
	if (Result):
		RetOfStep = DL.SendCommand('Burst mode Off')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("04 00 00 00")	
	if (Result):
		RetOfStep = DL.SendCommand('Poll on Demand')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("01 00 00 00")
			
	# # TTQ 20 00 40 00		
	# if (Result):
		# RetOfStep = DL.SendCommand('TTQ 20 00 40 00')
		# if (RetOfStep):
			# Result = Result and DL.Check_RXResponse("04 00 00 00")	

	# AT cmd, tap card
	if (Result):
		for j in range (1, 3):
			if (Result):
				if j == 1:
					RetOfStep = DL.SendCommand('Enable Encryption (02)')
					if (RetOfStep):
						Result = DL.Check_RXResponse("C7 00 00 00")
				if j == 2:
					RetOfStep = DL.SendCommand('Enable Encryption (03)')
					if (RetOfStep):
						Result = DL.Check_RXResponse("C7 00 00 00")			
				for i in range (1, 5):
					if (Result):
						if i == 1:
							RetOfStep = DL.SendCommand('Activate Transaction 02-01')
							if (RetOfStep):
								DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
								alldata = DL.Get_RXResponse(0)
						if i == 2:
							RetOfStep = DL.SendCommand('Activate Transaction 02-40')
							if (RetOfStep):
								DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
								alldata = DL.Get_RXResponse(0)
						if i == 3:
							RetOfStep = DL.SendCommand('Activate Transaction 03-00')
							if (RetOfStep):
								DL.Check_StringAB(DL.Get_RXResponse(1), "56 69 56 4F 74 65 63 68 32 00 03 23")
								alldata = DL.Get_RXResponse(1)		
						if i == 4:
							RetOfStep = DL.SendCommand('Activate Transaction 03-40')
							if (RetOfStep):
								DL.Check_StringAB(DL.Get_RXResponse(1), "56 69 56 4F 74 65 63 68 32 00 03 23")
								alldata = DL.Get_RXResponse(1)						
							
						mask57 = DL.GetTLV(alldata,"57", 0)
						mask5A = DL.GetTLV(alldata,"5A", 0)
							
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
						# Tag 57
						Result = DL.Check_StringAB(mask57, '47 61 73 90 01 01 00 10 D2 01 21 20 00 12 33 99 00 03 1F')
						if Result == True:
							DL.SetWindowText("blue", "Tag 57: PASS")
						else:
							DL.SetWindowText("red", "Tag 57: FAIL")

						# Tag 5A
						Result = DL.Check_StringAB(mask5A, '47 61 73 90 01 01 00 10')
						if Result == True:
							DL.SetWindowText("blue", "Tag 5A: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A: FAIL")
								
						# Tags 9F39/ FFEE01
						if Tag9F39 == "91": 
							DL.SetWindowText("blue", "Tag 9F39: PASS")
						else:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
							
						if (DL.Check_StringAB(TagFFEE01, "DF300100")): 
							DL.SetWindowText("blue", "Tag FFEE01: PASS")
						else:
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
else:
	DL.SetWindowText("Red", "Please erase data key first before running this case")