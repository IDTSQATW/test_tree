#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Aull Poll/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Auto Poll")
	DL.SendIOCommand("IDG", "01 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# cmd 03-00
if (Result):
	DL.ShowMessageBox("CL card", "Tap 3#-Discover ZIP No.01 card , then click OK", 0)
	DL.SetWindowText("black",'----- cmd 03-00')
	DL.SendIOCommand("IDG", "0300", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 03 23")
	
# cmd 03-40
if (Result):
	DL.ShowMessageBox("CL card", "Tap 3#-Discover ZIP No.01 card , then click OK", 0)
	DL.SetWindowText("black",'----- cmd 03-40')
	DL.SendIOCommand("IDG", "0340", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 03 23")	
	
if Result == False:
	DL.SetWindowText("red",'=============== Test result: FAIL ===============')
else:
	DL.SetWindowText("green",'=============== Test result: PASS ===============')