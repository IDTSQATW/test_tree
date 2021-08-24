#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

if (Result):
	DL.SetWindowText("black", "*** 04-09")
	DL.SendIOCommand("IDG", "04 09", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** DFED59 =  00 (Send First Response 0x63)")
	DL.SendIOCommand("IDG", "04 00 DF ED 59 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")

#Send cmd 60-10, w/o inserting CT card, cancel the cmd
if (Result):
	DL.SetWindowText("black", "*** 60-10 Contact Start Transaction")
	DL.SendIOCommand("IDG", "60 10 01 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40", 120000, 1) 
    
	DL.SetWindowText("black", "*** 05-01 Cancel transaction")
	DL.SendIOCommand("IDG", "05 01", 3000, 1) 
	Result = DL.Check_RXResponse("05 00 00 00")	

#Send cmd 60-10, w/ inserting CT card, cancel the cmd
if (Result):
	DL.SetWindowText("black", "*** 60-10 Contact Start Transaction, Please insert  EMV Test Card (T=0)..........")
	DL.SendIOCommand("IDG", "60 10 01 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40", 120000, 1) 

	DL.SetWindowText("black", "*** 05-01 Cancel transaction")
	DL.SendIOCommand("IDG", "05 01", 3000, 1) 
	Result = DL.Check_RXResponse("05 00 00 00")	