#Card113ContactlessMCDE3GX20010.py
#Load CAP, load CAP process
import sys
import time
import System
DL.pyresult = False

C2C03CAP = []
C2C03CAP.append(['Install CAP', '80 E6 02 00 13 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00 00 00 00 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 00 FA C4 82 08 90 01 00 1E DE CA FF ED 02 02 04 00 01 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 05 6D 63 70 6B 67 02 00 21 00 1E 00 21 00 13 00 29 00 A2 00 0E 06 E8 00 0A 00 58 00 00 01 77 05 E2 00 00 00 00 00 00 04 01 00 04 00 29 04 03 01 07 A0 00 00 00 62 01 01 03 01 07 A0 00 00 00 62 02 01 03 01 07 A0 00 00 00 62 01 02 00 01 07 A0 00 00 00 62 00 01 03 00 13 01 0F 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00 05 B6 06 00 0E 00 00 00 80 03 16 00 15 07 01 00 00 05 CA 07 06 E8 00 05 10 18 8C 00 18 18 10 10 90 0B 3D 03 10 46 38 3D 04 10 2F 38 3D 05 10 C4 38 3D 06 10 16 38 3D 07 10 E0 38 3D 08 10 E9 38 3D 10 06 10 3D 38 3D 10 07 07 38 3D 10 08 10 2C 38 3D 10 09 10 D0 38 3D 10 0A 10 B0 38 3D 10 0B 10 07 38 3D 10 0C 10 31 38 3D 10 0D 10 AB 38 3D 10 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 01 FA 0E 10 46 38 3D 10 0F 10 37 38 87 00 18 05 90 0B 3D 03 10 0D 38 3D 04 10 14 38 87 01 18 05 90 0B 3D 03 03 38 3D 04 10 37 38 87 02 18 06 90 0B 3D 03 10 9F 38 3D 04 10 36 38 3D 05 05 38 87 03 18 05 90 0B 3D 03 10 11 38 3D 04 10 46 38 87 04 18 03 88 05 18 10 3F 90 0B 3D 03 10 6F 38 3D 04 10 3D 38 3D 05 10 84 38 3D 06 10 0E 38 3D 07 10 32 38 3D 08 10 50 38 3D 10 06 10 41 38 3D 10 07 10 59 38 3D 10 08 10 2E 38 3D 10 09 10 53 38 3D 10 0A 10 59 38 3D 10 0B 10 53 38 3D 10 0C 10 2E 38 3D 10 0D 10 44 38 3D 10 0E 10 44 38 3D 10 0F 10 46 38 3D 10 10 10 30 38 3D 10 11 10 31 38 3D 10 12 10 A5 38 3D 10 13 10 2B 38 3D 10 14 10 BF 38 3D 10 15 10 0C 38 3D 10 16 10 28 38 3D 10 17 10 61 38 3D 10 18 10 0C 38 3D 10 19 10 4F 38 3D 10 1A 10 07 38 3D 10 1B 10 A0 38 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 02 FA 3D 10 1C 03 38 3D 10 1D 03 38 3D 10 1E 03 38 3D 10 1F 07 38 3D 10 20 10 10 38 3D 10 21 10 10 38 3D 10 22 10 87 38 3D 10 23 04 38 3D 10 24 04 38 3D 10 25 10 61 38 3D 10 26 10 0C 38 3D 10 27 10 4F 38 3D 10 28 10 07 38 3D 10 29 10 A0 38 3D 10 2A 03 38 3D 10 2B 03 38 3D 10 2C 03 38 3D 10 2D 07 38 3D 10 2E 10 30 38 3D 10 2F 10 60 38 3D 10 30 10 87 38 3D 10 31 04 38 3D 10 32 06 38 3D 10 33 10 61 38 3D 10 34 10 0A 38 3D 10 35 10 4F 38 3D 10 36 08 38 3D 10 37 10 B0 38 3D 10 38 10 12 38 3D 10 39 10 34 38 3D 10 3A 10 56 38 3D 10 3B 10 78 38 3D 10 3C 10 87 38 3D 10 3D 04 38 3D 10 3E 10 09 38 87 06 18 10 3D 90 0B 3D 03 10 6F 38 3D 04 10 3B 38 3D 05 10 84 38 3D 06 10 07 38 3D 07 10 A0 38 3D 08 03 38 3D 10 06 03 38 3D 10 07 03 38 3D 10 08 07 38 3D 10 09 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 03 FA 10 10 38 3D 10 0A 10 10 38 3D 10 0B 10 A5 38 3D 10 0C 10 30 38 3D 10 0D 10 87 38 3D 10 0E 04 38 3D 10 0F 04 38 3D 10 10 10 50 38 3D 10 11 10 0A 38 3D 10 12 10 4D 38 3D 10 13 10 61 38 3D 10 14 10 73 38 3D 10 15 10 74 38 3D 10 16 10 65 38 3D 10 17 10 72 38 3D 10 18 10 43 38 3D 10 19 10 61 38 3D 10 1A 10 72 38 3D 10 1B 10 64 38 3D 10 1C 10 5F 38 3D 10 1D 10 2D 38 3D 10 1E 10 06 38 3D 10 1F 10 65 38 3D 10 20 10 6E 38 3D 10 21 10 64 38 3D 10 22 10 65 38 3D 10 23 10 66 38 3D 10 24 10 72 38 3D 10 25 10 9F 38 3D 10 26 10 11 38 3D 10 27 04 38 3D 10 28 04 38 3D 10 29 10 9F 38 3D 10 2A 10 38 38 3D 10 2B 10 08 38 3D 10 2C 10 9F 38 3D 10 2D 05 38 3D 10 2E 10 06 38 3D 10 2F 10 9F 38 3D 10 30 10 33 38 3D 10 31 06 38 3D 10 32 10 9C 38 3D 10 33 04 38 3D 10 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 04 FA 34 10 BF 38 3D 10 35 10 0C 38 3D 10 36 10 06 38 3D 10 37 10 9F 38 3D 10 38 10 5D 38 3D 10 39 06 38 3D 10 3A 03 38 3D 10 3B 03 38 3D 10 3C 03 38 87 07 18 10 0C 90 0B 3D 03 10 77 38 3D 04 10 0A 38 3D 05 10 82 38 3D 06 05 38 3D 07 03 38 3D 08 03 38 3D 10 06 10 94 38 3D 10 07 07 38 3D 10 08 10 08 38 3D 10 09 04 38 3D 10 0A 04 38 3D 10 0B 03 38 87 08 18 07 90 0B 3D 03 10 08 38 3D 04 04 38 3D 05 04 38 3D 06 03 38 87 09 18 10 38 90 0B 3D 03 10 70 38 3D 04 10 36 38 3D 05 10 9F 38 3D 06 10 65 38 3D 07 05 38 3D 08 03 38 3D 10 06 10 0E 38 3D 10 07 10 9F 38 3D 10 08 10 66 38 3D 10 09 05 38 3D 10 0A 10 0E 38 3D 10 0B 10 70 38 3D 10 0C 10 9F 38 3D 10 0D 10 6B 38 3D 10 0E 10 13 38 3D 10 0F 10 54 38 3D 10 10 10 13 38 3D 10 11 10 33 38 3D 10 12 10 90 38 3D 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 05 FA 10 13 03 38 3D 10 14 03 38 3D 10 15 10 15 38 3D 10 16 10 13 38 3D 10 17 10 D4 38 3D 10 18 10 91 38 3D 10 19 10 21 38 3D 10 1A 04 38 3D 10 1B 10 90 38 3D 10 1C 03 38 3D 10 1D 10 99 38 3D 10 1E 03 38 3D 10 1F 03 38 3D 10 20 03 38 3D 10 21 10 0F 38 3D 10 22 10 9F 38 3D 10 23 10 67 38 3D 10 24 04 38 3D 10 25 06 38 3D 10 26 10 9F 38 3D 10 27 10 69 38 3D 10 28 10 0F 38 3D 10 29 10 9F 38 3D 10 2A 10 6A 38 3D 10 2B 07 38 3D 10 2C 10 9F 38 3D 10 2D 10 7E 38 3D 10 2E 04 38 3D 10 2F 10 9F 38 3D 10 30 05 38 3D 10 31 10 06 38 3D 10 32 10 5F 38 3D 10 33 10 2A 38 3D 10 34 05 38 3D 10 35 10 9F 38 3D 10 36 10 1A 38 3D 10 37 05 38 87 0A 18 10 0C 90 0B 3D 03 10 77 38 3D 04 10 0A 38 3D 05 10 9F 38 3D 06 10 61 38 3D 07 05 38 3D 08 10 A2 38 3D 10 06 10 C4 38 3D 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 06 FA 10 07 10 9F 38 3D 10 08 10 36 38 3D 10 09 05 38 3D 10 0A 06 38 3D 10 0B 10 F9 38 87 0B 18 08 03 8D 00 16 87 0C 18 06 10 40 03 8D 00 19 94 00 00 1A 87 0D 18 07 05 8D 00 17 87 0E 18 10 11 05 8D 00 17 87 0F 18 05 05 8D 00 17 87 10 18 05 05 8D 00 17 87 11 18 10 08 05 8D 00 17 87 12 18 10 08 05 8D 00 17 87 13 18 10 08 05 8D 00 17 87 14 18 10 08 05 8D 00 17 87 15 7A 05 30 8F 00 1B 3D 8C 00 1C 18 1D 04 41 18 1D 25 8B 00 1D 7A 02 21 19 8B 00 1E 2D 18 8B 00 1F 60 08 18 19 8C 00 20 7A 1A 03 25 75 00 53 00 02 FF 80 00 2B 00 00 00 0D 1A 04 25 75 00 19 00 02 FF A4 00 0D FF B2 00 14 18 19 8C 00 20 70 07 18 19 8C 00 21 70 30 1A 04 25 75 00 23 00 02 FF A8 00 0D 00 2A 00 19 19 8B 00 22 3B 18 19 8C 00 23 70 0C 19 8B 00 22 3B 18 19 8C 00 24 70 08 11 6D 00 8D 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 00 07 FA 00 25 7A 05 21 19 8B 00 1E 2D 1A 08 25 75 00 37 00 02 FF A0 00 23 00 32 00 0D AD 06 03 1A 03 AD 06 92 8D 00 26 3B 19 03 AD 06 92 8B 00 27 70 16 AD 07 03 1A 03 AD 07 92 8D 00 26 3B 19 03 AD 07 92 8B 00 27 7A 05 21 19 8B 00 1E 2D AD 08 03 1A 03 AD 08 92 8D 00 26 3B 19 03 AD 08 92 8B 00 27 7A 05 21 19 8B 00 1E 2D 1A 05 25 75 00 29 00 01 00 01 00 09 1A 06 25 75 00 1D 00 01 00 0C 00 09 AD 0A 03 1A 03 AD 0A 92 8D 00 26 3B 19 03 AD 0A 92 8B 00 27 7A 05 21 19 8B 00 1E 2D AD 0B 03 1A 03 AD 0B 92 8D 00 26 3B 19 03 AD 0B 92 8B 00 27 7A 08 00 0A 00 00 00 00 00 00 00 00 00 00 05 00 A2 00 28 02 00 02 00 02 00 02 01 02 00 02 02 02 00 02 04 02 00 02 05 02 00 02 15 02 00 02 0C 02 00 02 0D 02 00 02 0E 02 00 02 0F 02 00 02 10 02 00 02 11 02 00 02 13 02 00 02 01', '90 00'])


C2C03CAP.append(['Uploadding CAP', '80 E8 80 08 C4 14 02 00 02 03 02 00 02 12 02 00 02 06 02 00 02 07 02 00 02 08 02 00 02 09 02 00 02 0A 02 00 02 0B 06 81 01 00 06 80 08 0D 06 80 03 00 06 82 0D 00 01 82 0A 00 01 00 02 00 06 00 00 01 03 80 03 02 03 80 0A 01 03 80 03 03 06 00 06 3A 06 00 06 98 03 80 0A 06 06 00 06 7C 06 00 06 CC 06 80 07 01 06 80 10 02 03 80 0A 08 09 00 58 00 28 66 10 0F 14 10 04 FF 6E FF 61 42 17 FF 41 46 08 0E 08 09 08 08 09 09 09 09 9E 05 09 08 05 09 0E 05 09 26 05 09 0E 05 09 00 2C 05 FF FF FF FF FF 5E 0A 04 08 09 08 08 09 09 09 09 08 04 0A 07 05 07 26 07 16 06 06 06 08 07 1C 09 0D 09 07 0C 09 07 24 09 07 0C 09 01', '90 00'])


C2C03CAP.append(['Install CAP', '80 E6 0C 00 35 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 0F 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00 0F 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00 01 00 02 C9 00 00 00', '90 00'])


Result = True
RetOfStep = True
bRet = DL.OpenDevice()
if(Result == True):
# Start pass through
	DL.SetWindowText("green",'Start pass through' )
	DL.SendIOCommand("IDG",'2C 01 01',5000) 
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "2C 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Start Pass-through Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red", "Start Pass-through Fail")
			break
		time.sleep(0.02)

# Stop Antenna
if(Result == True):
	DL.SetWindowText("green",'Stop Antenna' )
	DL.SendIOCommand("IDG",'28 01 00',5000) 
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "28 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Stop Antenna Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red","Stop Antenna Fail")
			break
		time.sleep(0.02)


# Poll 4 T
if(Result == True):
	DL.SetWindowText("green",'Poll 4 T' )
	DL.SendIOCommand("IDG",'2C 02 FF FF',5000) 
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "2C 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Poll For Token Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red","Poll For Token Fail")
			break
		time.sleep(0.02)


#Select card
if(Result == True):
	DL.SetWindowText("green",'Select card' )
	DL.SendIOCommand("IDG",'2C 03 00 A4 04 00 08 A0 00 00 00 03 00 00 00 00',5000)
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "90 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Select card Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red", "Select card Fail")
			break
		time.sleep(0.02)

#Init-Update 255
if(Result == True):
	DL.SetWindowText("green",'Init-Update 255' )
	DL.SendIOCommand("IDG",'2C 03 80 50 00 00 08 D0 3E 90 B6 23 AC 53 86 00',5000)
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "90 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Init-Update Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red", "Init-Update Fail")
			break
		time.sleep(0.02)


#########################################CMAC#########################################
	Resp=Data.replace(" ","")
	DL.SetWindowText("green", 'Resp = ' +  Resp)
	auth_level = '00'
	DL.SetWindowText("green", 'auth_level = ' +  auth_level)
	static_key = '404142434445464748494A4B4C4D4E4F'
	DL.SetWindowText("green", 'static_key = ' +  static_key)
	host_random = 'D03E90B623AC5386'
	DL.SetWindowText("green", 'host_random  = ' +  host_random )
		
	key_diversification_data = Resp[28:48]
	DL.SetWindowText("green", 'key_diversification_data = ' +  key_diversification_data)
	Key_information = Resp[48:52]
	DL.SetWindowText("green", 'Key_information = ' +  Key_information)
	Sequence_counter = Resp[52:56]
	DL.SetWindowText("green", 'Sequence_counter = ' +  Sequence_counter)
	Card_challenge = Resp[56:68]
	DL.SetWindowText("green", 'Card_challenge = ' +  Card_challenge )
	Card_cryptogram = Resp[68:84]
	DL.SetWindowText("green", 'Card_cryptogram = ' + Card_cryptogram)
	
	SENC_P = '0182' + Sequence_counter + '000000000000000000000000'
	DL.SetWindowText("green", 'SENC_P = ' + SENC_P)
	CMAC_P = '0101' + Sequence_counter + '000000000000000000000000'
	DL.SetWindowText("green", 'CMAC_P  = ' + CMAC_P)
	CDEK_P = '0181' + Sequence_counter + '000000000000000000000000'
	DL.SetWindowText("green", 'CDEK_P  = ' + CDEK_P)

	SENC_SESSION = DL.EncryptionDecryption_TDESCBC(0,1,static_key,SENC_P,'0000000000000000')
	DL.SetWindowText("green", 'SENC_SESSION  = ' + SENC_SESSION)
	CMAC_SESSION = DL.EncryptionDecryption_TDESCBC(0,1,static_key,CMAC_P,'0000000000000000')
	DL.SetWindowText("green", 'CMAC_SESSION  = ' + CMAC_SESSION)
	SDEK_SESSION = DL.EncryptionDecryption_TDESCBC(0,1,static_key,CDEK_P,'0000000000000000')
	DL.SetWindowText("green", 'SDEK_SESSION  = ' + SDEK_SESSION)

	host_authenticate_cryptogram = Sequence_counter + Card_challenge +  host_random + '8000000000000000'
	DL.SetWindowText("green", 'host_authenticate_cryptogram  = ' + host_authenticate_cryptogram)
	host_authenticate_cryptogram_c = DL.EncryptionDecryption_TDESCBC(0,1,SENC_SESSION,host_authenticate_cryptogram,'0000000000000000')
	DL.SetWindowText("green", 'host_authenticate_cryptogram_c  = ' + host_authenticate_cryptogram_c)
	host_authenticate_cryptogram_MAC = host_authenticate_cryptogram_c[32:48]
	DL.SetWindowText("green", 'host_authenticate_cryptogram_MAC   = ' + host_authenticate_cryptogram_MAC )
	external_auth = '848200' + auth_level + '10' + host_authenticate_cryptogram_MAC
	DL.SetWindowText("green", 'external_auth   = ' + external_auth)
	pack_external_auth = external_auth + '800000'
	DL.SetWindowText("green", 'pack_external_auth   = ' + pack_external_auth)
	external_auth_mac = DL.ComputeCMacTDESValue(CMAC_SESSION, pack_external_auth)
	DL.SetWindowText("green", 'external_auth_mac   = ' + external_auth_mac)

#########################################CMACEnd#########################################

#ext-auth plain
if(Result == True):
	DL.SetWindowText("green",'ext-auth plain' )
	DL.SendIOCommand("IDG",'2C 03' + external_auth +external_auth_mac,5000)
	Data = DL.Get_RXResponse(0)
	while(DL.bIsStopRun == False):
		Result = DL.Check_StringAB(Data, "90 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Ext-auth plain Pass")
			break
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red", "Ext-auth plain Fail")
			break
		time.sleep(0.02)


#######################################DeleteAID###########################################
#Get all AID
	DL.SetWindowText("green",'Get App' )
	DL.SendIOCommand("IDG",'2C 03 80 F2 20 00 02 4F 00 00',5000)
	Data = DL.Get_RXResponse(0)
	Data= Data.replace(" ","")
	while(DL.bIsStopRun == False):
		if(Data != ""):
			DL.SetWindowText("green",Data)
			break
		else:time.sleep(0.1)

	strResponse = Data[24:len(Data)]
	DL.setText("green",strResponse)
	LAID = strResponse[4:6]
	i=0
	AIDpara=[]
	DeleteAID=[]
	while (LAID!="90"):
		strResponse = strResponse[4:len(strResponse)]
		if(strResponse==""):break
		LAID = strResponse[0:2] # AID length Hex str
		LAID = int(str(LAID),16) # AID length int
		Lend = LAID*2+2  # AID length int + 
		AID = strResponse[0:Lend]
		para = hex(LAID+2)
		para = para[2:len(para)]
		if(LAID+2 < 16):AIDpara.append("0"+para)
		else: AIDpara.append(para)
		DeleteAID.append(str(AID))
		strResponse = strResponse[Lend:len(strResponse)]
		i=i+1
		LAID = strResponse[4:6]
	i=i-1

#Delete all AID
	while(i>=0):
		DL.setText("Black","Delete AID:"+ str(DeleteAID[i]))
		DL.SendIOCommand("IDG",'2C 03 80 E4 00 80'+AIDpara[i]+'4F'+DeleteAID[i]+'00',5000)
		Data = DL.Get_RXResponse(0)
		DL.SetWindowText("green",Data)
		i=i-1
#######################################WriteData###########################################
	i=0
	while (i< 11):
		DL.setText("BLACK",C2C03CAP[i][0])
		DL.SendIOCommand("IDG",'2C 03' + C2C03CAP[i][1],5000)
		Data = DL.Get_RXResponse(0)
		Result = DL.Check_StringAB(Data, "90 00")
		if(Result):
			DL.SetWindowText("green", Data)
			DL.SetWindowText("green", "Load card data Pass")
		else:
			DL.SetWindowText("red", Data)
			DL.SetWindowText("red", "Load card data Fail")
			break
		i=i+1
	time.sleep(1)


#Stop Pass Through
DL.SetWindowText("green",'Stop Pass Through' )
DL.SendIOCommand("IDG",'2C 01 00',5000)
Data = DL.Get_RXResponse(0)
while(DL.bIsStopRun == False):
	Result = DL.Check_StringAB(Data, "2C 00")
	if(Result):
		DL.SetWindowText("green", Data)
		DL.SetWindowText("green", "Stop Pass-Through Pass")
		break
	else:
		DL.SetWindowText("red", Data)
		DL.SetWindowText("red", "Stop Pass-Through Fail")
		break
time.sleep(0.01)

if(Result):
	DL.pyresult = True
else:
	DL.pyresult = False

