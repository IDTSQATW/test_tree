#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN='1234567812345678'
strKey =''
rx = 0

#Objective: to verify cmd 62-01, decrypt PIN code.

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")

# 62-01 PLEASE ENTER PIN
if (Result):
    RetOfStep = DL.SendCommand('62-01 PLEASE ENTER PIN')
    if (RetOfStep):
        Result = DL.Check_RXResponse(0, "62 00 00 00")
        if (Result):
            PINdata = str(DL.Get_RXResponse(1))
            PINdata = PINdata.replace(" ","")
            PINdata = PINdata.decode("hex")
            ksn = PINdata[15:35]	
            PINblock = PINdata[35:51]
            decryptPIN = DL.FormatX_PIN_Block_Decipher(1, 1, ksn, Key, PAN, PINblock)
            if decryptPIN != "168168168":
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "PIN <> 168168168: FAIL")

if(0 < (DL.fails + DL.warnings)):
    DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
    DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )