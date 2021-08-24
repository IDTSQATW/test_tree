#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

if (Result):
	RetOfStep = DL.SendCommand('02-05(Transaction Currency Exponent 5F36), 02, UI Check, ICC')
	if (RetOfStep):
		Result = DL.Check_RXResponse("NULL") and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse("YES") and Result
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result

if (Result):
	RetOfStep = DL.SendCommand('02-05(Transaction Currency Exponent 5F36), 01, UI Check, ICC')
	if (RetOfStep):
		Result = DL.Check_RXResponse("NULL") and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse("YES") and Result
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result

if (Result):
	RetOfStep = DL.SendCommand('02-05(Transaction Currency Exponent 5F36), 02, Transaction Check, ICC')
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result
		Result = DL.Check_RXData("5F 36 01 02") and Result
		Result = DL.Check_RXResponse("NULL") and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse("Yes") and Result
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result

if (Result):
	RetOfStep = DL.SendCommand('02-05(Transaction Currency Exponent 5F36), 01, Transaction Check, ICC')
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result
		Result = DL.Check_RXData("5F 36 01 01") and Result
		Result = DL.Check_RXResponse("NULL") and Result
	if (RetOfStep):
		Result = DL.Check_RXResponse("Yes") and Result
	if (RetOfStep):
		Result = DL.Check_RXErrorCode("00") and Result
