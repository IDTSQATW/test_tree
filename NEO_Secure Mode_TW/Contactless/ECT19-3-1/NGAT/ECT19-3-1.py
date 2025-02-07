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
            Result = DL.Check_RXResponse("01 00 00 00")

    # cmd 02-40, tap card
    if (Result):
        RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
        if (RetOfStep):
            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E5 ** DF EE 12")
            
            str123 = DL.Get_RXResponse(0).replace(" ","")
            str456 = DL.Get_RXResponse(1).replace(" ","")
            if(str456!=""):str1 = str123[30:-4]+str456[28:-4]
            else:str1 = str123[30:-4]
            
            if (Result):
                alldata = DL.Get_RXResponse(0)
                ksn = DL.GetTLV(alldata,"DFEE12")	
                
                mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
                str57 = DL.GetTLV_Embedded(str1, "57",1)
                strD57 = DL.DecryptTransAmorData(str57)
                    
                mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
                str5A = DL.GetTLV_Embedded(str1, "5A",1)
                strD5A = DL.DecryptTransAmorData(str5A)
                
                # Tag 57
                Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC')
                if Result == False:
                    Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC CC CC')
                if Result == True and DL.Check_RXResponse("57 A1 13"):
                    DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                    
                if (strD57 == '876543214761739001010010=30121200012339900031' or strD57 == '876543214761739001010010=20121200012339900031') and DL.Check_RXResponse("57 C2 01 58"):
                    DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Enc: FAIL")

                # Tag 5A
                Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
                if Result == True and DL.Check_RXResponse("5A A1 08"):
                    DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                    
                if (strD5A == '876543214761739001010010') and DL.Check_RXResponse("5A C2 01 58"):
                    DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                    
                # Tags 9F39/ FFEE01/ DFEE26
                if DL.Check_RXResponse("9F39 01 07") == False: 
                    DL.fails=DL.fails+1
                    DL.SetWindowText("Red", "Tag 9F39: FAIL")
                
                if DL.Check_RXResponse("FFEE01 ** DFEE300100") == False: 
                    DL.fails=DL.fails+1
                    DL.SetWindowText("Red", "Tag FFEE01: FAIL")
                
                if DL.Check_RXResponse("DFEE26 02 E502") == False: 
                    DL.fails=DL.fails+1
                    DL.SetWindowText("Red", "Tag DFEE26: FAIL")
            else:
                DL.fails=DL.fails+1
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