#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
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
			if sResult!=None and sResult!="":
				sResult=sResult.replace(" ","")
				CardData=DL.GetTLV(sResult,"DFEE23")
				bresult = False
				if CardData!=None and CardData!='':
					objectMSR = DL.ParseCardData(CardData ,bresult,Key,MacKey)
					EncryptType = DL.Get_EncryptionKeyType_CardData()
					EncryptMode = DL.Get_EncryptionMode_CardData()
					if objectMSR!=None:
						DL.SetWindowText("blue", "KSN:")
						KSN=DL.Get_KSN_CardData()
							
			TagDFEF4C = DL.GetTLV(sResult,"DFEF4C", 0)
			encDFEF4D = DL.GetTLV(sResult,"DFEF4D", 0)
			decDFEF4D = DL.DecryptDLL(0,1, strKey, KSN, encDFEF4D)	

			#1 Tag DFEF4C-4D	
			if i == 1:
				Result = DL.Check_StringAB(TagDFEF4C, '4A 00 00 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 50'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
				
			#2 Tag DFEF4C-4D	
			if i == 2:
				Result = DL.Check_StringAB(TagDFEF4C, '00 24 00 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 28'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#3 Tag DFEF4C-4D	
			if i == 3:
				Result = DL.Check_StringAB(TagDFEF4C, '00 00 66 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 68'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#4 Tag DFEF4C-4D	
			if i == 4:
				Result = DL.Check_StringAB(TagDFEF4C, '4A 24 00 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 70'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")
							
			#5 Tag DFEF4C-4D	
			if i == 5:
				Result = DL.Check_StringAB(TagDFEF4C, '4A 00 66 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 81 B0'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")

			#6 Tag DFEF4C-4D	
			if i == 6:
				Result = DL.Check_StringAB(TagDFEF4C, '00 24 66 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 81 90'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")

			#7 Tag DFEF4C-4D	
			if i == 7:
				Result = DL.Check_StringAB(TagDFEF4C, '4A 24 66 00 00 00')
				if Result == True:
					DL.SetWindowText("blue", "Tag DFEF4C: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4C: FAIL")
							
				Result = DL.Check_StringAB(decDFEF4D, '42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(0), 'DF EF 4D 81 D8'):
					DL.SetWindowText("blue", "Tag DFEF4D: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF4D: FAIL")