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

#Objective: Encryption OFF, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

#-----------------------------------------------------------------
# # Check output interface
# interfacecheck1 = DL.ShowMessageBox("", "Current output interface = USB-HID?", 0)
# if interfacecheck1 == 1:
    # DL.SetWindowText("Green", "*** output interface = USB-HID ***")
    # # Output = USB-HID, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
    # DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
    # DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
    # DL.Check_RXResponse("04 00 00 00")	
# else:
    # interfacecheck2 = DL.ShowMessageBox("", "Current output interface = RS232?", 0)
    # if interfacecheck2 == 1:
        # DL.SetWindowText("Green", "*** output interface = RS232 ***")
        # # Output = RS232, Data Case Sensitivity = Default (Original from Card, upper/lower mixed)
        # DL.SetWindowText("black", "*** Data Case Sensitivity = Default (Original from Card, upper/lower mixed)")
        # DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
        # DL.Check_RXResponse("04 00 00 00")	
    # else:
        # DL.fails=DL.fails+1
        # Result = False
    
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
    
# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
	time.sleep(0.5)
#-----------------------------------------------------------------
def msr_data_analysis(strCardData):
	global Key
        
	Track1_CardData = ""
	Track2_CardData = ""
	Track3_CardData = ""
	TRK1DecryptData = ""
	TRK2DecryptData = ""
	TRK3DecryptData = ""
    
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
    for i in range (1, 7):
        if i == 1:
            DL.ShowMessageBox("Notice", "Swipe IDT test card --> Click OK")
        if i == 2:
            DL.ShowMessageBox("Notice", "Swipe VISA MSD card --> Click OK")
        if i == 3:
            DL.ShowMessageBox("Notice", "Swipe AAMVA card --> Click OK")
        if i == 4:
            DL.ShowMessageBox("Notice", "Swipe JIS 1 card --> Click OK")
        if i == 5:
            DL.ShowMessageBox("Notice", "Swipe JIS 2 card --> Click OK")
        if i == 6:
            DL.ShowMessageBox("Notice", "Swipe ISO 4909 (3T) card --> Click OK")
            
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)

        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02 00',
            'E8 DF EE 25 02 00 11', 
            'DF EE 23',
            '9F 39 01 90',
            'FF EE 01 05 DF EE 30 01 0C',
            'DF EE 26 02 E8 00',
            '9F 02 06 00 00 00 00 04 44',
            '9A 03',
            '9F 21 03']
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
            
        # call function: msr_data_analysis(strCardData)
        Track1_CardData, Track2_CardData, Track3_CardData, TRK1DecryptData, TRK2DecryptData, TRK3DecryptData = msr_data_analysis(strCardData)
            
        if i == 1:#IDT-----------------------------------------------------------
            target_patterns = [
                '83 3F 4F 28 6B 87 00',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR2maskdata = ";2121*****************************1212?*"
            TR1plaintextdata = "25545241434B31373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373F43"
            TR2plaintextdata = "3B323132313231323132313736373637363037303730373736373637363736323132313231323F30"
            TR3plaintextdata = "3B33333333333333333333373637363736303730373037373637363736333333333333333333333736373637363037303730373736373637363333333333333333333337363736373630373037303737363736373633333333333333333333373637363736303730373F32"

            tracks = [
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
                (TR3plaintextdata, TRK3DecryptData, "TR3plaintextdata"),
            ]

            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
        
        if i == 2:#VISA MSD-----------------------------------------------------------
            target_patterns = [
                '80 17 00 28 00 82 92',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR2maskdata = ";4761********0010=2012****************?"
            TR2plaintextdata = ";4761739001010010=20121200012339900031?"

            tracks = [
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
            ]

            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
        
        if i == 3:#AAMVA-----------------------------------------------------------
            target_patterns = [
                '81 3F 30 23 52 82 87',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR2maskdata = ";3555************************0303?*"
            TR1plaintextdata = "254E594E455720594F524B5E4C4545244252554345244A525E363535204E2E2042455252592053542E2C20234B5E3F52"
            TR2plaintextdata = "3B333535353535313131313131313131313131313D3030303931393737303330333F3F"
            TR3plaintextdata = "25232339323832312D30303434304141424242424242424242425454545446353037313235425257424C4B303132333435363738392020202020202020202020202020202043434343434353535353533F25"

            tracks = [
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
                (TR3plaintextdata, TRK3DecryptData, "TR3plaintextdata"),
            ]

            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                
        if i == 4:#JIS 1-----------------------------------------------------------
            target_patterns = [
                '80 1F 48 28 00 A3 9B',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR1maskdata = "a900*************************************************************0000"
            TR2maskdata = ";4322********2833=1108****************?*"
            TR1plaintextdata = "613930303030303030323131313131323334353637383930313232323232333333333334343434343535353535363636363637373737373838383838393939393930303030"
            TR2plaintextdata = "3B343332323036313030303837323833333D31313038323031383836343038323531303030303F3B"

            tracks = [
                (TR1maskdata, Track1_CardData, "TR1maskdata"),
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
            ]

            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                    
        if i == 5:#JIS 2-----------------------------------------------------------
            target_patterns = [
                '85 17 00 48 00 82 92',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR2maskdata = ";1234*************************************************************6789?*"
            TR2plaintextdata = "313233343536373839303132333435363738393031323334353637383930313233343536373839303132333435363738393031323334353637383930313233343536373839"

            tracks = [
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
            ]

            for mask, card, label in tracks:
                if not DL.Check_StringAB(mask, card):
                    DL.fails += 1
                    DL.SetWindowText("red", label + ": FAIL")
                    
        if i == 6:#ISO 4909 (3T)-----------------------------------------------------------
            target_patterns = [
                '80 3F 4D 27 69 87 BF',]

            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
            
            TR1maskdata = "%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
            TR2maskdata = ";4547********0000=1102***************?*"
            TR3maskdata = ";**4547********0000=***********************************************************************************?*"
            TR1plaintextdata = "2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F2E"
            TR2plaintextdata = "3B343534373537303030313037303030303D313130323130313030303030333036303030303F38"
            TR3plaintextdata = "3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F35"

            tracks = [
                (TR1maskdata, Track1_CardData, "TR1maskdata"),
                (TR2maskdata, Track2_CardData, "TR2maskdata"),
                (TR3maskdata, Track3_CardData, "TR3maskdata"),
                (TR1plaintextdata, TRK1DecryptData, "TR1plaintextdata"),
                (TR2plaintextdata, TRK2DecryptData, "TR2plaintextdata"),
                (TR3plaintextdata, TRK3DecryptData, "TR3plaintextdata"),
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