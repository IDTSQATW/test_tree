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

# Enable encryption (03)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
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
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		alldata = DL.Get_RXResponse(1)
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		if (Result):
			Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):
				Tag57 = DL.GetTLV(alldata,"57", 0)
				Tag5A = DL.GetTLV(alldata,"5A", 0)
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
			# Tag 57
				Result = DL.Check_StringAB(Tag57, '47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 11'):
					DL.SetWindowText("blue", "Tag 57: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 57: FAIL")

			# Tag 5A
				Result = DL.Check_StringAB(Tag5A, '47 61 73 90 01 01 00 10')
				if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A 08'):
					DL.SetWindowText("blue", "Tag 5A: PASS")
				else:
					DL.fails=DL.fails+1
					DL.SetWindowText("red", "Tag 5A: FAIL")
			
			# TagList (default)
				Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F34')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F20')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F24')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F20')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F25')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F2D')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '50')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '84')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '4F')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DFEE23')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F53')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F1E')
				if Result == False:
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Default Tags List: FAIL")
			
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 != "05": 
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
				if TagFFEE01 != "DFEE300101": 
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
				if TagDFEE26 != "6200": 
					DL.fails=DL.fails+1
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			else:
				DL.fails=DL.fails+1

        # cmd 60-11					
        if  CTresultcode == "0010":
            Result = True
            RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction')
            if (RetOfStep):
                Result = Result and DL.Check_RXResponse("60 63 00 00")
                alldata = DL.Get_RXResponse(1)
                CTresultcode = DL.GetTLV(alldata,"DFEE25")	
                if (Result):
                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
                    if (Result):
                        ksn = DL.GetTLV(alldata,"DFEE12")	
                        Tag9F39 = DL.GetTLV(alldata,"9F39")
                        TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
                        TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
                        
                        # TagList (default)
                        Result = DL.Check_StringAB(DL.Get_RXResponse(1), '4F')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '50')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '57')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5A')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '82')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '84')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '8E')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9A')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '95')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '99')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9B')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9C')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F20')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F24')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F25')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F34')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F28')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F2A')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '5F2D')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F02')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F03')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F07')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F08')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F09')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F0D')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F0E')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F0F')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F0B')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F10')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F11')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F12')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F13')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F15')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F16')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F1A')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F1C')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F1E')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F20')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F21')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F24')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F26')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F27')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F33')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F34')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F35')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F36')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F37')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F53')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F5B')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DF21')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DFEE23')
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DFEE51')
                        if Result == False:
                            DL.fails=DL.fails+1
                            DL.SetWindowText("Red", "Default Tags List: FAIL")
                    
                        # Tags 9F39/ FFEE01/ DFEE26
                        if Tag9F39 != "05": 
                            DL.fails=DL.fails+1
                            DL.SetWindowText("Red", "Tag 9F39: FAIL")
                
                        if TagFFEE01 != "DFEE300101": 
                            DL.fails=DL.fails+1
                            DL.SetWindowText("Red", "Tag FFEE01: FAIL")
                
                        if TagDFEE26 != "6200": 
                            DL.fails=DL.fails+1
                            DL.SetWindowText("Red", "Tag DFEE26: FAIL")

                        # cmd 60-13
                        RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result, for 60-11')
                        if (RetOfStep):
                            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** 62 9F 10 07 06 01 1A 03 90 00 00 9F 26 08 ** 9F 27 01 80 9F 36 02 00 01 9F 37 04 ** 9F 02 06 00 00 00 00 02 00 9F 4D 00 9F 13 00 95 05 ** 9B 02 C8 00 9F 03 06 00 00 00 00 00 00 9F 34 03 5F 03 02 9F 39 01 05")
                            if Result == False:
                                DL.fails=DL.fails+1
                    else:
                        DL.fails=DL.fails+1

                # cmd 60-12
                if  CTresultcode == "0004":
                    Result = True
                    RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response')
                    if (RetOfStep):
                        Result = Result and DL.Check_RXResponse("60 63 00 00")
                        alldata = DL.Get_RXResponse(1)
                        CTresultcode = DL.GetTLV(alldata,"DFEE25")
                        if (Result):
                            Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
                            if (Result):
                                ksn = DL.GetTLV(alldata,"DFEE12")
                                Tag9F39 = DL.GetTLV(alldata,"9F39")
                                TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
                                TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
                                
                                # TagList (default)
                                Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F 10 07 06 01 1A 03 60 00 00')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '8A')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F10')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F26')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F27')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F36')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F37')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F02')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F13')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '95')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9B')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F03')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F34')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DFEE51')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '99')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'DF21')
                                if (Result):
                                    Result = DL.Check_StringAB(DL.Get_RXResponse(1), '9F53')
                                if Result == False:
                                    DL.fails=DL.fails+1
                                    DL.SetWindowText("Red", "Default Tags List: FAIL")
                                    
                                # Tags 9F39/ FFEE01/ DFEE26
                                if Tag9F39 != "05": 
                                    DL.fails=DL.fails+1
                                    DL.SetWindowText("Red", "Tag 9F39: FAIL")
                        
                                if TagFFEE01 != "DFEE300101": 
                                    DL.fails=DL.fails+1
                                    DL.SetWindowText("Red", "Tag FFEE01: FAIL")
                        
                                if TagDFEE26 != "6200": 
                                    DL.fails=DL.fails+1
                                    DL.SetWindowText("Red", "Tag DFEE26: FAIL")
                                    
                                # cmd 60-13
                                RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result, for 60-12')
                                if (RetOfStep):
                                    Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** 62 9F 10 07 06 01 1A 03 60 00 00 9F 26 08 ** 9F 27 01 40 9F 36 02 00 01 9F 37 04 ** 9F 02 06 00 00 00 00 02 00 9F 4D 00 9F 13 00 95 05 ** 9B 02 F8 00 9F 03 06 00 00 00 00 00 00 9F 34 03 5F 03 02 99 00 9F 5B 00 9F 39 01 05")				
                                    if Result == False:
                                        DL.fails=DL.fails+1
                            else:
                                DL.fails=DL.fails+1
                                    
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )