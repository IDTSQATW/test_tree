#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

if (Result):
	RetOfStep = DL.SendCommand('Create folder slide')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("83 25")


cmdlist1 = []
cmdlist1 = DL.ConvertBitMapToHexString('slide1.png','D:\\temp\\PISCES\\Slide\\slide1.png')
for i in range(len(cmdlist1)):
   cmd = '8324' + cmdlist1[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)

cmdlist2 = []
cmdlist2 = DL.ConvertBitMapToHexString('slide2.png','D:\\temp\\PISCES\Slide\\slide2.png')
for i in range(len(cmdlist2)):
   cmd = '8324' + cmdlist2[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist3 = []
cmdlist3 = DL.ConvertBitMapToHexString('slide3.png','D:\\temp\\PISCES\\Slide\\slide3.png')
for i in range(len(cmdlist3)):
   cmd = '8324' + cmdlist3[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)   

cmdlist4 = []
cmdlist4 = DL.ConvertBitMapToHexString('slide1.bmp','D:\\temp\\PISCES\\Slide\\slide1.bmp')
for i in range(len(cmdlist4)):
   cmd = '8324' + cmdlist4[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist5 = []
cmdlist5 = DL.ConvertBitMapToHexString('slide2.bmp','D:\\temp\\PISCES\\Slide\\slide2.bmp')
for i in range(len(cmdlist5)):
   cmd = '8324' + cmdlist5[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)   

cmdlist6 = []
cmdlist6 = DL.ConvertBitMapToHexString('slide3.bmp','D:\\temp\\PISCES\\Slide\\slide3.bmp')
for i in range(len(cmdlist6)):
   cmd = '8324' + cmdlist6[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)   
   
if (Result):
	RetOfStep = DL.SendCommand('List all folders and files')
	#time.sleep(1)