#Pro_SendCmd Py - Command Exchange
import sys
import time
import System
from System import Array, String

class Pro_Command:
	
	# Run Command Test With [Command Table]
	# Command Table:
	# cmdTBL = [
	#	[Description,	cmd,		[Set Test Value , Default Value]]
	#	['DFEE2D' ,	    '01',		['00',		'00']],
	# 	['9C',		    '01',		['00',		'00']],

	def __init__(self,cmd,option, DL):
		self.cmd = cmd
		self.listOption = option	

	def RunWithOption(self,DL):
		DL.SendIOCommand("IDG",C0400,30000)
		if(False == DL.Check_RXResponse(0,"04 00",True)):
			DL.fails = DL.fails + 1
            
	def RunAllOption(self,DL):
		DL.SendIOCommand("IDG",C0400,30000)
		if(False == DL.Check_RXResponse(0,"04 00",True)):
			DL.fails = DL.fails + 1

