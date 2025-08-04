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


ointerface = DL.ShowMessageBox("Check output interface", "Do u test Bluetooth output interface?", 0)

# Enable MSR Additional Tags (Pure and Fallback)
if (Result):
	DL.SetWindowText("black", "*** MSR Additional Tags (Pure and Fallback) = Enable")
	if ointerface == 0: #USB KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 01 00 00 00 00 00", 3000, 1) 
	if ointerface == 1: #Bluetooth KB
		DL.SendIOCommand("IDG", "04 00 DFEC4F 08 02 00 01 00 00 00 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# DFEF4B = 3F
if (Result):
	DL.SetWindowText("black", "*** DFEF4B = 3F")
	DL.SendIOCommand("IDG", "04 00 DF EF 4B 03 3F 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# DF7D = 01 (NEO2)
if (Result):
	DL.SetWindowText("black", "*** DF7D = 01 (NEO2)")
	DL.SendIOCommand("IDG", "04 00 DF EE 7D 01 01 ", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)