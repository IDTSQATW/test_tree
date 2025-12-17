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

# Objective: to verify TransArmor TDES

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")
    
# Check platform
pf = DL.ShowMessageBox("", "Is the project platform NEOI(GR)?", 0)
if pf == 1:
	DL.SetWindowText("Green", "*** The project platform is NEOI(GR) ***")
else:
	DL.SetWindowText("Green", "*** The project platform is not NEOI(GR) ***")
    
if pf != 1:
    # Encryption Type -- TransArmor TDES
    if (Result):
        RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
        time.sleep(1)

    # Check data encryption TYPE is TDES: TransArmor TDES	
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")
            if Result == False:
                DL.SetWindowText("red", "Please change TDES DUKPT Output Mode as TransArmor TDES first...")
else:
    # 2-use TransArmor TDES to encrypt (C7-32)
    if (Result):
        RetOfStep = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
        time.sleep(1)

    # Encryption Type -- TransArmor TDES	
    if (Result):
        RetOfStep = DL.SendCommand('Encryption Type -- TransArmor TDES')
        if (RetOfStep):
            Result = DL.Check_RXResponse("C7 00 00 01 02")
            if Result == False:
                DL.SetWindowText("red", "Please change TDES DUKPT Output Mode as TransArmor TDES first...")

# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap card
if (Result):
    if lcdtype == 1:
        RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
        rx = 0
    if lcdtype == 0:
        if pf != 1: #non-NEOI/GR
            RetOfStep = DL.SendCommand('Activate Transaction w/o LCD')	
            rx = 5
        if pf == 1: #NEOI/GR
            RetOfStep = DL.SendCommand('Activate Transaction (NEOI/ GR)')	
            rx = 0
    if (RetOfStep):
        if pf != 1: #non-NEOI/GR
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E5 ** DF EE 12")
        if pf == 1: #NEOI/GR
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** F5 ** FF EE 12")
        if (Result):
            alldata = DL.Get_RXResponse(rx)
            if pf != 1: #non-NEOI/GR
                ksn = DL.GetTLV(alldata,"DFEE12")	
            if pf == 1: #NEOI/GR
                ksn = DL.GetTLV(alldata,"FFEE12")	
            
            if DL.GetTLV(alldata,"57", 0) == "":
                alldata = DL.GetTLV(alldata,"FF8105", 0)
            mask57 = DL.GetTLV(alldata,"57", 0)	
            enc57 = DL.GetTLV(alldata,"57", 1)
            dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
            
            if DL.GetTLV(alldata,"5A", 0) == "":
                alldata = DL.GetTLV(alldata,"FF8105", 0)
            mask5A = DL.GetTLV(alldata,"5A", 0)	
            enc5A = DL.GetTLV(alldata,"5A", 1)
            dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
            
            # Tag 57
            Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC')
            if Result == False:
                Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC CC CC')
            if Result == True and DL.Check_RXResponse(rx, "57 A1 13"):
                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                
            Result = DL.Check_StringAB(dec57, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
            if Result == False:
                Result = DL.Check_StringAB(dec57, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
            if Result == True and DL.Check_RXResponse(rx, "57 C1 28"):
                DL.SetWindowText("blue", "Tag 57_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Enc: FAIL")

            # Tag 5A
            Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
            if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                
            Result = DL.Check_StringAB(dec5A, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
            if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
                DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                
            # Tags 9F39/ FFEE01/ DFEE26
            if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
            if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
            if DL.Check_RXResponse(rx, "DFEE26 02 E506") == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DFEE26: FAIL")
        else:
            DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
            
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )