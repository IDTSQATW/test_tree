#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True
strKey = '0123456789ABCDEFFEDCBA9876543210'

if (Result):
	RetOfStep = DL.SendCommand('DFEE1D-00002A0B30')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('XP6')
	if (RetOfStep):
		DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 0A ?? ?? 54 90 00 05 FF 81 05 82 01 76 50 10 41 6D 65 72 69 63 61 6E 20 45 78 70 72 65 73 73 57 A1 13 BB BB BB BB BB BB BB BD BB BB 70 2B BB BB BB BB BB BB BB 57 C1 20 ** 5A A1 08 BB BB BB BB BB BB BB BF 5A C1 10 ")
		str = DL.Get_RXResponse(1)
		str=str.replace(" ","")
		str1 = str[38:len(str) - 4]
		str9 = DL.GetTLV(str1,"FF8105")
		str2 = DL.GetTLV(str9,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4,'5713374245455400001D141070210100000000000F')
		str5 = DL.GetTLV(str9,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6,'5A08374245455400001F')  

if (Result):
	RetOfStep = DL.SendCommand('Online decline')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 03 03 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00 ")
