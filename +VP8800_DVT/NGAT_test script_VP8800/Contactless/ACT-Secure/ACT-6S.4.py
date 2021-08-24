#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True


if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '0123456789ABCDEFFEDCBA9876543210' 
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot1')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot1')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C1 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 18 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '11111111111111111111111111111111' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot2')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot2')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C1 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 18 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '22222222222222222222222222222222' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')	

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot3')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot3')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '33333333333333333333333333333333' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot4')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot4')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C1 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 18 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '44444444444444444444444444444444' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot5')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot5')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '55555555555555555555555555555555' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT slot6')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot6')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '66666666666666666666666666666666' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT slot7')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot7')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C1 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 18 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '77777777777777777777777777777777' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,1, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,1, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT slot8')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot8')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '88888888888888888888888888888888' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT slot9')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('ACT 02-05 slot9')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? C3 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 57 A1 13 47 61 CC CC CC CC 00 10 D2 01 21 20 CC CC CC CC CC CC CC 57 C1 20 ** 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10")
		strKey = '99999999999999999999999999999999' 
		str1 = DL.Get_RXResponse(0)
		str2 = DL.GetTLV(str1,"57", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, '57134761739001010010D20121200012339900031F')
		str5 = DL.GetTLV(str1,"5A",1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, '5A084761739001010010')