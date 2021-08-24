#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

for i in range (1, 8):
	if i == 1:
		timeout = 9
	if i == 2:
		timeout = 9.25
	if i == 3:
		timeout = 9.5
	if i == 4:
		timeout = 9.75
	if i == 5:
		timeout = 10
	if i == 6:
		timeout = 10.25
	if i == 7:
		timeout = 10.5	
		
	# Poll On Demand
	if (Result):
		DL.SetWindowText("black", "*** Poll On Demand")
		DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
		Result = DL.Check_RXResponse("01 00 00 00")	

	DL.OpenDevice()	
	time.sleep(6)
	alldata = DL.GetResponse()	
	if (alldata != ""):
		DL.SetWindowText("red", alldata)
		DL.SetWindowText("red","** FAIL: should not return any data!!")

	# cmd 02-40		
	if (Result):
		DL.SetWindowText("black", "*** cmd 02-40, Please tap any bank card..........")
		DL.SendIOCommand("IDG", "02 40 20 9F 02 06 00 00 00 00 03 33", 32000, 1) 
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02")
		DL.SetWindowText("green", "==========================Waiting " + str(timeout) + " sec...................")
		time.sleep(timeout)
		
	# Auto Poll
	if (Result):
		DL.SetWindowText("black", "*** Auto Poll")
		DL.SendIOCommand("IDG", "01 01 00", 3000, 1) 
		Result = DL.Check_RXResponse("01 00 00 00")	

	DL.OpenDevice()	
	time.sleep(6)
	alldata = DL.GetResponse()	
	if (alldata != ""):
		DL.SetWindowText("red", alldata)
		DL.SetWindowText("red","** FAIL: should not return any data!!")