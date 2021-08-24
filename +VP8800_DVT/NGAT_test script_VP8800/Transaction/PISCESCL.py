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
DDCardTK1_DFEE31=''
DDCardTK2_DFEE32=''
EncryptMode=0

Result = DL.SendCommand("02-05(All)")
sResult = DL.Get_RXResponse(0)
#sResult ='56 69 56 4F 70 61 79 56 33 00 02 05 00 01 A1 00 00 00 82 02 5C 00 9F 36 02 00 01 9F 07 02 FF C0 9F 26 08 78 5A D2 22 B6 63 68 B8 9F 27 01 40 8E 0C 00 00 00 00 00 00 00 00 5F 03 00 00 81 04 00 00 00 63 9F 34 03 5F 03 02 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 0D 05 00 00 00 00 00 9F 0E 05 00 00 00 00 00 9F 0F 05 00 00 00 00 00 9F 10 07 06 01 1A 03 90 00 00 9F 24 00 9F 33 03 60 F8 C8 9F 35 01 22 95 05 42 80 00 00 00 9F 37 04 8A F3 E8 6D 9F 01 06 56 49 53 41 30 30 9F 02 06 00 00 00 00 00 99 9F 03 06 00 00 00 00 00 00 5F 25 03 95 07 01 5F 24 03 20 12 31 5A 08 47 61 73 90 01 01 00 10 5F 34 01 01 5F 28 02 08 40 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1A 02 08 40 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E 57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89 5F 2A 02 08 40 9A 03 20 03 08 9F 21 03 06 07 05 9C 01 00 9F 06 07 A0 00 00 00 03 10 10 9F 09 02 00 96 5F 20 0F 46 55 4C 4C 20 46 55 4E 43 54 49 4F 4E 41 4C 9F 20 00 5F 2D 08 65 73 65 6E 66 72 64 65 50 0A 56 49 53 41 43 52 45 44 49 54 4F 07 A0 00 00 00 03 10 10 84 07 A0 00 00 00 03 10 10 9F 39 01 05 9F 4D 00 9F 13 00 9B 02 C8 00 99 00 DF EE 23 00 DF EE 0B 00 FF EE 01 05 DF EE 30 01 01 DF EE 26 01 00 D8 70'

if sResult!=None and sResult!="":
    sResult=sResult.replace(" ","")
    if sResult[24:26] != '0A':
        if sResult[24:26] != '08':
            if sResult[24:26] == '23':
                sResultTLV=sResult[32:len(sResult)-4]
            else:
                sResultTLV=sResult[30:len(sResult)-4]
            DL.SetWindowText("BLUE", sResult)
            DL.SetWindowText("GREEN", sResultTLV)
            DL.SetWindowText("RED", "Parse TLVs")
            ClrMskPAN_5A =  DL.GetTLV(sResultTLV,"5A",0,True)
            EncPAN_5A = DL.GetTLV(sResultTLV,"5A",1,False)
            EncStatInfo_DFEE26 = DL.GetTLV(sResultTLV, "DFEE26",0, False)
            ClrMskTK1EqData_56 = DL.GetTLV(sResultTLV, "56",0, False)
            EncTK1EqData_56 = DL.GetTLV(sResultTLV, "56",1, False)
            ClrMskTK2EqData_57 = DL.GetTLV(sResultTLV, "57",0, False)
            EncTK2EqData_57 = DL.GetTLV(sResultTLV, "57",1, False)
            TK2Discret_9F20= DL.GetTLV(sResultTLV, "9F20",0, False)
            DataKSN_DFEE12 = DL.GetTLV(sResultTLV, "DFEE12", 0, False)
            ClrMskTK1_DFEF17 = DL.GetTLV(sResultTLV, "DFEF17", 0, False)
            EncTK1_DFEF17 = DL.GetTLV(sResultTLV, "DFEF17", 1, False)
            ClrMskTK2_DFEF18 = DL.GetTLV(sResultTLV, "DFEF18", 0, False)
            EncTK2_DFEF18 = DL.GetTLV(sResultTLV, "DFEF18", 1, False)
            EncOlPIN_99=DL.GetTLV(sResultTLV,"99",0,False)
            MC3IMsgData_FFEE04=DL.GetTLV(sResultTLV,"FFEE04",0,False)
            if len(MC3IMsgData_FFEE04) != 0:
                DL.SetWindowText("RED", "Parse TLV-FFEE04")
                MC3IMsgMark_FFEE05=DL.GetTLV(MC3IMsgData_FFEE04,"FFEE05",0,True)
                if len(MC3IMsgMark_FFEE05) != 0:
                    DL.SetWindowText("RED", "Parse TLV-FFEE05")
                    DataRec_FF8105=DL.GetTLV(MC3IMsgMark_FFEE05,"FF8105",0,True)
                    if len(DataRec_FF8105) != 0:
                        DL.SetWindowText("RED", "Parse TLV-FF8105")
                        ClrMskTK1EqData_56 = DL.GetTLV(DataRec_FF8105, "56",0, True)
                        EncTK1EqData_56 = DL.GetTLV(DataRec_FF8105, "56",1, False)
                        ClrMskTK2EqData_57 = DL.GetTLV(DataRec_FF8105, "57",0, False)
                        EncTK2EqData_57 = DL.GetTLV(DataRec_FF8105, "57",1, False)
            ViVDataset_FFEE01=DL.GetTLV(sResultTLV,"FFEE01",0,False)
            if len(ViVDataset_FFEE01) != 0:
                DL.SetWindowText("RED", "Parse TLV-FFEE01")
                DDCardTK1_DFEE31=DL.GetTLV(sResultTLV,"DFEE31",0,True)
                DDCardTK2_DFEE32=DL.GetTLV(sResultTLV,"DFEE32",0,False)


            DL.SetWindowText("BLUE", "Encryption Status Information(DFEE26):"+str(EncStatInfo_DFEE26))
            if len(EncStatInfo_DFEE26) != 0:
                if (int(EncStatInfo_DFEE26[0:2], 16) & 0x80) == 0x00:
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
                strTK1EqData_56=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncTK1EqData_56)
                strTK2EqData_57=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncTK2EqData_57)
                strTK2Discret_9F20=  DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, TK2Discret_9F20)
                strTK1_DFEF17= DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncTK1_DFEF17)
                strTK2_DFEF18= DL.DecryptDLL(0, EncryptMode, DataKey, DataKSN_DFEE12, EncTK2_DFEF18)
                #DL.SetWindowText("BLUE", "PAN Tag:"+strPAN_5A[0:2])
                #DL.SetWindowText("BLUE", "PAN LEN:"+strPAN_5A[2:4])
            else:
                strPAN_5A = ClrMskPAN_5A
                strTK1EqData_56 = ClrMskTK1EqData_56
                strTK2EqData_57 = ClrMskTK2EqData_57
                strTK2Discret_9F20 = TK2Discret_9F20
                strTK1_DFEF17 = ClrMskTK1_DFEF17
                strTK2_DFEF18 = ClrMskTK2_DFEF18

            DL.SetWindowText("BLUE", "Primary Account Number(5A) Decrypted:"+strPAN_5A)
            DL.SetWindowText("BLUE", "Track 1 Equivalent Data(56) Decrypted:"+strTK1EqData_56)
            DL.SetWindowText("BLUE", "Track 2 Equivalent Data(57) Decrypted:"+strTK2EqData_57)
            DL.SetWindowText("BLUE", "Track 2 Discretionary Data(9F20) Decrypted:"+strTK2Discret_9F20)
            DL.SetWindowText("BLUE", "Track 1 Data(DFEF17) Decrypted:"+strTK1_DFEF17)
            DL.SetWindowText("BLUE", "Track 2 Data(DFEF18) Decrypted:"+strTK2_DFEF18)
            DL.SetWindowText("BLUE", "DD Card Track 1:"+DDCardTK1_DFEE31)
            DL.SetWindowText("BLUE", "DD Card Track 2:"+DDCardTK2_DFEE32)


            DL.SetWindowText("RED", sResult[24:26])

        else:
            DL.SetWindowText("RED", "Timeout")

    else:
        DL.SetWindowText("RED", "Failed")

