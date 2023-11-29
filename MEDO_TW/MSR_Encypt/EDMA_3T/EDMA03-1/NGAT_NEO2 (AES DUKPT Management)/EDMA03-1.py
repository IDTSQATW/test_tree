#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check reader is VP3350 or not
readertype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, swipe card
if (Result):
	for i in range (1, 8):
		if i == 1:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 1')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")			
		if i == 2:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 2')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
		if i == 3:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 3')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
		if i == 4:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 4')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")			
		if i == 5:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 5')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
		if i == 6:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 6')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
		if i == 7:
			RetOfStep = DL.SendCommand('04-00-----DFEF4B 7')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")	
				
		RetOfStep = DL.SendCommand('Activate Transaction')
		if (RetOfStep):
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 **")		
			sResult=DL.Get_RXResponse(0)
			if Result == True:
				CardData=DL.GetTLV(sResult,"DFEE23",0)
				if CardData!=None and CardData!='':
					objectMSR = DL.ParseCardData(CardData,Key)
					KSN=DL.Get_KSN_CardData()
							
			TagDFEF4C = DL.GetTLV(sResult,"DFEF4C", 0)
			encDFEF4D = DL.GetTLV(sResult,"DFEF4D", 0)
			decDFEF4D = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, encDFEF4D)

			#1 Tag DFEF4C-4D	
			if i == 1:
				Result = DL.Check_RXResponse('DFEF4C 06 4A 00 00 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 60'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
				
			#2 Tag DFEF4C-4D	
			if i == 2:
				Result = DL.Check_RXResponse('DFEF4C 06 00 24 00 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 40'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#3 Tag DFEF4C-4D	
			if i == 3:
				Result = DL.Check_RXResponse('DFEF4C 06 00 00 66 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 81 80'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#4 Tag DFEF4C-4D	
			if i == 4:
				Result = DL.Check_RXResponse('DFEF4C 06 4A 24 00 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 81 80'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#5 Tag DFEF4C-4D	
			if i == 5:
				Result = DL.Check_RXResponse('DFEF4C 06 4A 00 66 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 81 C0'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")

			#6 Tag DFEF4C-4D	
			if i == 6:
				Result = DL.Check_RXResponse('DFEF4C 06 00 24 66 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 81 A0'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")

			#7 Tag DFEF4C-4D	
			if i == 7:
				Result = DL.Check_RXResponse('DFEF4C 06 4A 24 66 10 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 00 00 00 00 00 00 00 00 00 00 00 00')
				if Result == True and DL.Check_RXResponse('DF EF 4D 81 F0'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
else:
	DL.fails=DL.fails+1
					
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")						
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )