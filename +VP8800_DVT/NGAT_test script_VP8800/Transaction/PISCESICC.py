#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import clr

DataKey="0123456789abcdeffedcba9876543210"
PinKey="0123456789abcdeffedcba9876543210"
#EncPAN_5A=''
#strPAN_5A=''
#EncStatInfo_DFEE26=''
strDecryptPIN=''
#EncOlPIN_99=''
Pan=''
EncryptMode=0

Result = DL.SendCommand("02-05(ICC)")
sResult = DL.Get_RXResponse(0)
#sResult ='56 69 56 4F 70 61 79 56 33 00 02 05 00 01 A1 00 00 00 82 02 5C 00 9F 36 02 00 01 9F 07 02 FF C0 9F 26 08 78 5A D2 22 B6 63 68 B8 9F 27 01 40 8E 0C 00 00 00 00 00 00 00 00 5F 03 00 00 81 04 00 00 00 63 9F 34 03 5F 03 02 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 0D 05 00 00 00 00 00 9F 0E 05 00 00 00 00 00 9F 0F 05 00 00 00 00 00 9F 10 07 06 01 1A 03 90 00 00 9F 24 00 9F 33 03 60 F8 C8 9F 35 01 22 95 05 42 80 00 00 00 9F 37 04 8A F3 E8 6D 9F 01 06 56 49 53 41 30 30 9F 02 06 00 00 00 00 00 99 9F 03 06 00 00 00 00 00 00 5F 25 03 95 07 01 5F 24 03 20 12 31 5A 08 47 61 73 90 01 01 00 10 5F 34 01 01 5F 28 02 08 40 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1A 02 08 40 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E 57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89 5F 2A 02 08 40 9A 03 20 03 08 9F 21 03 06 07 05 9C 01 00 9F 06 07 A0 00 00 00 03 10 10 9F 09 02 00 96 5F 20 0F 46 55 4C 4C 20 46 55 4E 43 54 49 4F 4E 41 4C 9F 20 00 5F 2D 08 65 73 65 6E 66 72 64 65 50 0A 56 49 53 41 43 52 45 44 49 54 4F 07 A0 00 00 00 03 10 10 84 07 A0 00 00 00 03 10 10 9F 39 01 05 9F 4D 00 9F 13 00 9B 02 C8 00 99 00 DF EE 23 00 DF EE 0B 00 FF EE 01 05 DF EE 30 01 01 DF EE 26 01 00 D8 70'

