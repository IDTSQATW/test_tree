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

		
# Set IIN
if (Result):
	RetOfStep = DL.SendCommand('Set IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("00")

# Get IIN
if (Result):
	RetOfStep = DL.SendCommand('Get IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("37 09 03 47 61 73 01 00 03 44 62 72 01 01 03 54 13 33 01 03 03 54 57 21 01 04 03 67 99 99 01 05 03 35 40 82 01 06 03 36 07 05 01 07 03 37 42 45 01 08 03 65 10 00 01 09")


		
# Delete IIN (With DEK/PEK slot 00)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 00)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")
			

				
# Delete IIN (With DEK/PEK slot 01)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 01)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		
		
				
# Delete IIN (With DEK/PEK slot 03)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 03)')
	if (RetOfStep):	
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

				
# Delete IIN (With DEK/PEK slot 04)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 04)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

		
# Delete IIN (With DEK/PEK slot 05)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 05)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

		
# Delete IIN (With DEK/PEK slot)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 06)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

		
# Delete IIN (With DEK/PEK slot)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 07)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

				
# Delete IIN (With DEK/PEK slot)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 08)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		

		
# Delete IIN (With DEK/PEK slot)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 09)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")		


		
# Delete 2 IIN (With DEK/PEK slot 05/06)

	RetOfStep = DL.SendCommand('Delete IIN (With DEK/PEK slot 09)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is to be 0x07")	

# Delete 3 IIN (With DEK/PEK slot 05/06/07)

	RetOfStep = DL.SendCommand('Delete 3 IIN (With DEK/PEK slot 05/06/07)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")	
			
			
# Delete 3 IIN (With DEK/PEK slot 05/06/07)

	RetOfStep = DL.SendCommand('Delete 3 IIN (With DEK/PEK slot 05/06/07)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 47 07 00 00 9D B9")
		if Result == True:
			DL.SetWindowText("blue", "PASS")
		else:
			DL.SetWindowText("red", "FAIL, Status code is expected to be 0x07")	
			   

# Get IIN
if (Result):
	RetOfStep = DL.SendCommand('Get IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("37 08 03 44 62 72 01 01 03 54 13 33 01 03 03 54 57 21 01 04 03 67 99 99 01 05 03 35 40 82 01 06 03 36 07 05 01 07 03 37 42 45 01 08 03 65 10 00 01 09")