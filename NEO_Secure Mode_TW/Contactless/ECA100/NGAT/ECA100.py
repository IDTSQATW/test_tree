#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'
rx = 0

#Objective: to verify AES DUKPT Management, AES-128 Working Key encryption/ decryption function

# CL test
if (Result):
	RetOfStep = DL.SendCommand('02-40 (enable CL only)')
	rx = 5 # for VP3350
	if (RetOfStep):
		alldata = DL.Get_RXResponse(rx)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		TagFF8105 = DL.GetTLV(alldata,"FF8105")
		# 57
		DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
		mask57 = DL.GetTLV(TagFF8105,"57", 0)
		enc57 = DL.GetTLV(TagFF8105,"57", 1)
		DL.SetWindowText("blue", "Tag 57 Decryption data:")
		dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)	
		if DL.Check_RXResponse(rx, '57A113 47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC') == False:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
		if DL.Check_StringAB(dec57, '57134761739001010010D30121200012339900031F0000000000000000000000') == False:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		# 5A
		DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
		mask5A = DL.GetTLV(TagFF8105,"5A", 0)
		enc5A = DL.GetTLV(TagFF8105,"5A", 1)
		DL.SetWindowText("blue", "Tag 5A Decryption data:")
		dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)	
		if DL.Check_RXResponse(rx, '5AA108 47 61 CC CC CC CC 00 10') == False:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
		if DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10') == False:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
            
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )