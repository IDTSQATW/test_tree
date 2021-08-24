#!/usr/bin/env python
import sys
import time
RetOfStep = True
Result=True
strKey = '0123456789ABCDEFFEDCBA9876543210'

if (Result):
	RetOfStep = DL.SendCommand('DFEE1D-06042A0C31')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 00 00 00 00")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('qVSDC typeB')
	if (RetOfStep):
		DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 73 CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 73 CC CC CC 00 10 5A C1 10")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00")
