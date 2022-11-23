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
	rx = 4 # for VP3350
	if (RetOfStep):
		DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 ** DF EE 12")
		alldata = DL.Get_RXResponse(rx)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		TagFF8105 = DL.GetTLV(alldata,"FF8105")
		# 57
		DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
		mask57 = DL.GetTLV(TagFF8105,"57", 0)
		enc57 = DL.GetTLV(TagFF8105,"57", 1)
		DL.SetWindowText("blue", "Tag 57 Decryption data:")
		dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)	
		if DL.Check_RXResponse(rx, '57A111 5413CCCCCCCC0010D1412CCCCCCCCCCCCC') == False:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
		if DL.Check_StringAB(dec57, '57115413330089600010D1412201012340917200000000000000000000000000') == False:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		# 5A
		DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
		mask5A = DL.GetTLV(TagFF8105,"5A", 0)
		enc5A = DL.GetTLV(TagFF8105,"5A", 1)
		DL.SetWindowText("blue", "Tag 5A Decryption data:")
		dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)	
		if DL.Check_RXResponse(rx, '5AA108 5413CCCCCCCC0010') == False:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
		if DL.Check_StringAB(dec5A, '5A085413330089600010000000000000') == False:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")

		# Tags 9F39/ DFEE26
		if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		if DL.Check_RXResponse(rx, "DFEE26 02 E301") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")