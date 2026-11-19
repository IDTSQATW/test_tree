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

# Objective: [JIRA] GRN-59 >> [Quick Chip Mode] Fallback to chip reader -> inserted card w/ opposite direction (IC chip can not be powered on) -> reinserted card normally, reader can not read the card.
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(11)
    
# Set CT terminal data = 5C (enable MSR fallback to CT function)
if (Result):
	DL.SetWindowText("black", "*** Set CT ICS Identification = 5C")
	DL.SendIOCommand("IDG", "60 16 05", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	
    
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (enable MSR fallback to CT function)")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DFEF62 01 01", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
#-----------------------------------------------------------------
for j in range (1, 3):
    if j == 2:     #test 4C
        DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        # Poll on demand
        if (Result):
            DL.SetWindowText("black", "*** Poll on demand")
            DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
            Result = DL.Check_RXResponse("01 00 00 00")	
            time.sleep(10)
            
        # Set CT terminal data = 4C (enable MSR fallback to CT function)
        if (Result):
            DL.SetWindowText("black", "*** Set CT ICS Identification = 4C")
            DL.SendIOCommand("IDG", "60 16 04", 3000, 1) 
            DL.Check_RXResponse("60 00 00 00")	
        if (Result):
            DL.SetWindowText("black", "*** Set CT terminal data = 4C (enable MSR fallback to CT function)")
            DL.SendIOCommand("IDG", "60 06 17009f33036008c89f3501259f40056000f05001df110101df260101df270100dfee1e08d09c20f0c20e16005f3601029f1a0208409f1e085465726d696e616c9f150212349f160f3030303030303030303030303030309f1c0838373635343332319f4e2231303732312057616c6b65722053742e20437970726573732c204341202c5553412edfee150101dfee160100dfee170105dfee180180dfee1f0180dfee1b083030303135313030dfee2203323c3cdf1008656e667265737a68 DFEF62 01 01", 3000, 1) 
            DL.Check_RXResponse("60 00 00 00")	

        # QuickChip mode
        if (Result):
            DL.SetWindowText("black", "*** QuickChip mode (02)")
            DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
            DL.Check_RXResponse("01 00 00 00")	
            time.sleep(10)

    # Fallback to CT transaction
    if (Result): 
        DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
        strCardData1 = DL.ReadKeyBoardCardData(30000)
        DL.SetWindowText("black", "*** Insert EMV T=0 card")
        strCardData2 = DL.ReadKeyBoardCardData(30000)
        if(-1 != strCardData2.find('DFEE25020003')):
            if(-1 != strCardData2.find('57114761739001010010D20122010123456789')):
                if(-1 != strCardData2.find('5A084761739001010010')):
                    if(-1 != strCardData2.find('9F3901')):
                        if(-1 != strCardData2.find('DFEF57')):
                            if(-1 != strCardData2.find('DFEC181D454D5620436F6D6D6F6E2047656E2033204C322056312E33302E303339')):
                                DL.SetWindowText("blue", "PASS")
                            else:
                                DL.SetWindowText("red", "DFEC18 FAIL")
                                DL.fails=DL.fails+1
                        else:
                            DL.SetWindowText("red", "DFEF57 FAIL")
                            DL.fails=DL.fails+1
                    else:
                        DL.SetWindowText("red", "9F39 FAIL")
                        DL.fails=DL.fails+1
                else:
                    DL.SetWindowText("red", "5A FAIL")
                    DL.fails=DL.fails+1
            else:
                DL.SetWindowText("red", "57 FAIL")
                DL.fails=DL.fails+1
        else:
            DL.SetWindowText("red", "DFEE25 FAIL")
            DL.fails=DL.fails+1
            DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, LED 3 was turned ON (steady status)?", 0)
        if speedcheck != 1:
            DL.SetWindowText("Red", "LED FAIL")
            DL.fails=DL.fails+1
    else:
        DL.fails=DL.fails+1
            
    # Fallback to CT, then Fallback to MSR
    if (Result): 
        DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
        DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
        strCardData1 = DL.ReadKeyBoardCardData(10000)
        if(-1 != strCardData1.find('DFEF6102F220')):
            DL.SetWindowText("blue", "PASS")
        else:
            DL.SetWindowText("red", "Error code FAIL")
            DL.fails=DL.fails+1
        DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
        strCardData1 = DL.ReadKeyBoardCardData(15000)
        DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
        strCardData1 = DL.ReadKeyBoardCardData(15000)
        DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
        strCardData1 = DL.ReadKeyBoardCardData(15000)
        if(-1 != strCardData1.find('DFEF6102F222')):
            DL.SetWindowText("blue", "PASS")
        else:
            DL.SetWindowText("red", "Error code FAIL")
            DL.fails=DL.fails+1
        DL.SetWindowText("black", "*** Swipe Discover card")
        strCardData2 = DL.ReadKeyBoardCardData(15000)
        if(-1 != strCardData2.find('DFEE25')):
            if(-1 != strCardData2.find('9F390180')):
                if(-1 != strCardData2.find('DFEE236A%B6510000000000125^CARD/IMAGE 08             ^17122011000095000000?;6510000000000125=17122011000095000000?')):
                    DL.SetWindowText("blue", "PASS")
                else:
                    DL.SetWindowText("red", "DFEE23 FAIL")
                    DL.fails=DL.fails+1
            else:
                DL.SetWindowText("red", "9F39 FAIL")
                DL.fails=DL.fails+1
        else:
            DL.SetWindowText("red", "DFEE25 FAIL")
            DL.fails=DL.fails+1
            DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, LED 3 was turned ON (steady status); When fallback to MSR reader, LED 3 was turned ON (flash status)?", 0)
        if speedcheck != 1:
            DL.SetWindowText("Red", "LED FAIL")
            DL.fails=DL.fails+1
    else:
        DL.fails=DL.fails+1
    
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )