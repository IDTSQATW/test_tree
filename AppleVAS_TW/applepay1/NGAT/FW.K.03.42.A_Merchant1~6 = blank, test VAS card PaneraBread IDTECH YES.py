#!/usr/bin/env pythonF
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

# Set Merchant 1~6 = Blank
if (Result):
	for i in range (1, 7):
		DL.SetWindowText("black", "*** Set Merchant " + str(i))
		cmd = '0411' + '0' + str(i) + '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
		DL.SendIOCommand("IDG", cmd, 32000, 1)	
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 04 00")
	
# cmd 02-01
if (Result):
	terminal = ['9F 26 04 00 00 00 02', '9F 26 04 00 00 00 00', '9F 26 04 00 00 00 01', '9F 26 04 00 00 00 03', 'DF EE 01 01 00']
	terminalname = ['VAS Only', 'VAS OR PAY', 'VAS AND PAY', 'PAY Only', ' VAS URL Only Protocol']
	
	for i in range (0, 5): #Panera Bread card
		DL.SetWindowText("black", "*** cmd 02-01 w/ ApplePay " + terminalname[i] + " >>>>> Please tap ApplePay w/ Panera Bread card...............")
		# TX
		if i <= 3:
			cmd = '0201' + '30 9F 02 06 00 00 00 00 00 01 9C 01 00 FF EE 06 19 9F 22 02 01 00' + terminal[i] + '9F 2B 05 01 00 00 00 00 DF EE 01 01 01'
			DL.SendIOCommand("IDG", cmd, 32000, 1) 
		if i == 4:
			cmd = '0201' + '30 9F 02 06 00 00 00 00 00 01 9C 01 00 FF EE 06 19 9F 22 02 01 00' + terminal[0] + '9F 2B 05 01 00 00 00 00' + terminal[4]
			DL.SendIOCommand("IDG", cmd, 32000, 1) 	
		# RX
		if i != 3:
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 57 ** 00 00 00 00 FF EE 06 ** 9A 03 ** 9F 21 03 ** DF EE 02 04 80 ** 9F 39 01 07 FF EE 01 ** DF EE 30 01 00 ** DF EE 26 02 21 00")
		if i == 3:
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 0A ** 6A 82")
		if Result != True:
			DL.SetWindowText("red", "FAIL -- RX data was incorrect")
			
	for i in range (0, 5): #IDTECH ENCRYPTION YES card
		DL.SetWindowText("black", "*** cmd 02-01 w/ ApplePay " + terminalname[i] + " >>>>> Please tap ApplePay w/ IDTECH ENCRYPTION YES card...............")
		# TX
		if i <= 3:
			cmd = '0201' + '30 9F 02 06 00 00 00 00 00 01 9C 01 00 FF EE 06 19 9F 22 02 01 00' + terminal[i] + '9F 2B 05 01 00 00 00 00 DF EE 01 01 01'
			DL.SendIOCommand("IDG", cmd, 32000, 1) 
		if i == 4:
			cmd = '0201' + '30 9F 02 06 00 00 00 00 00 01 9C 01 00 FF EE 06 19 9F 22 02 01 00' + terminal[0] + '9F 2B 05 01 00 00 00 00' + terminal[4]
			DL.SendIOCommand("IDG", cmd, 32000, 1) 	
		# RX
		if i != 3:
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 57 ** 00 00 00 00 FF EE 06 ** 9A 03 ** 9F 21 03 ** DF EE 02 04 80 ** 9F 39 01 07 FF EE 01 ** DF EE 30 01 00 ** DF EE 26 02 21 00")
		if i == 3:
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 0A ** 6A 82")
		if Result != True:
			DL.SetWindowText("red", "FAIL -- RX data was incorrect")