if sResult!=None and sResult!="":
    sResult=sResult.replace(" ","")
    if sResult[24:26] != '0A':
        if sResult[24:26] != '08':
            if sResult[24:26] == '00':
                sResultTLV=sResult[36:len(sResult)-4]
            else:
                sResultTLV=sResult[30:len(sResult)-4]
            DL.SetWindowText("BLUE", sResult)
            DL.SetWindowText("GREEN", sResultTLV)
            ClrMskPAN_5A =  DL.GetTLV(sResultTLV,"5A",0,False)
            EncPAN_5A = DL.GetTLV(sResultTLV,"5A",1,False)
            EncStatInfo_DFEE26 = DL.GetTLV(sResultTLV, "DFEE26",0, False)
            TK2EqData_57 = DL.GetTLV(sResultTLV, "57",0, False)
            TK2Discret_9F20= DL.GetTLV(sResultTLV, "9F20",0, False)
            DataKSN_DFEE12 = DL.GetTLV(sResultTLV, "DFEE12", 0, False)
            EncOlPIN_99=DL.GetTLV(sResultTLV,"99",0,True)

            DL.SetWindowText("BLUE", "Encryption Status Information(DFEE26):"+str(EncStatInfo_DFEE26))
            if len(EncStatInfo_DFEE26) != 0:
                if (int(EncStatInfo_DFEE26[0:2], 16) & 0x40) == 0x00:
                    EncryptMode = 0
                else:
                    if (int(EncStatInfo_DFEE26[0:2], 16) & 0x02) == 0x02:
                        EncryptMode = 2
                    elif (int(EncStatInfo_DFEE26[0:2], 16) & 0x02) == 0x00:
                        EncryptMode = 1
            else:
                DL.SetWindowText("RED", "No Encryption Status Information(DFEE26), Encryption Mode set to default.")
            #else:
                #EncryptMode = 0

            if len(DataKSN_DFEE12) == 24:
                if EncryptMode == 1:
                    EncryptMode = 4
                elif EncryptMode == 2:
                    EncryptMode = 3

            DL.SetWindowText("BLUE", "Encryption Mode:"+str(EncryptMode))

            if EncryptMode != 0:
                strPAN_5A= DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncPAN_5A)
                strTK2EqData_57=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, TK2EqData_57)
                strTK2Discret_9F20=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, TK2Discret_9F20)
                #DL.SetWindowText("BLUE", "PAN Tag:"+strPAN_5A[0:2])
                #DL.SetWindowText("BLUE", "PAN LEN:"+strPAN_5A[2:4])
            else:
                strPAN_5A = ClrMskPAN_5A
                strTK2EqData_57 = TK2EqData_57
                strTK2Discret_9F20 = TK2Discret_9F20
            
            DL.SetWindowText("BLUE", "Primary Account Number(5A) Decrypted:"+strPAN_5A)
            DL.SetWindowText("BLUE", "Track 2 Equivalent Data(57) Decrypted:"+strTK2EqData_57)
            DL.SetWindowText("BLUE", "Track 2 Discretionary Data(9F20) Decrypted:"+strTK2Discret_9F20)
            
            if len(strPAN_5A) != 0 :
                if EncryptMode !=0:
                    Pan = strPAN_5A[4:(int(strPAN_5A[2:4],16)*2+4)]
                else:
                    Pan = strPAN_5A
            DL.SetWindowText("GREEN", "PAN:"+ Pan)
            DL.SetWindowText("GREEN", "len(EncOlPIN_99):"+ str(len(EncOlPIN_99)))
            
            if len(EncOlPIN_99)==36:
                strDecryptPIN=DL.Format4_PIN_Block_Decipher(EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
                #strDecryptPIN=DL.FormatX_PIN_Block_Decipher(2,1,EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[16:len(EncOlPIN_99)])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:16])
            elif len(EncOlPIN_99)==40:
                strDecryptPIN=DL.FormatX_PIN_Block_Decipher(2,1,EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[16:len(EncOlPIN_99)])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:16])
            elif len(EncOlPIN_99) == 52:
                strDecryptPIN = DL.FormatX_PIN_Block_Decipher(1,2,EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[32:len(EncOlPIN_99)])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:32])
            elif len(EncOlPIN_99) == 56:
                strDecryptPIN = DL.FormatX_PIN_Block_Decipher(1,2,EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])  
                DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[32:len(EncOlPIN_99)])
                DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:32])
            	  
            DL.SetWindowText("RED", "Encipherd Online PIN(99):"+EncOlPIN_99)
            
            DL.SetWindowText("BLUE", "Encipherd Online PIN(99) Decrypted:"+strDecryptPIN)
            
            DL.SetWindowText("RED", sResult[24:26])
            if sResult[24:26] == '30':
                DL.SetWindowText("RED", "Request Online Authorization")
                
                Result = DL.SendCommand("02-06(Approved)")
                sResult = DL.Get_RXResponse(0)
                if sResult!=None and sResult!="":
                    sResult=sResult.replace(" ","")
                    if sResult[24:26] == '00':
                        sResultTLV=sResult[36:len(sResult)-4]
                    else:
                        sResultTLV=sResult[30:len(sResult)-4]
                    DL.SetWindowText("BLUE", sResult)
                    DL.SetWindowText("GREEN", sResultTLV)
                    ClrMskPAN_5A =  DL.GetTLV(sResultTLV,"5A",0,False)
                    EncPAN_5A = DL.GetTLV(sResultTLV,"5A",1,False)
                    EncStatInfo_DFEE26 = DL.GetTLV(sResultTLV, "DFEE26",0, False)
                    TK2EqData_57 = DL.GetTLV(sResultTLV, "57",0, False)
                    TK2Discret_9F20= DL.GetTLV(sResultTLV, "9F20",0, False)
                    DataKSN_DFEE12 = DL.GetTLV(sResultTLV, "DFEE12", 0, False)
                    EncOlPIN_99=DL.GetTLV(sResultTLV,"99",0,True)

                    DL.SetWindowText("BLUE", "Encryption Status Information(DFEE26):"+str(EncStatInfo_DFEE26))
                    if len(EncStatInfo_DFEE26) != 0:
                        if (int(EncStatInfo_DFEE26[0:2], 16) & 0x40) == 0x00:
                            EncryptMode = 0
                        else:
                            if (int(EncStatInfo_DFEE26[0:2], 16) & 0x02) == 0x02:
                                EncryptMode = 2
                            elif (int(EncStatInfo_DFEE26[0:2], 16) & 0x02) == 0x00:
                                EncryptMode = 1
                    else:
                        DL.SetWindowText("RED", "No Encryption Status Information(DFEE26), Encryption Mode set to default.")

                    if len(DataKSN_DFEE12) == 24:
                        if EncryptMode == 1:
                            EncryptMode = 4
                        elif EncryptMode == 2:
                            EncryptMode = 3

                    DL.SetWindowText("BLUE", "Encryption Mode:"+str(EncryptMode))

                    if EncryptMode != 0:
                        strPAN_5A= DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncPAN_5A)
                        strTK2EqData_57=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, TK2EqData_57)
                        strTK2Discret_9F20=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, TK2Discret_9F20)
                        #DL.SetWindowText("BLUE", "PAN Tag:"+strPAN_5A[0:2])
                        #DL.SetWindowText("BLUE", "PAN LEN:"+strPAN_5A[2:4])
                    else:
                        strPAN_5A = ClrMskPAN_5A
                        strTK2EqData_57 = TK2EqData_57
                        strTK2Discret_9F20 = TK2Discret_9F20

                    DL.SetWindowText("BLUE", "Primary Account Number(5A) Decrypted:"+strPAN_5A)
                    DL.SetWindowText("BLUE", "Track 2 Equivalent Data(57) Decrypted:"+strTK2EqData_57)
                    DL.SetWindowText("BLUE", "Track 2 Discretionary Data(9F20) Decrypted:"+strTK2Discret_9F20)

                    if len(strPAN_5A) != 0 :
                        if EncryptMode !=0:
                            Pan = strPAN_5A[4:(int(strPAN_5A[2:4],16)*2+4)]
                        else:
                            Pan = strPAN_5A
                    DL.SetWindowText("GREEN", "PAN:"+ Pan)
                    DL.SetWindowText("GREEN", "len(EncOlPIN_99):"+ str(len(EncOlPIN_99)))

                    if len(EncOlPIN_99)==36:
                        strDecryptPIN=DL.FormatX_PIN_Block_Decipher(2,1,EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[16:len(EncOlPIN_99)])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:16])
                    elif len(EncOlPIN_99)==40:
                        strDecryptPIN=DL.FormatX_PIN_Block_Decipher(2,1,EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])  
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[16:len(EncOlPIN_99)])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:16])
                    elif len(EncOlPIN_99) == 52:
                        strDecryptPIN = DL.FormatX_PIN_Block_Decipher(1,2,EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[32:len(EncOlPIN_99)])	
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:32])
                    elif len(EncOlPIN_99) == 56:
                        strDecryptPIN = DL.FormatX_PIN_Block_Decipher(1,2,EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) KSN field:"+EncOlPIN_99[32:len(EncOlPIN_99)])
                        DL.SetWindowText("RED", "Encipherd Online PIN(99) Enciphered PIN field:"+EncOlPIN_99[0:32])

                    DL.SetWindowText("BLUE", "Encipherd Online PIN(99):"+EncOlPIN_99)
                    DL.SetWindowText("BLUE", "Encipherd Online PIN(99) Decrypted:"+strDecryptPIN)
        else:
            DL.SetWindowText("RED", "Timeout")    

    else:                                 
        DL.SetWindowText("RED", "Failed")

