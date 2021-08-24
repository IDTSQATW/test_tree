#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import binascii
Result = True
i=0

dek='0123456789abcdeffedcba9876543210'
pek='0123456789abcdeffedcba9876543210'
hmac='0123456789abcdeffedcba9876543210'

while(Result):
    if (i%10==0):
        DL.ClearWindowText()
    i=i+1
    DL.SetWindowText("Green", str(i))
    Result=DL.SendCommand("Encrypt PIN")
    sResult=DL.Get_RXResponse(0)
    if sResult!=None and sResult!="":
        sResult=sResult.replace(" ","")
        DL.SetWindowText("BLUE", "Encrypted Data: " + sResult[52:68])
        DecryptData = DL.DecryptDLL(1, 1, pek, sResult[32:52], sResult[52:68])
        DL.SetWindowText("BLUE", "Decrypted Data: " + binascii.a2b_hex(DecryptData))
        DL.SetWindowText("BLUE", "KSN: " + sResult[32:52])
        if(DecryptData == '3132333435360202'):
            DL.SetWindowText("GREEN", "Decrypted PIN Matched")
        else:
            DL.SetWindowText("RED", "Decrypted PIN Unmatched")
            Result = False
    else:
	    Result=False