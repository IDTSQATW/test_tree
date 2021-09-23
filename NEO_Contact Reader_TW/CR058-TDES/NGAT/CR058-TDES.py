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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")		
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# DFED59 =  00 (Send First Response 0x63)
if (Result):
	RetOfStep = DL.SendCommand('DFED59 =  00 (Send First Response 0x63)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 60-10 w/ DFEF1F: 00 00
if (Result):
	RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 00 00')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
		
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
			# Tag 57
				Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 A1 11'):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 C1 18'):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A A1 08'):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A C1 10'):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07" or Tag9F39 == "05": 
					DL.SetWindowText("Green", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E000": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")

		# cmd 60-11 Contact Authenticate Transaction (DFEF1F: 00 00)			
		if  CTresultcode == "0010":
			Result = True
			RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction (DFEF1F: 00 00)')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(1)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")	
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")	
				
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
	
						# Tags 9F39/ FFEE01/ DFEE26
						if Tag9F39 == "07" or Tag9F39 == "05": 
							DL.SetWindowText("Green", "Tag 9F39: PASS")
						else:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
						if TagFFEE01 != "DFEE300101": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
						if TagDFEE26 != "E000": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 00 00)
		if  CTresultcode == "0004":
			Result = True
			RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 00 00)')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(1)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
				
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
					
						# Tags 9F39/ FFEE01/ DFEE26
						if Tag9F39 == "07" or Tag9F39 == "05": 
							DL.SetWindowText("Green", "Tag 9F39: PASS")
						else:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
						if TagFFEE01 != "DFEE300101": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
						if TagDFEE26 != "E000": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")		

# cmd 60-10 w/ DFEF1F: 01 01 --1
if DL.Get_RXResponse(2) == "YES":
	RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --1')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07" or Tag9F39 == "05": 
					DL.SetWindowText("Green", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E000": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")					

		# cmd 60-11 Contact Authenticate Transaction (DFEF1F: 01 01 --1)		
		if  CTresultcode == "0004":
			Result = True
			RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction (DFEF1F: 01 01 --1)')
			if (RetOfStep):		
				Result = DL.Check_RXResponse("60 0C 00 00")
				if (Result):
					DL.SendCommand('05-01')
					Result = DL.Check_RXResponse("05 00 00 00")
					
# cmd 60-10 w/ DFEF1F: 01 01 --2
if (Result):
	RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --2')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07" or Tag9F39 == "05": 
					DL.SetWindowText("Green", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E000": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
					
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 01 01 --2)
		if  CTresultcode == "0004":
			Result = True
			RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 01 --2)')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(1)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
						
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
						# Tags 9F39/ FFEE01/ DFEE26
						if Tag9F39 == "07" or Tag9F39 == "05": 
							DL.SetWindowText("Green", "Tag 9F39: PASS")
						else:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if TagFFEE01 != "DFEE300101": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if TagDFEE26 != "E000": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
					
# cmd 60-10 w/ DFEF1F: 01 00
if DL.Get_RXResponse(2) == "YES":
	RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 00')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07" or Tag9F39 == "05": 
					DL.SetWindowText("Green", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "E000": 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
					
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 01 00)
		if  CTresultcode == "0004":
			Result = True
			RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 00)')
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(1)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
						
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
						# Tags 9F39/ FFEE01/ DFEE26
						if Tag9F39 == "07" or Tag9F39 == "05": 
							DL.SetWindowText("Green", "Tag 9F39: PASS")
						else:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if TagFFEE01 != "DFEE300101": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if TagDFEE26 != "E000": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")	