#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time




Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

CompareCardEncodeType=''
CompareEncryptType=''
CompareEncryptMode=''

Compare_Track1_MaskASCLLCardData=''
Compare_Track2_MaskASCLLCardData=''
Compare_Track3_MaskASCLLCardData=''
ComparePAN=''

CompareTrack1ClearHEX=''
CompareTrack2ClearHEX=''
CompareTrack3ClearHEX=''

CompareTrack1Exist=''
CompareTrack2Exist=''
CompareTrack3Exist=''

CompareTrack1Decode=''
CompareTrack2Decode=''
CompareTrack3Decode=''


def CompareField(strTitle,expectData,cardData):
    if type(expectData)==str:
        if(len(str(expectData))>0):
            expectData = str(expectData).upper()
    if type(cardData) == str:
        if (len(str(cardData)) > 0):
            cardData = str(cardData).upper()
    if (expectData == cardData):
        DL.SetWindowText("Green",strTitle+ " Passed")
    else:
        DL.SetWindowText("Red", strTitle + " Failed")

Result=DL.SendCommand("Activate Transaction(MSR)")
sResult=DL.Get_RXResponse(0)
#sResult="56 69 56 4F 74 65 63 68 32 00 02 00 02 12 C8 DF EE 23 82 01 F9 02 F3 01 80 7F 4A 24 66 07 87 01 29 2A 34 35 34 37 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 34 35 34 37 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 3D 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 34 35 34 37 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 3D 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 06 A1 30 6C 17 BB 26 0D AF E3 8C 63 5A D6 96 53 7F 01 73 9B C7 D4 EF 87 C1 D2 1C C1 7C 8F 1A D5 72 7E 9B 21 41 C1 16 66 4B 32 E0 8D 7B 90 1A 50 8C C1 9E CB 9D FD 16 81 FE 36 0E FC 04 61 C2 90 96 E7 B2 B7 01 7A E0 F3 7C DA B9 FB C4 77 6F 85 73 B0 38 BA 5B 1D B8 D1 81 62 D9 7D 30 02 2C D6 DB 9D 80 2E 70 30 B7 9A 56 FF 8C 1B 54 4F 11 B4 D3 F4 50 29 4A 9E 63 D9 37 06 70 BD 71 75 6A 8A 17 2D 49 DD D3 43 4D E7 69 BC D0 B8 F9 6A DE FB 12 FF F7 36 DD FB 59 82 52 CF 20 14 42 5A 4A D9 D1 D7 88 11 50 6C 20 DB 1D 3A 58 50 F6 53 4D 70 58 A6 68 21 C8 AA C6 5E D3 B4 F1 78 3E 25 9E FC 30 4C A8 BC 68 C0 0B AD 6A 3C 3B 24 FC 55 7E 36 C4 CF 07 76 F3 33 5D 97 CD A6 96 2F 40 F2 E3 FD AF FF 98 76 54 32 10 00 00 03 20 00 9F 29 8D D3 57 18 98 CD 48 B5 1F BA 0F A9 DA 4D 15 72 51 B5 E5 22 D2 95 D7 67 A8 9E DF 37 76 6C CF FF 98 76 54 32 10 00 00 03 FE BE 03 9F 39 01 90 FF EE 01 05 DF EE 30 01 0C DF EE 26 01 C8 5B 60"
DL.SetWindowText("BLUE", sResult)
if sResult!=None and sResult!="":
    sResult=sResult.replace(" ","")
    sResult=sResult[32:len(sResult)-4]
    DL.SetWindowText("BLUE", sResult)
    CardData=DL.GetTLV(sResult,"DFEE23")
    bresult = False
    if CardData!=None and CardData!='':
        objectMSR = DL.ParseCardData(CardData ,bresult,Key,MacKey)
        if objectMSR!=None:
            #msrdecode = '\n'.join(['%s:%s' % item for item in objectMSR.__dict__.items()])
            DL.SetWindowText("blue",str(objectMSR[0].msr_cardType))
        #if DL.ParseCardData(CardData,Key):
            #DL.SetWindowText("Green", "Parse Card Data Pass")

            #CardType=DL.GetCardEncodeType()
            EncryptType = DL.Get_EncryptionKeyType_CardData()
            EncryptMode = DL.Get_EncryptionMode_CardData()

            TRK1Decode = DL.Get_TrackNDecodeStatus_CardData(1)
            TRK2Decode = DL.Get_TrackNDecodeStatus_CardData(2)
            TRK3Decode = DL.Get_TrackNDecodeStatus_CardData(3)
            
            DL.SetWindowText("Black", "Track1Existed:")          
            DL.SetWindowText("Black", str(objectMSR[0].bIsTrack1SamplingDataExits))
            DL.SetWindowText("Black", "Track2Existed:")          
            DL.SetWindowText("Black", str(objectMSR[0].bIsTrack2SamplingDataExits))
            DL.SetWindowText("Black", "Track3Existed:")          
            DL.SetWindowText("Black", str(objectMSR[0].bIsTrack3SamplingDataExits))

            if(CompareCardEncodeType!=""):
                CompareField('Card Type Comparison',CompareCardEncodeType,str(objectMSR[0].msr_cardType))
            if CompareEncryptType!="":
                CompareField('Encrypt Type Comparison',CompareEncryptType,EncryptType)
            if (CompareEncryptMode != ""):
                CompareField('Encrypt Mode Comparison', CompareEncryptMode, EncryptMode)

            if (CompareTrack1Exist != ""):
                CompareField('Track1 Existed Comparison', CompareTrack1Exist, bool(objectMSR[0].bIsTrack1SamplingDataExits)),
            if (CompareTrack2Exist != ""):
                CompareField('Track2 Existed Comparison', CompareTrack2Exist, bool(objectMSR[0].bIsTrack2SamplingDataExits)),
            if (CompareTrack3Exist != ""):
                CompareField('Track3 Existed Comparison', CompareTrack3Exist, bool(objectMSR[0].bIsTrack3SamplingDataExits)),

            if (CompareTrack1Decode != ""):
                CompareField('Track1 Decoded Comparison', CompareTrack1Decode, TRK1Decode),
            if (CompareTrack2Decode != ""):
                CompareField('Track2 Decoded Comparison', CompareTrack2Decode, TRK2Decode),
            if (CompareTrack3Decode != ""):
                CompareField('Track3 Decoded Comparison', CompareTrack3Decode, TRK3Decode),
            
            Track1_CardData = DL.Get_TrackN_CardData(1)
            Track2_CardData = DL.Get_TrackN_CardData(2)
            Track3_CardData = DL.Get_TrackN_CardData(3)

            if(Compare_Track1_MaskASCLLCardData!=""):
                CompareField('Track1 ASCII Mask/Clear Data Comparison', Compare_Track1_MaskASCLLCardData, Track1_CardData)
            if (Compare_Track2_MaskASCLLCardData != ""):
                CompareField('Track2 ASCII Mask/Clear Data Comparison', Compare_Track2_MaskASCLLCardData, Track2_CardData)
            if (Compare_Track3_MaskASCLLCardData != ""):
                CompareField('Track3 ASCII Mask/Clear Data Comparison', Compare_Track3_MaskASCLLCardData, Track3_CardData)

            PAN = DL.Get_PAN_CardData()
            if ComparePAN!='':
                CompareField('PAN', ComparePAN, PAN)

            TRK1 = DL.Get_EncryptTrackN_CardData(1)
            TRK2 = DL.Get_EncryptTrackN_CardData(2)
            TRK3 = DL.Get_EncryptTrackN_CardData(3)
            KSN=DL.Get_KSN_CardData()

            if len(TRK1)>0:
                TRK1DecryptData=DL.DecryptDLL( EncryptType,EncryptMode , Key ,KSN ,TRK1 )
                TRK1DecryptData=TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
                if(CompareTrack1ClearHEX!=""):
                    CompareField('Track1 Decrypt', CompareTrack1ClearHEX, TRK1DecryptData)

            if len(TRK2) > 0:
                TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
                TRK2DecryptData=TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
                if(CompareTrack2ClearHEX!=""):
                    CompareField('Track2 Decrypt', CompareTrack2ClearHEX, TRK2DecryptData)


            if len(TRK3) > 0:
                TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
                TRK3DecryptData=TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]
                if (CompareTrack3ClearHEX !=""):
                    CompareField('Track3Decrypt', CompareTrack3ClearHEX, TRK3DecryptData)

        else:
            DL.SetWindowText("RED", "Parse Card Data Fail")
