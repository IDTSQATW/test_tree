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
	RetOfStep = DL.SendCommand('MCHIP')
	if (RetOfStep):
		DL.Check_RXResponse(0, "56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 DF EF 18 A1 24 35 34 31 33 33 33 2A 2A 2A 2A 2A 2A 31 35 31 33 3D 31 32 30 37 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 ** 5A A1 08 54 13 33 CC CC CC 15 13 5A C1 10 ** 57 A1 12 54 13 33 CC CC CC 15 13 D1 20 72 01 CC CC CC CC CC CC 57 C1 20")
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"DFEF18", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, 'DFEF1824353431333333393030303030313531333D31323037323031')
		str5 = DL.GetTLV_Embedded(str1,"FF8105",0, True)
		str6 = DL.GetTLV(str5,"5A", 1)
		str7 = DL.DecryptDLL(0,2, strKey, str3, str6)
		Result = DL.Check_StringAB(str7, '5A085413339000001513') 
		str8 = DL.GetTLV(str5,"57", 1)
		str9 = DL.DecryptDLL(0,2, strKey, str3, str8)
		Result = DL.Check_StringAB(str9,'57125413339000001513D1207201')

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00")
