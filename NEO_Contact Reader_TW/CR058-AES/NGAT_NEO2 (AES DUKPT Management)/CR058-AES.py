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

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
        
# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")
		if Result == False:
			DL.SetWindowText("Red", "Please ENABLE data encryption (03)...")

# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
		
# DFED59 =  00 (Send First Response 0x63)
if (Result):
	RetOfStep = DL.SendCommand('DFED59 =  00 (Send First Response 0x63)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("04 00 00 00")	

########################################################################		
### CASE 1		
# 60-10 w/ DFEF1F: 02 02 (error)
if (Result):
	RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 02 02 (error)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 05 00 00")			
else:
	DL.fails=DL.fails+1

### CASE 2	
# cmd 60-10 w/ DFEF1F: 00 00
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 00 00_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 00 00_w/o LCD')		
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(5)	
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
		
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
		
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
			# Tag 57
				Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(alldata, '57 A1 11'):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(alldata, '57 C1 20'):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
				if Result == True and DL.Check_StringAB(alldata, '5A A1 08'):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
				Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
				if Result == True and DL.Check_StringAB(alldata, '5A C1 10'):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
					DL.fails=DL.fails+0
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_StringAB(TagDFEE26, 'E401') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")

		# cmd 60-11 Contact Authenticate Transaction (DFEF1F: 00 00)			
		if  CTresultcode == "0010":
			Result = True
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction (DFEF1F: 00 00)_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction (DFEF1F: 00 00)_w/o LCD')	
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if lcdtype == 1:
					alldata = DL.Get_RXResponse(1)
				if lcdtype == 0:
					alldata = DL.Get_RXResponse(2)	
				CTresultcode = DL.GetTLV(alldata,"DFEE25")	
				if (Result):
					Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")	
				
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
	
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
							DL.fails=DL.fails+0
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_StringAB(TagDFEE26, 'E401') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 00 00)
		if  CTresultcode == "0004":
			Result = True
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 00 00)_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 00 00)_w/o LCD')	
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if lcdtype == 1:
					alldata = DL.Get_RXResponse(1)
				if lcdtype == 0:
					alldata = DL.Get_RXResponse(2)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
				
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
					
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
							DL.fails=DL.fails+0
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_StringAB(TagDFEE26, 'E401') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
else:
	DL.fails=DL.fails+1

### CASE 3							
# cmd 60-10 w/ DFEF1F: 01 01 --1
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --1_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --1_w/o LCD')		
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(6)			
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
					DL.fails=DL.fails+0
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_StringAB(TagDFEE26, 'E401') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")			

		# cmd 60-11 Contact Authenticate Transaction (DFEF1F: 01 01 --1)		
		if  CTresultcode == "0004":
			Result = True
			RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction (DFEF1F: 01 01 --1)')
			if (RetOfStep):		
				Result = DL.Check_RXResponse("60 0C 00 00")
				if (Result):
					if lcdtype == 1:
						DL.SendCommand('05-01_w LCD')
					if lcdtype == 0:
						DL.SendCommand('05-01_w/o LCD')	
					time.sleep(2)	
else:
	DL.fails=DL.fails+1

### CASE 4					
# cmd 60-10 w/ DFEF1F: 01 01 --2
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --2_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 01 --2_w/o LCD')		
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(6)			
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
					DL.fails=DL.fails+0
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
                    
				if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
                    
				if DL.Check_StringAB(TagDFEE26, 'E401') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 01 01 --2)
		if  CTresultcode == "0004":
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 01 --2)_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 01 --2)_w/o LCD')	
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if lcdtype == 1:
					alldata = DL.Get_RXResponse(1)
				if lcdtype == 0:
					alldata = DL.Get_RXResponse(2)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
						
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
							DL.fails=DL.fails+0
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_StringAB(TagDFEE26, 'E401') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
else:
	DL.fails=DL.fails+1

### CASE 5							
# cmd 60-10 w/ DFEF1F: 01 00
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 00_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('60-10 w/ DFEF1F: 01 00_w/o LCD')		
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			alldata = DL.Get_RXResponse(1)
		if lcdtype == 0:
			alldata = DL.Get_RXResponse(6)	
		CTresultcode = DL.GetTLV(alldata,"DFEE25")	
		if (Result):
			Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
			
				# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
					DL.fails=DL.fails+0
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_StringAB(TagDFEE26, 'E401') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					
		# cmd 60-12 Contact Apply Host Response (DFEF1F: 01 00)
		if  CTresultcode == "0004":
			Result = True
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 00)_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response (DFEF1F: 01 00)_w/o LCD')	
			if (RetOfStep):
				Result = DL.Check_RXResponse("60 63 00 00")
				if lcdtype == 1:
					alldata = DL.Get_RXResponse(1)
				if lcdtype == 0:
					alldata = DL.Get_RXResponse(2)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")
						
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
							DL.fails=DL.fails+0
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
						if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_StringAB(TagDFEE26, 'E401') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
else:
	DL.fails=DL.fails+1
                            
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )