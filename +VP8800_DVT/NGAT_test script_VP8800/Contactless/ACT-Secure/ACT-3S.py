#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

if(Result):
	ans=DL.ShowMessageBox('message','After clicking pass, Verfiy LCD shows cashback and amount is 27, \nThen tap qVSDC card.',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with enable transaction type')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9C 01 01") and Result

if(Result):
	ans=DL.ShowMessageBox('message','After clicking pass, Verfiy LCD not show Contactless logo \nThen tap qVSDC card.',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with disable Default CL Logo')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9F 02 06 00 00 00 00 27 00") and Result

if(Result):
	ans=DL.ShowMessageBox('MESSAGE','Tap qVSDC card after clicking pass, \nVerify reader not beep',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with disable default buzzer')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9F 02 06 00 00 00 00 27 00") and Result

if (Result):
	ans=DL.ShowMessageBox('message','Tap qVSDC card after clicking pass, \nVerfiy LED not light',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with disable LED UI')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9F 02 06 00 00 00 00 27 00") and Result

if (Result):
	ans=DL.ShowMessageBox('MESSAGE','Tap qVSDC card after clicking pass, \nVerfiy LCD not show any message',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with disable LCD message')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9F 02 06 00 00 00 00 27 00") and Result

if (Result):
	RetOfStep = DL.SendCommand('Online approve')
	if (RetOfStep):
		Result = DL.Check_RXResponse("03 03 00") and Result

if (Result):
	ans=DL.ShowMessageBox('MESSAGE','Tap qVSDC card after clicking pass',0)
	if(ans==1):
		Result=True
	else:
		Result=False

if (Result):
	RetOfStep = DL.SendCommand('02-05 with default setting')
	if (RetOfStep):
		Result = DL.Check_RXResponse("9F 02 06 00 00 00 00 27 00") and Result

if (Result):
	RetOfStep = DL.SendCommand('Online Decline')
	if (RetOfStep):
		Result = DL.Check_RXResponse("03 03 00") and Result
