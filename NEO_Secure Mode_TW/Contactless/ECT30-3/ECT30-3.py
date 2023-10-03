#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

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
    
# Check data encryption TYPE is TDES	
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")

# Set Configuration
if (Result):
	DL.SetWindowText("black", "*** Set Configuration")
	DL.SendIOCommand("IDG", "04 00 DF EE 44 02 FF FF DF EE 37 01 03 DF EE 0C 01 09 DF ED 66 04 F9 C0 00 09 5F 2A 02 03 92", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# Set Configurable Group
if (Result):
	DL.SetWindowText("black", "*** Set Configurable Group")
	DL.SendIOCommand("IDG", "04 03 DF EE 2D 01 D0 DF EF 44 02 7F 00 DF 81 23 06 00 00 00 00 45 00 DF EE 34 06 00 00 00 02 00 00 DF 81 26 06 00 00 00 01 00 00 DF EE 2B 01 00 DF EF 45 02 10 00 DF EE 2C 01 00 DF 81 20 05 90 40 00 80 00 DF 81 21 05 04 10 00 00 00 DF 81 22 05 90 60 00 90 00 9F 53 03 70 00 00 DF EE 2A 06 00 00 00 00 20 00 9F 01 06 00 00 00 00 00 10 9F 15 02 70 32 9F 4E 17 58 58 20 4D 45 52 43 48 41 4E 54 20 59 59 20 4C 4F 43 41 54 49 4F 4E 9F 1A 02 03 92 9F 35 01 22 5F 2A 02 03 92 5F 36 01 02 9F 40 05 F0 00 F0 30 01 DF EF 19 04 00 00 00 3C", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")

# Delete Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Delete Configurable AID")
	DL.SendIOCommand("IDG", "04 04 9F 06 06 A0 00 00 00 25 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")

if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 04 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 04 30 60", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 20 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 30 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 65 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 03 24 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 02 77 10 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 01 52 30 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 00 03 80 10", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 07 A0 00 00 03 33 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 08 A0 00 00 03 33 01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 08 A0 00 00 03 33 01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
if (Result):
	DL.SendIOCommand("IDG", "04 04 9F 06 09 A0 00 00 04 76 D0 00 01 11", 3000, 1) 
	Result = DL.Check_RXResponse("04 ** 00 00")
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 D0 9F 06 07 A0 00 00 00 65 20 20 DF EE 53 01 02 DF EE 4B 01 01 DF EE 2E 01 10 DF EE 54 0C 05 00 D0 05 01 D0 05 09 D0 05 20 D0 DF EE 59 01 05 DF EE 4D 01 54 DF EE 4C 01 0E", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")
	
# Set Configurable AID
if (Result):
	DL.SetWindowText("black", "*** Set Configurable AID")
	DL.SendIOCommand("IDG", "04 02 DF EE 2D 01 D0 9F 06 07 A0 00 00 00 65 10 10 DF EE 53 01 02 DF EE 4B 01 01 DF EE 2E 01 10 DF EE 54 06 05 00 D0 05 01 D0 DF EE 59 01 05 DF EE 4D 01 54 DF EF 2C 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# cmd 02-40
if (Result):
	DL.SetWindowText("black", "*** cmd 02-40, Please tap Card 58#-JCB_MagStripe card..........")
	DL.SendIOCommand("IDG", "02 40 1E 9C 01 00 9F 02 06 00 00 00 00 15 00", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
	if (Result):
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")
		Tag50 = DL.GetTLV_Embedded(alldata,"50")
		mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
		enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
		dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)
		
		# Tag 50
		if DL.Check_RXResponse("50 ** 4A434220437265646974"): 
			DL.SetWindowText("blue", "Tag 50: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("Red", "Tag 50: FAIL")
		
		# Tag 57
		if DL.Check_RXResponse('57 A1 13 35 40 CC CC CC CC 10 12 D4 91 2C CC CC CC CC CC CC CC CC '):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '57 13 35 40 82 99 99 42 10 12 D4 91 22 01 55 55 55 55 55 55 1F ')
		if Result == True and DL.Check_RXResponse("57 C1"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.fails=DL.fails+1
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
	
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