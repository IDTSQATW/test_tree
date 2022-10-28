#Pro_GetDevice Py - use for get device type ?
import sys
import time
import System



class Pro_DecToHex:
	def dec2hex(self,num,cmd):
		if(num<10):
			return cmd+str(num)
		else:
			if(num==10):
				return cmd+"A"
			if(num==11):
				return cmd+"B"
			if(num==12):
				return cmd+"C"
			if(num==13):
				return cmd+"D"
			if(num==14):
				return cmd+"E"
			if(num==15):
				return cmd+"F"