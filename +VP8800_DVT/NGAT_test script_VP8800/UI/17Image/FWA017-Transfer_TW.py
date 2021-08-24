#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True

if (Result):
	RetOfStep = DL.SendCommand('Create folder bitmap')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("83 25")


cmdlist1 = []
cmdlist1 = DL.ConvertBitMapToHexString('100x100.png','D:\\temp\\PISCES\\Images\\100x100.png')
for i in range(len(cmdlist1)):
   cmd = '8324' + cmdlist1[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)

cmdlist2 = []
cmdlist2 = DL.ConvertBitMapToHexString('100x100-2.bmp','D:\\temp\\PISCES\\Images\\100x100-2.bmp')
for i in range(len(cmdlist2)):
   cmd = '8324' + cmdlist2[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist3 = []
cmdlist3 = DL.ConvertBitMapToHexString('100x100-4.bmp','D:\\temp\\PISCES\\Images\\100x100-4.bmp')
for i in range(len(cmdlist3)):
   cmd = '8324' + cmdlist3[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist4 = []
cmdlist4 = DL.ConvertBitMapToHexString('100x100-8.bmp','D:\\temp\\PISCES\\Images\\100x100-8.bmp')
for i in range(len(cmdlist4)):
   cmd = '8324' + cmdlist4[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)

cmdlist5 = []
cmdlist5 = DL.ConvertBitMapToHexString('100x100-24.bmp','D:\\temp\\PISCES\\Images\\100x100-24.bmp')
for i in range(len(cmdlist5)):
   cmd = '8324' + cmdlist5[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist6 = []
cmdlist6 = DL.ConvertBitMapToHexString('bitmap/100x100.png','D:\\temp\\PISCES\\Images\\100x100.png')
for i in range(len(cmdlist6)):
   cmd = '8324' + cmdlist6[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist7 = []
cmdlist7 = DL.ConvertBitMapToHexString('500x500-24.bmp','D:\\temp\\PISCES\\Images\\500x500-24.bmp')
for i in range(len(cmdlist7)):
   cmd = '8324' + cmdlist7[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)
   
cmdlist8 = []
cmdlist8 = DL.ConvertBitMapToHexString('500x500.png','D:\\temp\\PISCES\\Images\\500x500.png')
for i in range(len(cmdlist8)):
   cmd = '8324' + cmdlist8[i]
   DL.SendIOCommand('VIV', cmd, 3000)
   Result = DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 83 24 00 00 00 DA 27")
   time.sleep(1)   


if (Result):
	RetOfStep = DL.SendCommand('List all folders and files')
	#time.sleep(1)