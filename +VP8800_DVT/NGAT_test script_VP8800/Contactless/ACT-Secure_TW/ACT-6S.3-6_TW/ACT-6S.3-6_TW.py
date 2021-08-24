#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True
strKey = '11111111111111111111111111111111'

if (Result):
	RetOfStep = DL.SendCommand('DFEE1D-06042A0C30')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 00 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot1')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('Interac')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 0A 01 93 42 90 00 0A ** 57 A1 11 54 13 33 CC CC CC 15 13 DC CC C2 20 CC CC CC CC CC 57 C1 18 ** 5A A1 08 54 13 33 CC CC CC 15 13 5A C1 10")
		str = DL.Get_RXResponse(1)
		str=str.replace(" ","")
		str1 = str[38:len(str) - 4]
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57115413339000001513D30122200123456789')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A085413339000001513')

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00")
