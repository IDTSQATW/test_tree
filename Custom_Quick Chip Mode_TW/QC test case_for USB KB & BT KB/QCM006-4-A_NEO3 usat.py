#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

#Objective: Encryption ON, MSR test under Quick Chip Mode. (IDT/ VISA MSD/ AAMVA/ JIS 2/ ISO4909 3T)

# # Poll on demand
# if (Result):
	# DL.SetWindowText("black", "*** Poll on demand")
	# DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	# Result = DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(12)
    
# # Set DF7D = 02 (NEO2)
# if (Result):
	# DL.SetWindowText("black", "*** Set DF7D = 02 (NEO2)")
	# DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 02", 3000, 1) 
	# DL.Check_RXResponse("04 00 00 00")	

# # QuickChip mode
# if (Result):
	# DL.SetWindowText("black", "*** QuickChip mode (02)")
	# DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	# DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(10)
    
# # Get DUKPT DEK Attribution based on KeySlot (C7-A3)
# if (Result):
	# DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	# DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	# Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
	# time.sleep(0.5)
#-----------------------------------------------------------------
def verify_data(source_data, expected_substring, label):
    if expected_substring in source_data:
        DL.SetWindowText("blue", label + " PASS")
    else:
        DL.SetWindowText("red", label + " FAIL")
        DL.fails += 1
        
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    for i in range (1, 7):
        if i == 1:
            DL.SetWindowText("black", "*** Swipe IDT test card")
        if i == 2:
            DL.SetWindowText("black", "*** Swipe AAMVA card")
        if i == 3:
            DL.SetWindowText("black", "*** Swipe JIS 1 card")
        if i == 4:
            DL.SetWindowText("black", "*** Swipe JIS 2 card")
        if i == 5:
            DL.SetWindowText("black", "*** Swipe VISA MSD card")
        if i == 6:
            DL.SetWindowText("black", "*** Swipe ISO 4909 (3T) card")
            
        strCardData = DL.ReadKeyBoardCardData(60000)
        
        if i == 1:#IDT
            # Tracks data, ASCII convert to HEX
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:66]) + strCardData[66:716]
            # Length update
            l = str(0) + str(hex((len(rawdata) - 12) / 2)[2:])
            l = l[2:] + l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:756]
            rawdata = rawdata.upper()
            # LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:750])
            checksum = DL.GetSUM(rawdata[6:750])
            # Final MSR data
            rawdata = rawdata[0:750] + lrc + checksum + rawdata[754:756]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
                
            test_cases = [
                (strCardData, '837F4F286B82BF021600', 'MSR format'),
                (strCardData, ';2121*****************************1212?*', 'Mask2 data'),
                ('25545241434B31373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373F4300', TRK1DecryptData, 'TRK1DecryptData'),
                ('3B323132313231323132313736373637363037303730373736373637363736323132313231323F300000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
                ('3B33333333333333333333373637363736303730373037373637363736333333333333333333333736373637363037303730373736373637363333333333333333333337363736373630373037303737363736373633333333333333333333373637363736303730373F320000000000', TRK3DecryptData, 'TRK3DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
        
        if i == 2:#AAMVA
            # Tracks data, ASCII convert to HEX
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:61]) + strCardData[61:615]
            # Length update
            l = str(0) + str(hex((len(rawdata) - 12) / 2)[2:])
            l = l[2:] + l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:650]
            rawdata = rawdata.upper()
            # LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:644])
            checksum = DL.GetSUM(rawdata[6:644])
            # Final MSR data
            rawdata = rawdata[0:644] + lrc + checksum + rawdata[648:650]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
                
            test_cases = [
                (strCardData, '817F30235282BF021600', 'MSR format'),
                (strCardData, ';3555************************0303?*', 'Mask2 data'),
                ('254E594E455720594F524B5E4C4545244252554345244A525E363535204E2E2042455252592053542E2C20234B5E3F52', TRK1DecryptData, 'TRK1DecryptData'),
                ('3B333535353535313131313131313131313131313D3030303931393737303330333F3F00000000000000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
                ('25232339323832312D30303434304141424242424242424242425454545446353037313235425257424C4B303132333435363738392020202020202020202020202020202043434343434353535353533F250000000000000000000000000000', TRK3DecryptData, 'TRK3DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
        
        if i == 3:#JIS 1
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:138])+ strCardData[138:524]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:636]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:630])
            checksum = DL.GetSUM(rawdata[6:630])
            #Final MSR data
            rawdata = rawdata[0:630] + lrc + checksum + rawdata[634:636]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            
            test_cases = [
                (strCardData, '805F482800A39B021600', 'MSR format'),
                (strCardData, ';a900*************************************************************0000?', 'Mask1 data'),
                (strCardData, ';4322********2833=1108****************?*', 'Mask2 data'),
                ('7F6139303030303030303231313131313233343536373839303132323232323333333333343434343435353535353636363636373737373738383838383939393939303030307F150000000000000000', TRK1DecryptData, 'TRK1DecryptData'),
                ('3B343332323036313030303837323833333D31313038323031383836343038323531303030303F3B0000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
        
        if i == 4:#JIS 2
            # Tracks data, ASCII convert to HEX
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:98]) + strCardData[98:412]
            # Length update
            l = str(0) + str(hex((len(rawdata) - 12) / 2)[2:])
            l = l[2:] + l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:484]
            rawdata = rawdata.upper()
            # LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:478])
            checksum = DL.GetSUM(rawdata[6:478])
            # Final MSR data
            rawdata = rawdata[0:478] + lrc + checksum + rawdata[482:484]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
                
            test_cases = [
                (strCardData, '85570048008292021600', 'MSR format'),
                (strCardData, ';1234*************************************************************6789?*', 'Mask2 data'),
                ('3132333435363738393031323334353637383930313233343536373839303132333435363738393031323334353637383930313233343536373839303132333435363738390000000000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
            
        if i == 5:#VISA MSD
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:66])+ strCardData[66:252]
            #Length update
            l = str(0)+str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:292]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:286])
            checksum = DL.GetSUM(rawdata[6:286])
            #Final MSR data
            rawdata = rawdata[0:286] + lrc + checksum + rawdata[290:292]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
                
            test_cases = [
                (strCardData, '80570028008292021600', 'MSR format'),
                (strCardData, ';4761********0010=2012****************?', 'Mask2 data'),
                ('3B343736313733393030313031303031303D32303132313230303031323333393930303033313F320000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
                
        if i == 6:#ISO 4909 (3T)
            #Tracks data, ASCII convert to HEX 
            rawdata = strCardData[0:26] + DL.stringToHexString(strCardData[26:247])+ strCardData[247:897]
            #Length update
            l = str(0)+str(hex((len(rawdata)-12)/2)[2:])
            l = l[2:]+l[0:2]
            rawdata = rawdata[0:2] + l + rawdata[6:1118]
            rawdata = rawdata.upper()
            #LRC/ check sum update
            lrc = DL.GetLRC(rawdata[6:1112])
            checksum = DL.GetSUM(rawdata[6:1112])
            #Final MSR data
            rawdata = rawdata[0:1112] + lrc + checksum + rawdata[1116:1118]
            objectMSR = DL.ParseCardData(rawdata, Key)
            KSN = DL.Get_KSN_CardData()
            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
            TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
            TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
                           
            test_cases = [
                (strCardData, '807F4D276987BF021600', 'MSR format'),
                (strCardData, '%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*', 'Mask1 data'),
                (strCardData, ';4547********0000=1102***************?*', 'Mask2 data'),
                (strCardData, ';**4547********0000=***********************************************************************************?*', 'Mask3 data'),
                ('2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F2E000000', TRK1DecryptData, 'TRK1DecryptData'),
                ('3B343534373537303030313037303030303D313130323130313030303030333036303030303F38000000000000000000', TRK2DecryptData, 'TRK2DecryptData'),
                ('3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F3500000000000000', TRK3DecryptData, 'TRK3DecryptData'),
            ]
            for target_data, expected_val, test_name in test_cases:
                verify_data(target_data, expected_val, test_name)
else:
    DL.fails=DL.fails+1
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )