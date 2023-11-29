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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")			
		
# cmd 60-10, insert card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')		
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
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
			
			# TagList (default)
				Result = DL.Check_StringAB(alldata, '5F34')
				if (Result):
					Result = DL.Check_StringAB(alldata, '5F20')
				if (Result):
					Result = DL.Check_StringAB(alldata, '5F24')
				if (Result):
					Result = DL.Check_StringAB(alldata, '9F20')
				if (Result):
					Result = DL.Check_StringAB(alldata, '5F25')
				if (Result):
					Result = DL.Check_StringAB(alldata, '5F2D')
				if (Result):
					Result = DL.Check_StringAB(alldata, '50')
				if (Result):
					Result = DL.Check_StringAB(alldata, '84')
				if (Result):
					Result = DL.Check_StringAB(alldata, '4F')
				if (Result):
					Result = DL.Check_StringAB(alldata, 'DFEE23')
				if (Result):
					Result = DL.Check_StringAB(alldata, '9F53')
				if (Result):
					Result = DL.Check_StringAB(alldata, '9F1E')
				if Result == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Default Tags List: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.fails=DL.fails+1
				
				if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_StringAB(TagDFEE26, 'E401') == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")

		# cmd 60-11					
		if  CTresultcode == "0010":
			Result = True
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w LCD')
			if lcdtype == 0:
				RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w/o LCD')
			if (RetOfStep):
				Result = Result and DL.Check_RXResponse("60 63 00 00")
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
						
						# TagList (default)
						Result = DL.Check_StringAB(alldata, '4F')
						if (Result):
							Result = DL.Check_StringAB(alldata, '50')
						if (Result):
							Result = DL.Check_StringAB(alldata, '57')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5A')
						if (Result):
							Result = DL.Check_StringAB(alldata, '82')
						if (Result):
							Result = DL.Check_StringAB(alldata, '84')
						if (Result):
							Result = DL.Check_StringAB(alldata, '8E')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9A')
						if (Result):
							Result = DL.Check_StringAB(alldata, '95')
						if (Result):
							Result = DL.Check_StringAB(alldata, '99')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9B')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9C')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F20')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F24')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F25')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F34')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F28')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F2A')
						if (Result):
							Result = DL.Check_StringAB(alldata, '5F2D')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F02')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F03')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F07')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F08')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F09')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F0D')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F0E')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F0F')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F0B')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F10')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F11')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F12')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F13')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F15')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F16')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F1A')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F1C')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F1E')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F20')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F21')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F24')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F26')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F27')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F33')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F34')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F35')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F36')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F37')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F53')
						if (Result):
							Result = DL.Check_StringAB(alldata, '9F5B')
						if (Result):
							Result = DL.Check_StringAB(alldata, 'DF21')
						if (Result):
							Result = DL.Check_StringAB(alldata, 'DFEE23')
						if (Result):
							Result = DL.Check_StringAB(alldata, 'DFEE51')			
						if Result == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Default Tags List: FAIL")
					
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
							DL.SetWindowText("blue", "Tag 9F39: PASS")
						else:
							DL.fails=DL.fails+1
				
						if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_StringAB(TagDFEE26, 'E401') == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")

						# cmd 60-13
						RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result, for 60-11')
						if (RetOfStep):
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** E4 ** 9F 10 07 06 01 1A 03 90 00 00 9F 26 08 ** 9F 27 01 80 9F 36 02 00 01 9F 37 04 ** 9F 02 06 00 00 00 00 02 00 9F 4D 00 9F 13 00 95 05 ** 9B 02 ** 9F 03 06 00 00 00 00 00 00 9F 34 03 5F 03 02 9F 39 01 05")
							if Result == False:
								DL.fails=DL.fails+1
                        
				# cmd 60-12
				if  CTresultcode == "0004":
					Result = True
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w LCD')
					if lcdtype == 0:
						RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w/o LCD')
					if (RetOfStep):
						Result = Result and DL.Check_RXResponse("60 63 00 00")
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
								
								# TagList (default)
								Result = DL.Check_StringAB(alldata, '9F 10 07 06 01 1A 03 60 00 00')
								if (Result):
									Result = DL.Check_StringAB(alldata, '8A')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F10')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F26')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F27')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F36')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F37')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F02')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F13')
								if (Result):
									Result = DL.Check_StringAB(alldata, '95')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9B')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F03')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F34')
								if (Result):
									Result = DL.Check_StringAB(alldata, 'DFEE51')
								if (Result):
									Result = DL.Check_StringAB(alldata, '99')
								if (Result):
									Result = DL.Check_StringAB(alldata, 'DF21')
								if (Result):
									Result = DL.Check_StringAB(alldata, '9F53')			
								if Result == False:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Default Tags List: FAIL")
									
								# Tags 9F39/ FFEE01/ DFEE26
								if DL.Check_StringAB(Tag9F39, '05') == True or DL.Check_StringAB(Tag9F39, '07') == True: 
									DL.SetWindowText("blue", "Tag 9F39: PASS")
								else:
									DL.fails=DL.fails+1
				
								if DL.Check_StringAB(TagFFEE01, 'DFEE300101') == False:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
								if DL.Check_StringAB(TagDFEE26, 'E401') == False:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag DFEE26: FAIL")
									
								# cmd 60-13
								RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result, for 60-12')
								if (RetOfStep):
									Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** E4 ** 9F 10 07 06 01 1A 03 60 00 00 9F 26 08 ** 9F 27 01 40 9F 36 02 00 01 9F 37 04 ** 9F 02 06 00 00 00 00 02 00 9F 4D 00 9F 13 00 95 05 ** 9B 02 ** 9F 03 06 00 00 00 00 00 00 9F 34 03 5F 03 02 99 00 9F 5B 00 9F 39 01 05")	
									if Result == False:
										DL.fails=DL.fails+1
				else:
					DL.fails=DL.fails+1
		else:
			DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )                                    