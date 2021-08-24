#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Test cmd 25-03 1000 cycles
for i in range(1, 101):
	DL.SetWindowText("black",'***** Cycle: ' + str(i))
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 01", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 02", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 03", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 04", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 05", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 06", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 07", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 08", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 09", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")	
	if (Result):
		DL.SendIOCommand("IDG", "25 03 20 20 09 10", 3000, 1) 
		Result = DL.Check_RXResponse("25 00")		