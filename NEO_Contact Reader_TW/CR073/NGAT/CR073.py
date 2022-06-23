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

# Objective: to verify case SDK: V2CA0010100av4.1d_1 & check 'Force Online'

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

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")			
		
# cmd 60-10, insert card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')	
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(9)	
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')

		# cmd 60-11					
		if  CTresultcode == "0010":
			Result = True
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if lcdtype == 1:
					alldata = DL.Get_RXResponse(1)
				if lcdtype == 0:
					alldata = DL.Get_RXResponse(4)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")	
				if (Result):
					DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
				
				# cmd 60-12
				if  CTresultcode == "0004":
					Result = True
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w LCD')
					if lcdtype == 0:
						RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')
					if (RetOfStep):
						Result = DL.Check_RXResponse("60 63 00 00")
						if lcdtype == 1:
							alldata = DL.Get_RXResponse(1)
						if lcdtype == 0:
							alldata = DL.Get_RXResponse(2)
						CTresultcode = DL.GetTLV(alldata,"DFEE25")
						if (Result):
							Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
							if (Result):
								Result = DL.Check_StringAB(CTresultcode, '00 02')
								if Result != True:
									DL.SetWindowText("red", "cmd 60-12, tag DFEE25 value: FAIL")