'''
if DL.GetCardEncodeType()==0X80:
    Result=DL.SendCommand("Display Message and Get Encrypted PIN (62-01)")
    xsResult=DL.Get_RXResponse(0)
    time.sleep(10)
    sResult1=DL.Get_RXResponse(1)
    if sResult1!=None and sResult1!="":
        sResult1=sResult1.replace(" ","")
        sResult1=sResult1[30:len(sResult1)-4]
        DL.SetWindowText("BLUE", sResult1)
        sResult1 = DL.getASCIIArray(sResult1)
        DL.SetWindowText("BLUE", sResult1)
        if len(sResult1)==56:
            pinKSN=sResult1[0:24]
            DL.SetWindowText("BLUE", pinKSN)
            PINBlock=sResult1[24:56]
            DL.SetWindowText("BLUE", PINBlock)
            #a_PAN='476173900101001'
            ClearPIN=DL.Format4_PIN_Block_Decipher(pinKSN, Key, PAN, PINBlock)
            if ClearPIN=='123456':
                DL.SetWindowText("Green", "Decrypt PIN Pass")
'''

'''
 ############objectMSR[0]#############
public bool bHasFieldKSN;
        public bool bHasKSN;
        public bool bHasMacField;
        public bool bHasSessionID;
        public bool bHasSN;
        public bool bHasTransactionID;
        public bool bIsOptionalBytesLengthFieldExits;
        public bool bIsTrack1ClearorMaskDataPresent;
        public bool bIsTrack1DecodeSuccess;
        public bool bIsTrack1EncryptedDataPresent;
        public bool bIsTrack1HashDataPresent;
        public bool bIsTrack1SamplingDataExits;
        public bool bIsTrack2ClearorMaskDataPresent;
        public bool bIsTrack2DecodeSuccess;
        public bool bIsTrack2EncryptedDataPresent;
        public bool bIsTrack2HashDataPresent;
        public bool bIsTrack2SamplingDataExits;
        public bool bIsTrack3ClearorMaskDataPresent;
        public bool bIsTrack3DecodeSuccess;
        public bool bIsTrack3EncryptedDataPresent;
        public bool bIsTrack3HashDataPresent;
        public bool bIsTrack3SamplingDataExits;
        public byte byte8;
        public byte byte9;
        public int cardDataTotalLength;
        public byte[] CheckMacValueData;
        public string device_RSN;
        public ENCRYPTION_KEY_TYPE encryptionKeyType;
        public ENCRYPTION_MODE encryptionMode;
        public int encT1len;
        public int encT2len;
        public int encT3len;
        public KEY_MANAGEMENT_TYPE keyManagementType;
        public byte[] MacKSN_DUKPT;
        public byte[] MacValue;
        public byte[] MacValueLength;
        public CAPTURE_ENCODE_TYPE msr_cardType;
        public string msr_Decrypt_Track1;
        public string msr_Decrypt_Track2;
        public string msr_Decrypt_Track3;
        public string msr_encryptionKey;
        public byte[] msr_encTrack1;
        public byte[] msr_encTrack2;
        public byte[] msr_encTrack3;
        public byte[] msr_hashTrack1;
        public byte[] msr_hashTrack2;
        public byte[] msr_hashTrack3;
        public byte[] msr_KSN;
        public byte[] msr_rawData;
        public string msr_rawData_KB;
        public byte[] msr_sessionID;
        public string msr_track1;
        public int msr_track1Length;
        public string msr_track2;
        public int msr_track2Length;
        public string msr_track3;
        public int msr_track3Length;
        public byte[] OptionalBytes;
        public byte OptionalBytesLength;
        public string optionalStatusValue;
        public string ParseCardData_FailedReason;
        public byte[] SessionID;
        public byte[] TransactionID;'''