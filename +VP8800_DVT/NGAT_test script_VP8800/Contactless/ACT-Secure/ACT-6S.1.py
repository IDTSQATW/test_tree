﻿#!/usr/bin/env python
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
	RetOfStep = DL.SendCommand('Master NO3 card')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 DF EF 18 A1 25 35 34 31 33 31 32 2A 2A 2A 2A 2A 2A 34 38 30 38 3D 30 39 30 36 31 30 31 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 30 ** 9F 6B A1 13 54 13 12 CC CC CC CC CC CC CC CC CC CC CC CC CC C3 21 0F 9F 6B C1 20")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"DFEF18", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, 'DFEF1825353431333132333435363738343830383D3039303631303139303030393930303033323130')
		str5 = DL.GetTLV(str1,"FFEE04")
		str6 = DL.GetTLV(str5,"FFEE05",1)
		str7 = DL.GetTLV(str6,"FF8105")
		str8 = DL.GetTLV(str7,"9F6B",1)
		str9 = DL.DecryptDLL(0,2, strKey, str3, str8)
		Result = DL.Check_StringAB(str9, '9F6B135413123456784808D09061019000990003210F')

if (Result):
	RetOfStep = DL.SendCommand('qVSDC')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 73 CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 201  ** 5A A1 08 47 61 73 CC CC CC 00 10 5A C1 10")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')
	
if (Result):
	RetOfStep = DL.SendCommand('XP6')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 0A ?? ?? 54 90 00 05 FF 81 05 82 01 76 50 10 41 6D 65 72 69 63 61 6E 20 45 78 70 72 65 73 73 57 A1 13 37 42 45 CC CC C0 00 1D 14 10 70 2C CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 37 42 45 CC CC C0 00 1F 5A C1 10")
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
	RetOfStep = DL.SendCommand('MCHIP')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 DF EF 18 A1 24 35 34 31 33 33 33 2A 2A 2A 2A 2A 2A 31 35 31 33 3D 31 32 30 37 32 30 31 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 ** 5A A1 08 54 13 33 CC CC CC 15 13 5A C1 10 ** 57 A1 12 54 13 33 CC CC CC 15 13 D1 20 72 01 CC CC CC CC CC CC 57 C1 20")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"DFEF18", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, 'DFEF1824353431333333393030303030313531333D31323037323031303030303030303030303030')
		str5 = DL.GetTLV(str1,"FF8105")
		str6 = DL.GetTLV(str5,"5A")
		str7 = DL.DecryptDLL(0,2, strKey, str3, str6)
		Result = DL.Check_StringAB(str7, '5A085413339000001513') 
		str8 = DL.GetTLV(str5,"57")
		str9 = DL.DecryptDLL(0,2, strKey, str3, str8)
		Result = DL.Check_StringAB(str9,'57125413339000001513D1207201000000000000')

if (Result):
	RetOfStep = DL.SendCommand('qVSDC typeB')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 73 CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 73 CC CC CC 00 10 5A C1 10")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')
	
if (Result):
	RetOfStep = DL.SendCommand('Interac')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 0A ?? ?? 42 90 00 0A ** 57 A1 11 54 13 33 CC CC CC 15 13 D1 51 22 20 CC CC CC CC CC 57 C1 20 ** 5A A1 08 54 13 33 CC CC CC 15 13 5A C1 10")
		str = DL.Get_RXResponse(1)
		str=str.replace(" ","")
		str1 = str[38:len(str) - 4]
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57115413339000001513D15122200123456789')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A085413339000001513')

if (Result):
	RetOfStep = DL.SendCommand('Discover')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 DF EF 17 A1 41 2A 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 5E 44 49 53 43 4F 56 45 52 2F 4E 45 54 57 4F 52 4B 20 20 20 20 20 20 20 20 20 20 5E 31 31 31 32 31 30 31 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 17 C1 50 ** DF EF 18 A1 25 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 3D 31 31 31 32 31 30 31 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 30 ** 56 A1 41 2A 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 5E 44 49 53 43 4F 56 45 52 2F 4E 45 54 57 4F 52 4B 20 20 20 20 20 20 20 20 20 20 5E 31 31 31 32 31 30 31 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 56 C1 50 ** 57 A1 13 60 11 00 CC CC CC 42 71 D1 11 21 01 CC CC CC CC CC CC CC 57 C1 20")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"DFEF17", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, 'DFEF174142363031313030303939313930343237315E444953434F5645522F4E4554574F524B202020202020202020205E3131313231303131303030313635353935353031')
		str5 = DL.GetTLV(str1,"DFEF18", 1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, 'DFEF1825363031313030303939313930343237313D3131313231303131303030313635353935353031')
		str7 = DL.GetTLV(str1,"FFEE04")
		str8 = DL.GetTLV(str7,"FFEE05")
		str9 = DL.GetTLV(str8,"FF8105")
		str10 = DL.GetTLV(str9,"56", 1)
		str11 = DL.DecryptDLL(0,2, strKey, str3, str10)
		Result = DL.Check_StringAB(str11, '564142363031313030303939313930343237315E444953434F5645522F4E4554574F524B202020202020202020205E3131313231303131303030313635353935353031')
		str12 = DL.GetTLV(str9,"57", 1)
		str13 = DL.DecryptDLL(0,2, strKey, str3, str12)
		Result = DL.Check_StringAB(str13, '57136011000991904271D11121011000165595501F')
		

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00")
