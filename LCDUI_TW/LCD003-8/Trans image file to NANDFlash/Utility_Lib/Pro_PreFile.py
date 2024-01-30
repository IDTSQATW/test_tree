#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Import #######################################
import time
import System
import re
import Utility_Lib.Pro_Excuse
import Utility_Lib.Pro_GetDevice
import Utility_Lib.Pro_PKI
import Utility_Lib.Pro_KeyInjection
import Utility_Lib.Pro_GetDRS
import Utility_Lib.Pro_SendCmd
import Utility_Lib.Pro_MSR
import Utility_Lib.Pro_MSRData 
#import Utility_Lib.Pro_DecToHex
import Utility_Lib.Pro_ISOCardData
import Trans_Lib.Tran_Res
import Trans_Lib.Tran_ResAuto
import Trans_Lib.Tra_Type_1

from  Utility_Lib.Pro_Excuse import *
from  Utility_Lib.Pro_GetDevice import *
from  Utility_Lib.Pro_PKI import *
from  Utility_Lib.Pro_KeyInjection import *
from  Utility_Lib.Pro_GetDRS import *
from  Utility_Lib.Pro_SendCmd import *
from  Utility_Lib.Pro_MSR import *
from  Utility_Lib.Pro_MSRData import *
#from  Utility_Lib.Pro_DecToHex import *
from  Utility_Lib.Pro_ISOCardData import *
from  Trans_Lib.Tran_Res import *
from  Trans_Lib.Tran_ResAuto import *
from  Trans_Lib.Tra_Type_1 import *

class Pro_Files:
	def GetFiles_libFatherPath(self,DL):
		Pathfather = str(__file__).replace(r'\Utility_Lib\Pro_PreFile.py','') + r'\Files_Lib'
		DL.setText("GREEN",Pathfather)
		return Pathfather

	def CkFileExist(self,FilePath,DL):
		try:
			f =open(FilePath)
			f.close()
		except IOError:
			return False
		return True