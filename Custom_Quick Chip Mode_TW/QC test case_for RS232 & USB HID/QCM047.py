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

# Objective: 
# NEO3-14580 [KIOSKV FW v1.01.359.2525.T][AT][CS-6236]No UID returned for Mifare DESFire virtual card in Auto transaction mode
# NEO3-14035, [VP3350][v2.00.012.2519.D] Under Auto Transaction mode, reader can not read the Mifare DESFire virtual card.
# NEO3-20529, [NEO3][K81][AT] Support Mifare Classic Card Information Output via TAG DFEC0F in AT Mode.
# NEO3-20564, [VP6325][v1.00.283.2648.T] Under Auto Transaction mode (USB-KB), reader can not read a Felica card.

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(11)
    
# cmd 04-00 to set tag DFEC20 (for DESFire virtual card)
if (Result):
	DL.SetWindowText("black", "*** 04-00 set DFEC20")
	DL.SendIOCommand("IDG", "04 00 DF EC 20 16 00 A4 04 00 10 A0 00 00 03 96 56 43 41 03 00 30 00 00 00 00 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# enable Felica auto switch 
if (Result):
	DL.SetWindowText("black", "*** DFEE7C = 02 = enable Felica auto switch")
	DL.SendIOCommand("IDG", "04 00 DF EE 7C 01 02", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)
#-----------------------------------------------------------------
if (Result):
    for i in range (1, 9):
        if i == 1:
            DL.ShowMessageBox("", "Tap Mifare Classic card (UID = any) --> Click OK")
        if i == 2:
            DL.ShowMessageBox("", "Tap Mifare DESFire card (UID = 04 9B 4C FA 22 2A 80) --> Click OK")
        if i == 3:
            DL.ShowMessageBox("", "Tap Mifare Ultralight card (UID = 04 C2 78 9A 63 1E 80) --> Click OK")
        if i == 4:
            DL.ShowMessageBox("", "Tap Mifare Ultralight C card (UID = 04 2B 6E 9A 67 34 80) --> Click OK")
        if i == 5:
            DL.ShowMessageBox("", "Tap Mifare DESFire Virtual card (Android MIFARE 2GO Client Test App w/ MIFARE 2GO Accenture Card Bundle.json) --> Click OK")
        if i == 6:
            DL.ShowMessageBox("black", "Tap Felica card (UID = 01 2E 30 D3 47 18 85 7B) --> Click OK")
        if i == 7:
            DL.ShowMessageBox("black", "Tap Mifare PlusX card (UID = 04 33 3F E2 08 5D 80) --> Click OK")
        if i == 8:
            DL.ShowMessageBox("black", "Tap Broadcom NFC tag 1 card (UID = 68 E3 D3 00) --> Click OK")
            
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)
        
        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02',]
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
              
        if i == 1:#Mifare Classic card
            if(-1 != strCardData.find('DF EC 0F 09 05 04 00 08 04')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 2:#Mifare DESFire card
            if(-1 != strCardData.find('DF EC 0F 11 01 44 03 20 07 04 9B 4C FA 22 2A 80 75 77 81 02 80')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 3:#Mifare Ultralight card
            if(-1 != strCardData.find('DF EC 0F 0C 02 44 00 00 07 04 C2 78 9A 63 1E 80')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 4:#Mifare Ultralight C card
            if(-1 != strCardData.find('DF EC 0F 0C 02 44 00 00 07 04 2B 6E 9A 67 34 80')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 5:#Mifare DESFire Virtual card
            if(-1 != strCardData.find('DF EC 0F 17 03 6F 12 85 10 14 02 0C 11 22 33 44 55 66 77 00 00 61 41 A9 5D 90 00')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 6:#Felica card 
            if(-1 != strCardData.find('DF EC 0F 13 04 FF FF 01 2E 30 D3 47 18 85 7B 00 F1 00 00 00 01 43 00')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
            DL.SetWindowText("black", "*** PT off")
            DL.SendIOCommand("IDG", "2C FB", 3000, 1) 
            time.sleep(0.5)
                
        if i == 7:#Mifare Plus 
            if(-1 != strCardData.find('DF EC 0F 17 06 44 00 20 07 04 33 3F E2 08 5D 80 75 77 80 02 C1 05 2F 2F 01 BC D6')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
                
        if i == 8:#Broadcom NFC tag
            if(-1 != strCardData.find('DF EC 0F 09 00 00 0C 00 04 6B E3 D3 00')):
                DL.SetWindowText("blue", "PASS")
            else:
                DL.SetWindowText("red", "FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------set to default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(11)

# Disable auto switch 
if (Result):
	DL.SetWindowText("black", "*** Disable auto switch")
	DL.SendIOCommand("IDG", "04 00 DF EE 7C 01 00", 3000, 1) 
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