#Result = DL.SendCommand("Contact Authenticate Transaction (02-06)")
#sResult = DL.Get_RXResponse(0)
#sResult='56 69 56 4F 70 61 79 56 33 00 02 06 00 01 F7 00 00 00 82 02 5C 00 9F 36 02 00 01 9F 07 02 FF C0 9F 26 08 88 2D 84 27 A2 68 E2 14 9F 27 01 40 8E 0A 00 00 00 00 00 00 00 00 02 00 81 04 00 00 00 63 9F 34 03 02 00 00 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 0D 05 F0 20 04 00 00 9F 0E 05 00 50 88 00 00 9F 0F 05 F0 20 04 98 00 9F 10 07 06 01 1A 03 60 00 00 9F 24 00 9F 33 03 60 F8 C8 9F 35 01 22 95 05 42 C0 04 08 00 9F 37 04 49 A6 8E 8F 9F 01 06 56 49 53 41 30 30 9F 02 06 00 00 00 00 00 99 9F 03 06 00 00 00 00 00 00 5F 25 03 95 07 01 5F 24 03 20 12 31 5A A1 08 47 61 CC CC CC CC 00 10 5A C1 10 F1 99 2C 01 86 26 9F D6 94 CF 07 51 4A 58 65 8B 5F 34 01 01 5F 28 02 08 40 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1A 02 08 40 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E 57 C1 20 D6 41 87 14 CB 0B CB 04 8C CC 02 D4 D0 2B 5F 59 DB ED A1 E4 73 0A 45 BD 18 E6 05 3E A6 D4 7C 82 5F 2A 02 08 40 9A 03 30 09 29 9F 21 03 13 41 51 9C 01 00 9F 06 07 A0 00 00 00 03 10 10 9F 09 02 00 96 5F 20 0F 46 55 4C 4C 20 46 55 4E 43 54 49 4F 4E 41 4C 9F 20 C1 10 8B 1B F7 8C 9A 9D A8 B5 1C 5C 81 A1 BB DF DE D7 5F 2D 08 65 73 65 6E 66 72 64 65 50 0A 56 49 53 41 43 52 45 44 49 54 4F 07 A0 00 00 00 03 10 10 84 07 A0 00 00 00 03 10 10 9F 39 01 05 9F 4D 00 9F 13 00 9B 02 E8 00 99 1A 83 F5 E0 E9 47 AB DB 32 AC 50 B0 66 B3 C5 55 13 BF FF 98 76 54 32 10 00 00 0A DF EE 23 00 DF EE 0B 00 FF EE 01 00 DF EE 30 01 01 DF EE 12 0A AF FF 98 76 54 32 10 00 00 1F 1D 89'
#if sResult!=None and sResult!="":
#    sResult=sResult.replace(" ","")
#    sResult=sResult[36:len(sResult)-4]
#    EncOlPIN_99=DL.GetTLV(sResult,"99",0,True)
#		
#    if len(EncOlPIN_99)==32:
#        strDecryptPIN=DL.Format4_PIN_Block_Decipher(EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
#    elif len(EncOlPIN_99)==36:
#        strDecryptPIN=DL.Format4_PIN_Block_Decipher(EncOlPIN_99[16:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:16])
#    elif len(EncOlPIN_99) == 52:
#        strDecryptPIN = DL.Format4_PIN_Block_Decipher(EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])
#    elif len(EncOlPIN_99) == 56:
#        strDecryptPIN = DL.Format4_PIN_Block_Decipher(EncOlPIN_99[32:len(EncOlPIN_99)], PinKey, Pan, EncOlPIN_99[0:32])
#
#    elif len(EncOlPIN_99) == 4:
#    	  strDecryptPIN = EncOlPIN_99
#    	  
#    DL.SetWindowText("BLUE", "Encipherd Online PIN(99):"+EncOlPIN_99)
#    DL.SetWindowText("BLUE", "Encipherd Online PIN(99) Decrypted:"+strDecryptPIN)

    #if strDecryptPIN!="123456":
        #DL.SetWindowText("BLUE", "Dencrypt PIN Block FAIL !!!")
    #else:
        #DL.SetWindowText("BLUE", "Dencrypt PIN Block PASS")
