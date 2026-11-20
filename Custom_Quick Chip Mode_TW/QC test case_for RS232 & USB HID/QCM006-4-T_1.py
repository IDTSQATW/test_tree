#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result = True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'
KSN='629949012C0004600001'

#Objective: Encryption ON, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

#-----------------------------------------------------------------
# Check output interface
interfacecheck1 = DL.ShowMessageBox("", "Current output interface = USB-HID?", 0)
if interfacecheck1 == 1:
    DL.SetWindowText("Green", "*** output interface = USB-HID, enable MSR Additional Tags ***")
    # Output = USB-HID, enable MSR Additional Tags
    DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 01 00 00 00 00 00", 3000, 1) 
    DL.Check_RXResponse("04 00 00 00")	
else:
    interfacecheck2 = DL.ShowMessageBox("", "Current output interface = RS232?", 0)
    if interfacecheck2 == 1:
        DL.SetWindowText("Green", "*** output interface = RS232, enable MSR Additional Tags ***")
        # Output = RS232, enable MSR Additional Tags
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 01 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	
    else:
        DL.fails=DL.fails+1
        Result = False
    
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
        
# DF7D = 02 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 02 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 02 ", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# DFEF4B = 3F
if (Result):
	DL.SetWindowText("black", "*** DFEF4B = 3F")
	DL.SendIOCommand("IDG", "04 00 DF EF 4B 03 3F 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# enable MSR only
if (Result):
	DL.SetWindowText("black", "*** DFEF37 = 01 = enable MSR only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 01", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Get Data Encryption (C7-37) = encryption ON
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	DL.Check_RXResponse("C7 00 00 01 03")
	time.sleep(0.5)
    
# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
	time.sleep(0.5)

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)
#-----------------------------------------------------------------
def cl_data_analysis(strCardData):
    global strKey
    global KSN
    DFEF4D = ""
    strCardData = strCardData[:41] + " 00" + strCardData[41:]     #add fake attribution to meet NGAT parse rule. (AT mode had no attribution data)

    DFEF4D = DL.GetTLV_Embedded(strCardData,"DFEF4D", 0)
    if KSN and DFEF4D:
        decDFEF4D = DL.DecryptDLL(0,1, strKey, KSN, DFEF4D)	
		    
    return decDFEF4D
#-----------------------------------------------------------------
def msr_data_analysis(strCardData):
	global Key
    global KSN
	Track1_CardData = ""
	Track2_CardData = ""
	Track3_CardData = ""
	TRK1DecryptData = ""
	TRK2DecryptData = ""
	TRK3DecryptData = ""
	strCardData = strCardData[:41] + " 00" + strCardData[41:]     #add fake attribution to meet NGAT parse rule. (AT mode had no attribution data)
    
	if strCardData!=None and strCardData!="":
		strCardData=strCardData.replace(" ","")
		CardData=DL.GetTLV(strCardData,"DFEE23")
		DL.SetWindowText("red", CardData)
		if CardData!=None and CardData!='':
			objectMSR = DL.ParseCardData(CardData, Key)
			EncryptType = DL.Get_EncryptionKeyType_CardData()
			EncryptMode = DL.Get_EncryptionMode_CardData()
			if objectMSR!=None:
				DL.SetWindowText("blue", "Track 1:")
				Track1_CardData = DL.Get_TrackN_CardData(1)
				DL.SetWindowText("blue", "Track 2:")
				Track2_CardData = DL.Get_TrackN_CardData(2)
				DL.SetWindowText("blue", "Track 3:")
				Track3_CardData = DL.Get_TrackN_CardData(3)
				DL.SetWindowText("blue", "Track 1_Enc:")
				TRK1 = DL.Get_EncryptTrackN_CardData(1)
				DL.SetWindowText("blue", "Track 2_Enc:")
				TRK2 = DL.Get_EncryptTrackN_CardData(2)
				DL.SetWindowText("blue", "Track 3_Enc:")
				TRK3 = DL.Get_EncryptTrackN_CardData(3)
				DL.SetWindowText("blue", "KSN:")
				KSN=DL.Get_KSN_CardData()
				if len(TRK1)> 0:
					DL.SetWindowText("blue", "Track 1:")
					TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
				if len(TRK2)> 0:
					DL.SetWindowText("blue", "Track 2:")
					TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
				if len(TRK3) > 0:
					DL.SetWindowText("blue", "Track 3:")
					TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
	return Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
    for i in range (1, 3):
        if i == 1:
            DL.ShowMessageBox("Notice", "Swipe ISO 4909 (3T) card --> Click OK")
        if i == 2:
            DL.ShowMessageBox("Notice", "Insert MSR card 1 time --> Click OK")
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
            DL.ShowMessageBox("Notice", "Insert MSR card 1 time --> Click OK")
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
            DL.ShowMessageBox("Notice", "Insert MSR card 1 time --> Click OK")
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
            DL.ShowMessageBox("Notice", "Swipe ISO 4909 (3T) card --> Click OK")
            
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)

        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02 00',
            'DF EE 25 02 00 11', 
            'DF EE 23',
            '02',
            '80 3F 4D 27 69 87 BF',
            '03',
            'DF EC 11 20',
            'DF EF 4C 06 4C 26 68 00 00 00',
            'DFEF4D',]
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
            
        # call function
        Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData = msr_data_analysis(strCardData)
        
        decDFEF4D = cl_data_analysis(strCardData)
            
        TR1maskdata = "%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
        TR2maskdata = ";4547********0000=1102***************?*"
        TR1plaintextdata = "2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F"
        TR2plaintextdata = "3B343534373537303030313037303030303D313130323130313030303030333036303030303F"
        TR3plaintextdata = "3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F"
        DFEF4Dplaintextdata = "25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F"

        tracks = [
            (TR1maskdata, Track1_CardData, "TR1maskdata"),
            (TR2maskdata, Track2_CardData, "TR2maskdata"),
            (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
            (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
            (TR3plaintextdata, TRK3DecryptData, "TR3plaintextdata"),
            (DFEF4Dplaintextdata, decDFEF4D, "DFEF4Dplaintextdata"),
            ]

        for mask, card, label in tracks:
            if not DL.Check_StringAB(mask, card):
                DL.fails += 1
                DL.SetWindowText("red", label + ": FAIL")

else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Change to default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
    
# Enable 3 interfaces
if (Result):
	DL.SetWindowText("black", "*** Enable All interfaces")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 03", 3000, 1)     #VP6328 only can enable CL +MSR
	time.sleep(0.2)    
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1)     #VP6328 can not accept this cmd 
	time.sleep(0.2) 
    
if interfacecheck1 == 1:
    DL.SetWindowText("Green", "*** output interface = USB-HID, enable MSR Additional Tags ***")
    # Output = USB-HID, disable MSR Additional Tags
    DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
    DL.Check_RXResponse("04 00 00 00")	
    
if interfacecheck2 == 1:
    DL.SetWindowText("Green", "*** output interface = RS232, enable MSR Additional Tags ***")
    # Output = RS232, disable MSR Additional Tags
    DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
    DL.Check_RXResponse("04 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )