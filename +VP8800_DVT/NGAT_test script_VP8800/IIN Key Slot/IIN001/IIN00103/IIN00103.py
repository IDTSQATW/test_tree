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

# Check data key slot 00
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT KSN (81-0B)_0200')
	if (RetOfStep):
	    if Result == DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 81 0A 00 04 00 01 00 1C 92 15") :
	        DL.SetWindowText("red", "No Data key in slot 00 --> load DEK first.")
	    else:
	          DL.SetWindowText("blue", "DEK in slot 00 is vaild")
		   
		   
# Check data key slot 01
if (Result):
    RetOfStep = DL.SendCommand('Get DUKPT KSN (81-0B)_slot 0101 (PIN key)')
    if (RetOfStep):
	    if Result == DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 81 00 00 0B 01") :
	        DL.SetWindowText("red", "Please erase PIN key.")
	    else:
	          DL.SetWindowText("blue", "PEK slot 00 is empty")

		
# Set IIN (VISA only)
if (Result):
	RetOfStep = DL.SendCommand('Set IIN (VISA only)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("00")

# Get IIN
if (Result):
	RetOfStep = DL.SendCommand('Get IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 83 00 00 07 01 03 47 61 73 01 00 9A DF")


# cmd 02-05, insert card
if (Result):
	RetOfStep = DL.SendCommand('ACT (02-05) - CT only')
	if (RetOfStep):
	    if Result == DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 0A 00 16 70 00 0A 00 04 00 03 DF EE 25 02 10 01 FF EE 01 05 DF EE 30 01 01 ") :
	        DL.SetWindowText("blue", "RX is as expected")
	    else:
	        DL.SetWindowText("red", "Status code is expected to be 0x0A")