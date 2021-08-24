#!/usr/bin/env python
import sys
import time
RetOfStep = True
Result=True
strKey = '0123456789ABCDEFFEDCBA9876543210'


if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('CT ACT (02-05)')
	if (RetOfStep):
		DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 30 ?? ?? C0")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"5A", 1)
		str3 = DL.GetTLV(str1,"DFEE12")		
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)		
		Result = DL.Check_StringAB(str4, '5A084761739001010010')
		str5 = DL.GetTLV(str1,"57")
		str9 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str9, '57114761739001010010D20122010123456789')

if (Result):
	RetOfStep = DL.SendCommand('Approve (02-06)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 06 00")
