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

# Check reader is VP3350 or not
readermodel = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readermodel == 1:
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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")

# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
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

# cmd 02-40, tap card
if (Result):
    for i in range(1, 3):
        if readermodel == 1: #VP3350
            if i == 1:
                RetOfStep = DL.SendCommand('DFEE1D--02 02 21 0A 30 (NEO3)')
                if (RetOfStep):
                    Result = Result and DL.Check_RXResponse("C7 00 00 00")	
            if i == 2:
                RetOfStep = DL.SendCommand('DFEE1D--06 04 7E 0F 31 (NEO3)')
                if (RetOfStep):
                    Result = Result and DL.Check_RXResponse("C7 00 00 00")	
        if readermodel == 0: #non-VP3350
            if i == 1:
                RetOfStep = DL.SendCommand('DFEE1D--02 02 21 0A 30')
                if (RetOfStep):
                    Result = Result and DL.Check_RXResponse("04 00 00 00")	
            if i == 2:
                RetOfStep = DL.SendCommand('DFEE1D--06 04 7E 0F 31')
                if (RetOfStep):
                    Result = Result and DL.Check_RXResponse("04 00 00 00")	
				
        if (Result):	
            time.sleep(1)
            RetOfStep = DL.SendCommand('Activate Transaction')
            if (RetOfStep):
                Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
                if (Result):
                    alldata = DL.Get_RXResponse(0)
                    ksn = DL.GetTLV(alldata,"DFEE12")	
                    
                    maskDFEF17 = DL.GetTLV(alldata,"DFEF17", 0)
                    encDFEF17 = DL.GetTLV(alldata,"DFEF17", 1)
                    decDFEF17 = DL.DecryptDLL(0,1, strKey, ksn, encDFEF17)	
            
                    maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
                    encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
                    decDFEF18 = DL.DecryptDLL(0,1, strKey, ksn, encDFEF18)	
            
                    tagFF8105 = DL.GetTLV(alldata,"FF8105", 0)
                    mask56 = DL.GetTLV(tagFF8105,"56", 0)
                    enc56 = DL.GetTLV(tagFF8105,"56", 1)
                    dec56 = DL.DecryptDLL(0,1, strKey, ksn, enc56)	
            
                    mask57 = DL.GetTLV(tagFF8105,"57", 0)
                    enc57 = DL.GetTLV(tagFF8105,"57", 1)
                    dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
                
                    # Tag 57
                    if i == 1:
                        Result = DL.Check_RXResponse('36 AA AA AA AA AA A0 1D AA AA AA AA AA AA AA AA AA AA')
                    if i == 2:
                        Result = DL.Check_RXResponse('36 07 0F FF FF F0 00 1D 49 12 FF FF FF FF FF FF FF FF')
                        
                    if Result == True and DL.Check_RXResponse("57 A1 12"):
                        DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                    else:
                        DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            
                    r1 = DL.Check_StringAB(dec57, '57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01 00 00 00 00 00 00 00 00 00 00 00 00')
                    if r1 == True and DL.Check_RXResponse("57 C1 18"):
                        DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                    else:
                        DL.SetWindowText("red", "Tag 57_Enc: FAIL")		
                else:
                    DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1

# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")							
						
if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")								
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )