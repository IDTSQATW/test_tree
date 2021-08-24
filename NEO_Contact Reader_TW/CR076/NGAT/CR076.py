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

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")	

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
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

# 04-00 set date = 20200105
if (Result):
	RetOfStep = DL.SendCommand('04-00 set date = 20200105')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")
		
# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (03)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data -- 3C')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A 19')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
		
# cmd 60-10, insert card
if (Result):
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')

		# cmd 60-11					
		if  CTresultcode == "0010":
			RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if (Result):
					lcdcheck = DL.ShowMessageBox('Notice','Does LCD display msg "ENTER PIN"?', 0)
					if lcdcheck != 1:
						DL.SetWindowText("red", "LCD msg: FAIL")
					else:
						RetOfStep = DL.SendCommand('61-02 PIN = 1234')
						if (RetOfStep):
							alldata = DL.Get_RXResponse(1)
							CTresultcode = DL.GetTLV(alldata,"DFEE25")
							Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
							if (Result):
								Result = DL.Check_StringAB(CTresultcode, '00 00')
								if Result != True:
									DL.SetWindowText("red", "cmd 60-11, tag DFEE25 value: FAIL")
								lcdcheck = DL.ShowMessageBox('Notice','Does LCD display msg "APPROVED"?', 0)
								if lcdcheck != 1:
									DL.SetWindowText("red", "LCD msg: FAIL")