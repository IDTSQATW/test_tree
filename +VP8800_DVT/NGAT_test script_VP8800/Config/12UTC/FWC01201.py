#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

if (Result):
	RetOfStep = DL.SendCommand('Get Firmware Version')
	if (RetOfStep):

if (Result):
	RetOfStep = DL.SendCommand('Invalid Year(0A)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 05", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Month(13)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Month(00)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Day(32)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Day(00)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Date(18-02-29)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Invalid Date(18-04-31)')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 0A", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Set Date 18-01-01')
	if (RetOfStep):
		Result = DL.Check_RXResponse(0,"25 05 00", True) and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse(1,"25 06 00 00 06 18 01 01", True) and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse(2,"9A 03 18 01 01", True) and Result

if (Result):
	RetOfStep = DL.SendCommand('Set Current Date and Time(YYMMDD HHMMSS)')

if (Result):
	RetOfStep = DL.SendCommand('Get UTC Date and Time')
