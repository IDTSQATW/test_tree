#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Poll On Demand/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Poll On Demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
# cmd 02-01
if (Result):
	DL.SetWindowText("black", "*** cmd 02-01, Please tap 45#-MC CRL..........")
	DL.SendIOCommand("IDG", "02 01 20 9F 02 06 00 00 00 00 03 33", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")