#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True
Free1Bef=""
Used1Bef=""
Free1Aft=""
Free1Aft=""

if (Result):
	RetOfStep = DL.SendCommand('Get Free Space(1)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 23 00 00 0E ?? ?? ?? ?? ?? ?? ?? ?? 00 ?? ?? ?? ?? ??")
    str = DL.Get_RXResponse(0)
    str = str.replace(" ","")
    Free1 = str[30:46]
    Used1 = str[49:59]
    	
if (Result):
	RetOfStep = DL.SendCommand('Transfer img1.bmp(7654 bytes, 8192 bytes on disk)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")

if (Result):
	RetOfStep = DL.SendCommand('Get Free Space(2)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 23 00 00 0E ?? ?? ?? ?? ?? ?? ?? ?? 00 ?? ?? ?? ?? ??")

if (Result):
	RetOfStep = DL.SendCommand('Delete img1.bmp')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 1F 00 00 00 E8 D1")