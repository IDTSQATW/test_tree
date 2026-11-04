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

#Objective: Encryption OFF, CT + Fallback to CT + Fallback to MSR test under Quick Chip Mode. (T=0/ Discover)

#---------------------------------------------------------Define main test, use subroutine
def read_card():
    if (Result):       
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
        for i in range (1, 4):
            if i == 1:
                DL.ShowMessageBox("Notice", "Insert T=0 card --> (read over, remove card) --> Click OK")
            if i == 2:
                DL.ShowMessageBox("Notice", "Swipe Discover card (PAN = xxxx....0026) --> Click OK")
            if i == 3:
                DL.ShowMessageBox("Notice", "Insert MSR card: the 1st time (remove card) --> Click OK")
            strCardData = DL.GetResponse()
            DL.SetWindowText("blue", strCardData)
            
            target_patterns = [
                '56 69 56 4F 74 65 63 68 32 00 02',]
            if all(pattern in strCardData for pattern in target_patterns):
                DL.SetWindowText("GREEN", "Format PASS")
            else:
                DL.SetWindowText("red", "Format FAIL")
                DL.fails=DL.fails+1
                
            if i == 1:#T=0 card
                target_patterns1 = [
                    '20 DF EE 26 02 20 00',
                    'DF EE 25 02 00 03',
                    '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89',
                    '5A 08 47 61 73 90 01 01 00 10',
                    '9F 39',
                    '4F',
                    '50',
                    '82 02',
                    '84 07 A0 00 00 00 03 10 10',
                    '8A',
                    '8C',
                    '8D',
                    '8E',
                    '95 05',
                    '99',
                    '9B',
                    '9C',
                    '5F 20',
                    '5F 24',
                    '5F 25',
                    '5F 28',
                    '5F 2A',
                    '5F 2D',
                    '5F 34',
                    '5F 57',
                    '9F 02',
                    '9F 03',
                    '9F 10',
                    '9F 13',
                    '9F 20',
                    '9F 26',
                    '9F 27',
                    '9F 34',
                    '9F 36',
                    '9F 37',
                    '9F 38',
                    '9F 4D',
                    '9F 4F',
                    '9F 53',
                    '9F 5B',
                    'DF EF 57',
                    'DF EC 18',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "T=0 card PASS")
                else:
                    DL.SetWindowText("red", "T=0 card FAIL")
                    DL.fails=DL.fails+1
                    
            if i == 2:#Discover card (PAN = xxxx....0026)
                target_patterns1 = [
                    '28 DF EE 25 02 00 11', 
                    'DF EE 23',
                    '02 7D 00 80 1F 44 28 00 A3 00 25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 5E 43 41 52 44 2F 49 4D 41 47 45 20 30 33 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 25 3B 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 3D 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 3B',
                    '9F 39 01 90',
                    'FF EE 01 05 DF EE 30 01 0C',
                    'DF EE 26 02 28 00',
                    '9F 02 06 00 00 00 00 04 44',
                    '9A 03',
                    '9F 21 03',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Discover card PASS")
                else:
                    DL.SetWindowText("red", "Discover card FAIL")
                    DL.fails=DL.fails+1
            
            if i == 3:#Fallback to MSR transaction, Discover card (PAN = xxxx....0026)
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 50',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                
                DL.ShowMessageBox("Notice", "Insert MSR card: the 2nd time (remove card) --> Click OK")
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 50',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                    
                DL.ShowMessageBox("Notice", "Insert MSR card: the 3rd time (remove card) --> Click OK")
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                target_patterns1 = [
                    '56 69 56 4F 74 65 63 68 32 00 02',
                    'DF EF 61 02 F2 22',]
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Format PASS")
                else:
                    DL.SetWindowText("red", "Format FAIL")
                    DL.fails=DL.fails+1
                
                DL.ShowMessageBox("Notice", "Swipe Discover card (PAN = xxxx....0026) --> Click OK")
                strCardData = DL.GetResponse()
                DL.SetWindowText("blue", strCardData)
                target_patterns1 = [
                    '28 DF EE 25 02 00 07', 
                    'DF EE 23',
                    '02 7D 00 80 1F 44 28 00 A3 00 25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 5E 43 41 52 44 2F 49 4D 41 47 45 20 30 33 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 25 3B 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 3D 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 3B',
                    '9F 39 01 80',
                    'FF EE 01 05 DF EE 30 01 0C',
                    'DF EE 26 02 28 00',
                    '9F 02 06 00 00 00 00 04 44',
                    '9A 03',
                    '9F 21 03']
                if all(pattern in strCardData for pattern in target_patterns1):
                    DL.SetWindowText("GREEN", "Discover card PASS")
                    ledcheck = DL.ShowMessageBox("LED", "When fall back to MSR reader, green LED 4 was turned FLASH ON?", 0)
                    if ledcheck == 0: 
                        DL.SetWindowText("red", "LED behavior FAIL")
                        DL.fails=DL.fails+1
                else:
                    DL.SetWindowText("red", "Discover card FAIL")
                    DL.fails=DL.fails+1
    else:
        DL.fails=DL.fails+1
#---------------------------------------------------------Set 5C CT termianl data
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
        
# Set CT ICS Identification = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT ICS Identification = 5C")
	DL.SendIOCommand("IDG", "60 16 05", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set CT terminal data = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 16 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# Set transaction interface = ALL
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = ALL")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# DF7D = 01 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Get Data Encryption (C7-37) = encryption OFF
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	DL.Check_RXResponse("C7 00 00 01 00")
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
#---------------------------------------------------------Start main test
read_card()
#---------------------------------------------------------Set 4C CT termianl data
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(5)
        
# Set CT ICS Identification = 4C
if (Result):
	DL.SetWindowText("black", "*** Set CT ICS Identification = 4C")
	DL.SendIOCommand("IDG", "60 16 04", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set CT terminal data = 4C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 4C")
	DL.SendIOCommand("IDG", "6006 16009f33036008c89f3501259f40056000f05001df110101df260101df270100dfee1e08d09c20f0c20e16005f3601029f1a0208409f1e085465726d696e616c9f150212349f160f3030303030303030303030303030309f1c0838373635343332319f4e2231303732312057616c6b65722053742e20437970726573732c204341202c5553412edfee150101dfee160100dfee170105dfee180180dfee1f0180dfee1b083030303135313030dfee2203323c3cdf1008656e667265737a68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

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
#---------------------------------------------------------Start main test
read_card()
#---------------------------------------------------------Change to default
# # Poll on demand
# if (Result):
	# DL.SetWindowText("black", "*** Poll on demand")
	# DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	# Result = DL.Check_RXResponse("01 00 00 00")	
	# time.sleep(5)
    
# # Enable 3 interfaces
# if (Result):
	# DL.SetWindowText("black", "*** Enable All interfaces")
	# DL.SendIOCommand("IDG", "04 00 DF EF 37 01 03", 3000, 1)     #VP6328 only can enable CL +MSR
	# time.sleep(0.2)    
	# DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1)     #VP6328 can not accept this cmd 
	# time.sleep(0.2) 
    
# # QuickChip mode
# if (Result):
	# DL.SetWindowText("black", "*** QuickChip mode (02)")
	# DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	# DL.Check_RXResponse("01 00 00 00")	
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )