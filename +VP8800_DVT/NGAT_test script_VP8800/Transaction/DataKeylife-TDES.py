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
    Result=DL.SendCommand("Encrypt Track Data")
    sResult=DL.Get_RXResponse(0)
    if sResult!=None and sResult!="":
        sResult=sResult.replace(" ","")
        DL.SetWindowText("BLUE", "Encrypted Data: " + sResult[52:132])
        DecryptData = DL.DecryptDLL(0, 1, dek, sResult[32:52], sResult[52:132])
        DL.SetWindowText("BLUE", "Decrypted Data: " + binascii.a2b_hex(DecryptData))
        DL.SetWindowText("BLUE", "KSN: " + sResult[32:52])
        if(DecryptData == '363232353838373331353337323333303D3439313231323030373737303737363038373704040404'):
            DL.SetWindowText("GREEN", "Decrypted Data Matched")
        else:
            DL.SetWindowText("RED", "Decrypted Data Unmatched")
            Result = False
    else:
	    Result=False