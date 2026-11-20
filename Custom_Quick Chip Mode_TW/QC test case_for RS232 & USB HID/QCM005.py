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

# Objective: to verify 2 tags DFEF5A & DFEF59 in terminal data.

#-----------------------------------------------------------------Set CT terminal data = 5C w/ tag DFEF59.
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set CT terminal data = 5C w/ tag DFEF59.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF59")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DF EF 59 06 00 00 00 00 00 11", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set transaction interface = CT only.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 04", 3000, 1) 
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

# CT transaction
if (Result): 
    DL.ShowMessageBox("Card", "Insert T=0 card --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    required_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EE 25 02',
        '9F 03 06 00 00 00 00 00 00',
    ]
    forbidden_pattern = 'DF EF 59'

    if all(pattern in strCardData for pattern in required_patterns) and (forbidden_pattern not in strCardData):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails = DL.fails + 1
#-----------------------------------------------------------------Set CT terminal data = 5C w/ tag DFEF5A.
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set CT terminal data = 5C w/ tag DFEF5A.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF5A")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DF EF 5A 04 57 5A 9F 39", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

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
    
# CT transaction
if (Result): 
    DL.ShowMessageBox("Card", "Insert T=0 card --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        '57',
        '5A',
        '9F 39',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails=DL.fails+1

    rxcheck = DL.ShowMessageBox("", "Data output list meet tag DFEF5A -- DFEE25/ 57/ 5A/ 9F39/ DFEE26/ DFEF57 only (& DFEF4C/ DFEF4D are controlled by DFEF4B)?", 0)
    if rxcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------Set tags DFED20/ DFED21/ DFED22
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set tags DFED20/ DFED21/ DFED22
if (Result):
	DL.SetWindowText("black", "*** Set tags DFED20/ DFED21/ DFED22")
	DL.SendIOCommand("IDG", "04 00 df ed 20 06 53 6c 69 6d 43 44 df ed 21 03 11 02 18 df ed 22 0a 31 2e 33 7c 30 34 32 33 31 38", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	
    
# Set CT terminal data = 5C w/ tag DFEF5A.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF5A")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DF EF 5A 09 DF ED 20 DF ED 21 DF ED 22", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = All")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
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
    
if (Result):       
    DL.ShowMessageBox("Card", "Insert T=0 card --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF ED 20 06 53 6C 69 6D 43 44 DF ED 21 03 11 02 18 DF ED 22 0A 31 2E 33 7C 30 34 32 33 31 38',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails=DL.fails+1
        
    # for JIRA#CS-3869
    DL.ShowMessageBox("Card", "Tap any CL card --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF ED 20 06 53 6C 69 6D 43 44 DF ED 21 03 11 02 18 DF ED 22 0A 31 2E 33 7C 30 34 32 33 31 38',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------Set CT terminal data = 5C w/ tag 9F53.
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(11)
    
# Set CT terminal data = 5C w/ tag 9F53.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag 9F53")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 9F 53 01 50", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# Set transaction interface = CT only.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 04", 3000, 1) 
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
    
if (Result):       
    DL.ShowMessageBox("Card", "Insert T=0 card --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        '9F 53 01 50',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------Set CT terminal data = 5C w/ tag 9F53.
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set CT terminal data = 5C w/ tag 9F53.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag 9F53")
	DL.SendIOCommand("IDG", "60 06 18 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 9F 53 01 52 DF EF 5A 02 9F 53", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

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

if (Result):       
    DL.ShowMessageBox("Card", "Insert T=0 card --> (read over, remove card) --> Click OK", 0)
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    
    target_patterns = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        '9F 53 01 52',]
    if all(pattern in strCardData for pattern in target_patterns):
        DL.SetWindowText("GREEN", "Data PASS")
    else:
        DL.SetWindowText("red", "Data FAIL")
        DL.fails=DL.fails+1
#/////////////////////////////////////////////////////////////////////////// Return to default setting
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = ALL")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	

# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 16 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(1)

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )