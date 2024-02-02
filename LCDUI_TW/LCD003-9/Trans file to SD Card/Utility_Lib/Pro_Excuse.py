#Pro_Excuse Py - excuse original txt format
import sys
import time
import System
class Pro_Excuse:
	ITEM=''
	def __init__(self, Item):
		self.ITEM  = Item
	#!0:fail.
	#!1:succeed.
	#!2:Stop
	def Run(self,res,DL):
		DL.SetWindowText('Black', self.ITEM)
		DL.RunTest(self.ITEM)
		if not res.strip():
			Result = DL.Check_RXErrorCode(0,"00", True)
		else:
			Result = DL.Check_RXResponse(res)
		return Result