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

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)

# Set CT terminal data = 5C w/ tag DFEF59.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF59")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DF EF 59 06 00 00 00 00 00 11", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
# Set transaction interface = CT only.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 04", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# CT transaction
if (Result): 
    DL.ShowMessageBox("Card", "*** Click OK --> Insert EMV T=0 card", 0)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEF59')):
        DL.SetWindowText("red", "DFEF59 FAIL")
        DL.fails=DL.fails+1

    if(-1 != strCardData.find('DFEE2502')):
        DL.SetWindowText("blue", "DFEE25 PASS")
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
        
    if(-1 != strCardData.find('9F0306000000000000')):
        DL.SetWindowText("blue", "9F03 PASS")
    else:
        DL.SetWindowText("red", "9F03 FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)

# Set CT terminal data = 5C w/ tag DFEF5A.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF5A")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DF EF 5A 04 57 5A 9F 39", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# CT transaction
if (Result): 
    DL.ShowMessageBox("Card", "*** Click OK --> Insert EMV T=0 card", 0)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('57')):
        DL.SetWindowText("blue", "57 PASS")
    else:
        DL.SetWindowText("red", "57 FAIL")
        DL.fails=DL.fails+1
        
    if(-1 != strCardData.find('5A')):
        DL.SetWindowText("blue", "5A PASS")
    else:
        DL.SetWindowText("red", "5A FAIL")
        DL.fails=DL.fails+1
        
    if(-1 != strCardData.find('9F39')):
        DL.SetWindowText("blue", "9F39 PASS")
    else:
        DL.SetWindowText("red", "9F39 FAIL")
        DL.fails=DL.fails+1

    rxcheck = DL.ShowMessageBox("", "Data output list meet tag DFEF5A -- DFEE25/ 57/ 5A/ 9F39/ DFEE26/ DFEF57 only (& DFEF4C/ DFEF4D are controlled by DFEF4B)?", 0)
    if rxcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set tags DFED20/ DFED21/ DFED22
if (Result):
	DL.SetWindowText("black", "*** Set tags DFED20/ DFED21/ DFED22")
	DL.SendIOCommand("IDG", "04 00 df ed 20 06 53 6c 69 6d 43 44 df ed 21 03 11 02 18 df ed 22 0a 31 2e 33 7c 30 34 32 33 31 38", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# Set CT terminal data = 5C w/ tag DFEF5A.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag DFEF5A")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DF EF 5A 09 DF ED 20 DF ED 21 DF ED 22", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = All")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):       
    DL.ShowMessageBox("Card", "*** Click OK --> Insert EMV T=0 card", 0)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFED2006536C696D4344DFED2103110218DFED220A312E337C303432333138')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
    # for JIRA#CS-3869
    DL.ShowMessageBox("Card", "*** Click OK --> Tap any CL card", 0)
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFED2006536C696D4344DFED2103110218DFED220A312E337C303432333138')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set CT terminal data = 5C w/ tag 9F53.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag 9F53")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 9F 53 01 50", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# Set transaction interface = CT only.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT only")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 04", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result):       
    DL.ShowMessageBox("Card", "*** Click OK --> Insert EMV T=0 card", 0)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('9F530150')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)

# Set CT terminal data = 5C w/ tag 9F53.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C w/ tag 9F53")
	DL.SendIOCommand("IDG", "60 06 09 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 9F 53 01 52 DF EF 5A 02 9F 53", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

if (Result):       
    DL.ShowMessageBox("Card", "*** Click OK --> Insert EMV T=0 card", 0)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('9F530152')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)

#/////////////////////////////////// Return to default setting
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)

# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = ALL")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# Set transaction interface = ALL.
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 07 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )