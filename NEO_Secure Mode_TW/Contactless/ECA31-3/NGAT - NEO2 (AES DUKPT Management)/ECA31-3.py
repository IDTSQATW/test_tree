#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check reader is VP3350 or not
readertype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")	
	DL.SetWindowText("black", "*** 0105 do not use LCD")
	DL.SendIOCommand("IDG", "01 05 11 05", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")		
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	

# Poll On Demand/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Poll On Demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# Check data encryption TYPE is AES
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")	
	
# cmd 02-40
if (Result):
	DL.SetWindowText("black", "*** cmd 02-40")
	DL.SetWindowText("red", "[Please tap CUP QUICS test card]")
	DL.SendIOCommand("IDG", "02 40 1E 9A 03 07 11 21 9F 21 03 10 15 20 9C 01 00 9F 02 06 00 00 00 00 15 00 DF EF 37 01 02", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
	if (Result):
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")

		Tag84 = DL.GetTLV_Embedded(alldata,"84")
		mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
		enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
		dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
		mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
		enc5A = DL.GetTLV_Embedded(alldata,"5A", 1)
		dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
		
		# Tag 84
		if DL.Check_RXResponse("84 ** A000000333010101"): 
			DL.SetWindowText("blue", "Tag 84: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("Red", "Tag 84: FAIL")
		
		# Tag 57
		if DL.Check_RXResponse('57 A1 13 62 28 CC CC CC CC 11 17 D2 01 2C CC CC CC CC CC CC CC CC'):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '57 13 62 28 00 01 00 00 11 17 D2 01 21 20 00 12 33 99 00 03 1F')
		if Result == True and DL.Check_RXResponse("57 C1"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
			
		# Tag 5A
		if DL.Check_RXResponse('5A A1 08 62 28 CC CC CC CC 11 17'):
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec5A, '5A 08 62 28 00 01 00 00 11 17')
		if Result == True and DL.Check_RXResponse("5A C1"):
			DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")			
	else:
		DL.fails=DL.fails+1
		DL.SetWindowText("Red", "RX data is incorrect.")
        
# cmd 03-03
if (Result):
	DL.SetWindowText("black", "*** cmd 03-03, Approve")
	DL.SendIOCommand("IDG", "03 03 00 E3 00 06 31 32 33 34 35 36 9A 03 15 07 30 9F 21 03 10 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("03 00 00 00")	
else:
	DL.SendIOCommand("IDG", "05 01", 3000, 1)
	time.sleep(2)
	
if readertype == 1:
	DL.SetWindowText("black", "*** 0105 default (VP3350)")
	DL.SendIOCommand("IDG", "01 05 19 05", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")		
    
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )