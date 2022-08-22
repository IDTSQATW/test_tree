#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'
rx = 0

#Objective: to verify AES DUKPT Management, AES-128 Working Key encryption/ decryption function

# # CL test
# if (Result):
	# RetOfStep = DL.SendCommand('02-40 (enable CL only)')
	# if (RetOfStep):
		# alldata = DL.Get_RXResponse(3)
		# ksn = DL.GetTLV(alldata,"DFEE12")	
		# TagFF8105 = DL.GetTLV(alldata,"FF8105")
		# # 57
		# # DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
		# mask57 = DL.GetTLV(TagFF8105,"57", 0)
		# enc57 = DL.GetTLV(TagFF8105,"57", 1)
		# DL.SetWindowText("blue", "Tag 57 Decryption data:")
		# dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)	
		# # 5A
		# # DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
		# mask5A = DL.GetTLV(TagFF8105,"5A", 0)
		# enc5A = DL.GetTLV(TagFF8105,"5A", 1)
		# DL.SetWindowText("blue", "Tag 5A Decryption data:")
		# dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)	

# # MSR test
# if (Result):
	# RetOfStep = DL.SendCommand('02-40 (enable MSR only)')
	# rx = 1 # for VP3350
	# if (RetOfStep):
		# sResult=DL.Get_RXResponse(rx)
		# if sResult!=None and sResult!="":
			# sResult=sResult.replace(" ","")
			# CardData=DL.GetTLV(sResult,"DFEE23")
			# if CardData!=None and CardData!='':
				# objectMSR = DL.ParseCardData(CardData, strKey)
				# if objectMSR!=None:
					# DL.SetWindowText("blue", "Track 1:")
					# Track1_CardData = DL.Get_TrackN_CardData(1)
					# DL.SetWindowText("blue", "Track 2:")
					# Track2_CardData = DL.Get_TrackN_CardData(2)
					# DL.SetWindowText("blue", "Track 3:")
					# Track3_CardData = DL.Get_TrackN_CardData(3)
					# DL.SetWindowText("blue", "Track 1_Enc:")
					# TRK1 = DL.Get_EncryptTrackN_CardData(1)
					# DL.SetWindowText("blue", "Track 2_Enc:")
					# TRK2 = DL.Get_EncryptTrackN_CardData(2)
					# DL.SetWindowText("blue", "Track 3_Enc:")
					# TRK3 = DL.Get_EncryptTrackN_CardData(3)
					# DL.SetWindowText("blue", "KSN:")
					# KSN=DL.Get_KSN_CardData()
					# DL.SetWindowText("blue", "SN: (HEX/ ASCII)")
					# DL.SetWindowText("green", DL.getASCIIArray(DL.Get_DeviceRSN_CardData()))
					# if len(TRK1)> 0:
						# DL.SetWindowText("blue", "Track 1 Decryption data:")
						# TRK1DecryptData = DL.AES_DUPKT_MSRData_Decipher(KSN, strKey, TRK1)
					# if len(TRK2)> 0:
						# DL.SetWindowText("blue", "Track 2 Decryption data:")
						# TRK2DecryptData = DL.AES_DUPKT_MSRData_Decipher(KSN, strKey, TRK2)
					# if len(TRK3)> 0:
						# DL.SetWindowText("blue", "Track 3 Decryption data:")
						# TRK3DecryptData = DL.AES_DUPKT_MSRData_Decipher(KSN, strKey, TRK3)


					# TR1maskdata = "%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
					# TR2maskdata = ";4547********0000=1102***************?*"
					# TR3maskdata = ";**4547********0000=***********************************************************************************?*"
					# TR1plaintextdata = "2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F2E"
					# TR2plaintextdata = "3B343534373537303030313037303030303D313130323130313030303030333036303030303F38"
					# TR3plaintextdata = "3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F35"
									
					# if DL.Check_StringAB(TR1maskdata, Track1_CardData) == False:
						# DL.SetWindowText("red", "TR1 maskdata: FAIL")

					# if DL.Check_StringAB(TR2maskdata, Track2_CardData) == False:
						# DL.SetWindowText("red", "TR2 maskdata: FAIL")
						
					# if DL.Check_StringAB(TR3maskdata, Track3_CardData) == False:
						# DL.SetWindowText("red", "TR3 maskdata: FAIL")	
			
					# if len(TRK1)> 0:
						# if  DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData) == False:
							# DL.SetWindowText("red", "TR1 plaintextdata: FAIL")
					
					# if len(TRK2)> 0:
						# if  DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData) == False:
							# DL.SetWindowText("red", "TR2 plaintextdata: FAIL")
					
					# if len(TRK3)> 0:					
						# if  DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData) == False:
							# DL.SetWindowText("red", "TR3 plaintextdata: FAIL")		
		
# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Please load AES key first.....")		
		
# CT test
if (Result):
	RetOfStep = DL.SendCommand('60-10')		
	rx6010 = 9 #for VP3350
	if (RetOfStep):
		alldata = DL.Get_RXResponse(rx6010)			
		CTresultcode = DL.GetTLV(alldata,"DFEE25")
		ksn = DL.GetTLV(alldata,"DFEE12")	
		# 57
		DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
		mask57 = DL.GetTLV(alldata,"57", 0)
		enc57 = DL.GetTLV(alldata,"57", 1)
		DL.SetWindowText("blue", "Tag 57 Decryption data:")
		dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
		if DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC') == False:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
		if DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89') == False:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		# 5A
		DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
		mask5A = DL.GetTLV(alldata,"5A", 0)
		enc5A = DL.GetTLV(alldata,"5A", 1)
		DL.SetWindowText("blue", "Tag 5A Decryption data:")
		dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
		if DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10') == False:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
		if DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10') == False:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
		if  CTresultcode == "0010":
			RetOfStep = DL.SendCommand('60-11')
			rx6011 = 4 #for VP3350
			if (RetOfStep):
				alldata = DL.Get_RXResponse(rx6011)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")	
				ksn = DL.GetTLV(alldata,"DFEE12")
				# 57
				DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				DL.SetWindowText("blue", "Tag 57 Decryption data:")
				dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
				if DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC') == False:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				if DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89') == False:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
				# 5A
				DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				DL.SetWindowText("blue", "Tag 5A Decryption data:")
				dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)
				if DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10') == False:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
				if DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10') == False:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
				if  CTresultcode == "0004":
					RetOfStep = DL.SendCommand('60-12')
					rx6012 = 2 #for VP3350
					if (RetOfStep):
						alldata = DL.Get_RXResponse(rx6012)
						CTresultcode = DL.GetTLV(alldata,"DFEE25")	