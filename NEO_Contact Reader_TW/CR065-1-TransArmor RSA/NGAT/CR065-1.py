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

# Objective: Decrypted data for transarmorRSA should contain TID and tag data with the value from card.
		
# Check TransAmor RSA test cert
certcheck = DL.ShowMessageBox("", "Does the reader had TransAmor RSA test cert? (If NO, pls load it from NGAT toolbar -- RSA-TransAmor, and then restart test)", 0)
if certcheck == 1:
    Result= True
else:
    Result= False
        
########################### Start test ###########################
if (Result):
    # Check reader is VP3350 or not
    readertype = DL.ShowMessageBox("", "Is this VP3350?", 0)
    if readertype == 1:
        DL.SetWindowText("Green", "*** This is VP3350 ***")
        RetOfStep = DL.SendCommand('0105 do not use LCD')
        if (RetOfStep):
            Result = DL.Check_RXResponse("01 00 00 00")
    else:
        DL.SetWindowText("Green", "*** non-VP3350 reader ***")
            
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
        RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("60 63 00 00")
            alldata = DL.Get_RXResponse(1)
            
            str123 = DL.Get_RXResponse(1).replace(" ","")
            str456 = DL.Get_RXResponse(2).replace(" ","")
            if(str456!=""):str1 = str123[30:-4]+str456[28:-4]
            else:str1 = str123[30:-4]
            
            CTresultcode = DL.GetTLV(alldata,"DFEE25")
            if (Result):
                Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
                if (Result):
                    ksn = DL.GetTLV(alldata,"DFEE12")	
            
                    mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
                    str57 = DL.GetTLV_Embedded(str1, "57",1)
                    strD57 = DL.DecryptTransAmorData(str57)
                    
                    mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
                    str5A = DL.GetTLV_Embedded(str1, "5A",1)
                    strD5A = DL.DecryptTransAmorData(str5A)
            
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
                
                    DL.SetWindowText("blue", strD57)
                    Result = DL.Check_StringAB(strD57, '876543214761739001010010=20122010123456789')
                    if Result == True and DL.Check_StringAB(alldata, '57 C2 01 58'):
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
                
                    DL.SetWindowText("blue", strD5A)
                    Result = DL.Check_StringAB(strD5A, '876543214761739001010010')
                    if Result == True and DL.Check_StringAB(alldata, '5A C2 01 58'):
                        DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                    else:
                        DL.fails=DL.fails+1
                        DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                        
                # Tags 9F39/ FFEE01/ DFEE26
                    if Tag9F39 != "05": 
                        DL.fails=DL.fails+1
                        DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
                    if TagFFEE01 != "DFEE300101": 
                        DL.fails=DL.fails+1
                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
                    if TagDFEE26 != "E402": 
                        DL.fails=DL.fails+1
                        DL.SetWindowText("Red", "Tag DFEE26: FAIL")
                else:
                    DL.fails=DL.fails+1
    else:
        DL.fails=DL.fails+1

    # cmd 60-11					
    if  CTresultcode == "0010":
        Result = True
        RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction_w LCD')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("60 63 00 00")
            alldata = DL.Get_RXResponse(1)
            CTresultcode = DL.GetTLV(alldata,"DFEE25")	
            if (Result):
                Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
                if (Result):
                    ksn = DL.GetTLV(alldata,"DFEE12")	
                    
                    Tag9F39 = DL.GetTLV(alldata,"9F39")
                    TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
                    TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
                
                    # Tags 9F39/ FFEE01/ DFEE26
                    if Tag9F39 != "05": 
                        DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
                    if TagFFEE01 != "DFEE300101": 
                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
                    if TagDFEE26 != "E402": 
                        DL.SetWindowText("Red", "Tag DFEE26: FAIL")
    else:
        DL.fails=DL.fails+1
                    
    # cmd 60-12
    if  CTresultcode == "0004":
        Result = True
        RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response_w LCD')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("60 63 00 00")
            alldata = DL.Get_RXResponse(1)
            CTresultcode = DL.GetTLV(alldata,"DFEE25")
            if (Result):
                Result = DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 60 00')
                if (Result):
                    ksn = DL.GetTLV(alldata,"DFEE12")
                    
                    Tag9F39 = DL.GetTLV(alldata,"9F39")
                    TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
                    TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
                        
                    # Tags 9F39/ FFEE01/ DFEE26
                    if Tag9F39 != "05": 
                        DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
                    if TagFFEE01 != "DFEE300101": 
                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
                    if TagDFEE26 != "E402": 
                        DL.SetWindowText("Red", "Tag DFEE26: FAIL")
    else:
        DL.fails=DL.fails+1

    if readertype == 1:
        RetOfStep = DL.SendCommand('0105 default (VP3350)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("01 00 00 00")						
else:
    DL.fails=DL.fails+1

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )