#!/usr/bin/env python
import sys
import time
Result=True

if (Result):
	DL.SendCommand('Delete All Entries from EMV Transaction Log (84-01)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 01 00 00 00 36 F8 ")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 00 00 00 01 58 8C 67 ")

if (Result):
	DL.SendCommand('Get EMV Transaction Log (84-02)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 02 0A 00 04 00 08 00 03 6A 7C ")

if (Result):
	DL.SendCommand('Activate transaction',10000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 01 00")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 01 00 00 01 58")

if (Result):
	DL.SendCommand('Activate transaction',10000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 01 00")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 03 00 00 01 58")

if (Result):
	DL.SendCommand('Activate transaction',10000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 01 00")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 05 00 00 01 58")

if (Result):
	DL.SendCommand('Activate transaction',10000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 02 01 00")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 07 00 00 01 58")

if (Result):
	DL.SendCommand('Get EMV Transaction Log (84-02)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 02 00 01 64 00 00 00 01 00 00 00 06 00 00 01 58 01 00 02 58 00 02 00 01 02 FF C0 01 40 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 41 03 02 08 54 65 72 6D 69 6E 61 6C 05 FC 50 A0 00 00 05 00 00 00 00 00 05 F8 70 A4 98 00 12 02 10 A0 00 00 00 00 00 DA C0 00 00 00 00 00 00 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 28 A5")

if (Result):
	DL.SendCommand('Get EMV Transaction Log Status (84-00)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 00 00 00 0C 00 00 00 00 00 00 00 06 00 00 01 58")

if (Result):
	DL.SendCommand('Get EMV Transaction Log (84-02)',3000)
	Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 84 02 00 08 1C 00 00 00 06 00 00 00 00 00 00 01 58 ")
