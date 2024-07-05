#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

DL.SendIOCommand("IDG","60 10 01 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40",10000,2)
str123 = DL.Get_RXResponse(1).replace(" ","")
str456 = DL.Get_RXResponse(2).replace(" ","")
if(str456!=""):str1 = str123[30:-4]+str456[28:-4]
else:str1 = str123[30:-4]
DL.setText("GREEN",str1)
strDFEF17 = DL.GetTLV_Embedded(str1, "DFEF17",0)
strDDFEF17 = DL.DecryptTransAmorData(strDFEF17)
strDFEF18 = DL.GetTLV_Embedded(str1, "DFEF18",0)
strDDFEF18 = DL.DecryptTransAmorData(strDFEF18)
str56 = DL.GetTLV_Embedded(str1, "56",1)
strD56 = DL.DecryptTransAmorData(str56)
str57 = DL.GetTLV_Embedded(str1, "57",1)
strD57 = DL.DecryptTransAmorData(str57)
str5A = DL.GetTLV_Embedded(str1, "5A",1)
strD5A = DL.DecryptTransAmorData(str5A)
str9F6B = DL.GetTLV_Embedded(str1, "9F6B",1)
strD9F6B = DL.DecryptTransAmorData(str9F6B)
strDFEC35 = DL.GetTLV_Embedded(str1, "DFEC35",1)
strDFEC35 = DL.DecryptTransAmorData(strDFEC35)
strDFEC36 = DL.GetTLV_Embedded(str1, "DFEC36",1)
strDFEC36 = DL.DecryptTransAmorData(strDFEC36)
strDFEC45 = DL.GetTLV_Embedded(str1, "DFEC45",0)
strDFEC45 = DL.DecryptTransAmorData(strDFEC45)
strDFEF4D = DL.GetTLV_Embedded(str123, "DFEF4D",0)
strDFEF4D = DL.DecryptTransAmorData(strDFEF4D)
##################################################

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END