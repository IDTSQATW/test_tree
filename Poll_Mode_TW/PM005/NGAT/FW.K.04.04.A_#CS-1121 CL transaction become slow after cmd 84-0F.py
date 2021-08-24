#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

readercheck = DL.ShowMessageBox("Notice", "Is this SRED reader?", 0)

# Poll On Demand/ Burst mode off
if (Result):
	DL.SetWindowText("black", "*** Poll On Demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** Burst mode off")
	DL.SendIOCommand("IDG", "04 00 DF EE 7E 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
	
def cmd_840F():
	DL.SetWindowText("black", "*** cmd 84-0F")
	DL.SendIOCommand("IDG", "84 0F", 32000, 1) 
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 84 00")
		
def timecheck():
	usercheck = DL.ShowMessageBox("Time", "Does the reader read card slowly after sent cmd 84-0F?", 0)
	if usercheck == 1:
		DL.SetWindowText("red", "** FAIL: reader is slower than before!!")	
	else:
		DL.SetWindowText("green", "** PASS: reader is NOT slower than before.")	
	
for i in range(0, 4):
	if i == 0 or i == 1:
		card = "VISA MSD or other VISA card"
	if i == 2 or i == 3:
		card = "MasterCard MChip"
	
	if readercheck == 0:
		if (Result):
			if i == 1 or i == 3:
				cmd_840F()
			# cmd 02-01
			if (Result):
				DL.SetWindowText("black", "*** cmd 02-01, Please tap " + card + "..........")
				DL.SendIOCommand("IDG", "02 01 78 9F 02 06 00 00 00 00 10 00 9A 03 07 11 21 9F 21 03 10 15 20", 32000, 1) 
				Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")	
				if (Result):		
					if i == 1 or i == 3:
						timecheck()	
	if (Result):
		if i == 1 or i == 3:
			cmd_840F()
		# cmd 02-40		
		if (Result):
			DL.SetWindowText("black", "*** cmd 02-40, Please tap " + card + "..........")
			DL.SendIOCommand("IDG", "02 40 78 9F 02 06 00 00 00 00 10 00 9A 03 07 11 21 9F 21 03 10 15 20", 32000, 1) 
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23")
			if (Result):	
				if i == 1 or i == 3:
					timecheck()	