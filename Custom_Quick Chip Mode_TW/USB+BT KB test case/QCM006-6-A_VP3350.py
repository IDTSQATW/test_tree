#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Objective: Encryption ON, CL test under Quick Chip Mode. (Discover/ VISA MSD/ VISA qVSDC (EMV)/ MasterCard (MSD)/ MChip (EMV)/ INTERAC)

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	DL.SetWindowText("black", "*** Get DUKPT DEK Attribution based on KeySlot (C7-A3)")
	DL.SendIOCommand("IDG", "C7 A3 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
	time.sleep(0.5)
#-----------------------------------------------------------------
if (Result):       
    for i in range (1, 8):
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
        if i == 1:
            DL.SetWindowText("black", "*** Tap Discover #84 card")
        if i == 2:
            DL.SetWindowText("black", "*** Tap INTERAC card")
        if i == 3:
            DL.SetWindowText("black", "*** Tap VISA #97 card")
        if i == 4:
            DL.SetWindowText("black", "*** Tap MasterCard MC21 card")
        if i == 5:
            DL.SetWindowText("black", "*** Tap AMEX XP8 #86 card")
        if i == 6:
            DL.SetWindowText("black", "*** Tap JCB EMV card")
        if i == 7:
            DL.SetWindowText("black", "*** Tap CUP #69 card")
            
        strCardData = DL.ReadKeyBoardCardData(60000)
        ksn = DL.GetTLV(strCardData, "DFEE12")
        
        if i == 1:#Discover #84
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B083607CCCCCCC0001F')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A08360705000000001F'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D123607CCCCCCC0001D4912CCCCCCCCCCCCCCCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '5712360705000000001D49121010000332112301'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#INTERAC
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B085413CCCCCCCC1513')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A085413339000001513'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D115413CCCCCCCC1513D0512CCCCCCCCCCCCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '57115413339000001513D05122200123456789'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#VISA #97 card
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B074761CCCCCC0100')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A0747617390010100'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D124761CCCCCC0100D2012CCCCCCCCCCCCCCCCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            Result = DL.Check_StringAB(dec57, '571247617390010100D20121200012339900031F')
            if Result == True:
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
        
        if i == 4:#MasterCard MC21
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B085413CCCCCCCC0010')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A085413330089600010'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D115413CCCCCCCC0010D1412CCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '57115413330089600010D1412201'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
            
        if i == 5:#AMEX XP8#86
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B083742CCCCCCC0001F')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A08374245455400001F'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D133742CCCCCCC0001D1410CCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '5713374245455400001D1410'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
            
        if i == 6:#JCBO-48250
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B083540CCCCCCCC1012')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A083540829999421012'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D133540CCCCCCCC1012D4912CCCCCCCCCCCCCCCCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '57133540829999421012D4912201555555555555'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
            
        if i == 7:#CUP#69
            # Check mask 5A = DFEF5B
            if(-1 != strCardData.find('DFEF5B086228CCCCCCCC1117')):
                DL.SetWindowText("blue", "DFEF5B PASS")
            else:
                DL.SetWindowText("red", "DFEF5B FAIL")
                DL.fails=DL.fails+1
            # Check enc 5A
            enc5A = DL.GetTLV_Embedded(strCardData,"5A", 0)
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
            if DL.Check_StringAB(dec5A, '5A086228000100001117'):
                DL.SetWindowText("blue", "5A PASS")
            else:
                DL.SetWindowText("red", "5A FAIL")
                DL.fails=DL.fails+1
            # Check mask 57 = DFEF5D
            if(-1 != strCardData.find('DFEF5D136228CCCCCCCC1117D2012CCC')):
                DL.SetWindowText("blue", "DFEF5D PASS")
            else:
                DL.SetWindowText("red", "DFEF5D FAIL")
                DL.fails=DL.fails+1
            # Check enc 57
            enc57 = DL.GetTLV_Embedded(strCardData,"57", 0)
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
            if DL.Check_StringAB(dec57, '57136228000100001117D2012120'):
                DL.SetWindowText("blue", "57 PASS")
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
            
        # Check 9F39
        if(-1 != strCardData.find('9F390107')):
            DL.SetWindowText("blue", "9F39 PASS")
        else:
            DL.SetWindowText("red", "9F39 FAIL")
            DL.fails=DL.fails+1
        # Check DFEE26
        if(-1 != strCardData.find('DFEE2602E501')):
            DL.SetWindowText("blue", "DFEE26 PASS")
        else:
            DL.SetWindowText("red", "DFEE26 FAIL")
            DL.fails=DL.fails+1
        # Check DFEC18
        if i == 1:
            result = (-1 != strCardData.find('DFEC1818446973636F766572204450415320322E302C2076312E3030'))
        if i == 2:
            result = (-1 != strCardData.find('DFEC1813496E746572616320312E38612C2076312E3030'))
        if i == 3:
            result = (-1 != strCardData.find('DFEC1810564350532076322E322C2076312E3030'))
        if i == 4:
            result = (-1 != strCardData.find('DFEC18174D61737465724361726420332E312E342C2076312E3030'))
        if i == 5:
            result = (-1 != strCardData.find('DFEC181A416D6578204578707265737350617920342E312C2076312E3030'))
        if i == 7:
            result = (-1 != strCardData.find('DFEC181B515549435320312E302E32205549435320332E302C2076312E3030'))
        if result == True:
            DL.SetWindowText("blue", "DFEC18 PASS")
        else:
            DL.SetWindowText("red", "DFEC18 FAIL")
            DL.fails=DL.fails+1
        # Check DFEF57
        if i != 6:
            if(-1 != strCardData.find('DFEF57')):
                DL.SetWindowText("blue", "DFEF57 PASS")
            else:
                DL.SetWindowText("red", "DFEF57 FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )