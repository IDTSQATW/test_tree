#!/usr/bin/env python
import sys
import time
import clr
import System
import time
import re
from System import Array, Byte
DL.setText("BLACK", '[Case1: NFC White List.\r\n[Activated and Key Injection-> Swipe PayPass Demo #3 Card Encryption -> Set whitelist (contain Paypass test Card AID) -> Swipe Card Not Encryption -> Clear WhiteList -> PayPass Demo #3 Card Encryption again]]')

"""
---------------------------------------------------------------->
---------------------------------------------------------------->
---------------------------------------------------------------->
Below Part are common part of public Method.
Methods to translate to and from binary coded decimal
"""

def int_to_bcd(x):
    """
    This translates an integer into
    binary coded decimal
    """
    if x < 0:
        raise ValueError("Cannot be a negative integer")
    bcdstring = ''
    while (x > 0):
        nibble = x % 16
        if (nibble <= 9):
            bcdstring = str(nibble) + bcdstring

        if (nibble == 10):
            bcdstring = 'A' + bcdstring

        if (nibble == 11):
            bcdstring = 'B' + bcdstring

        if (nibble == 12):
            bcdstring = 'C' + bcdstring

        if (nibble == 13):
            bcdstring = 'D' + bcdstring

        if (nibble == 14):
            bcdstring = 'E' + bcdstring

        if (nibble == 15):
            bcdstring = 'F' + bcdstring

        x >>= 4

    if (len(bcdstring) == 1):
        return  '0' + bcdstring
    else:
        return bcdstring


#!  This Method get current OS time.
#!  return a list of below:
#!                  [year, month, day, hour, minute, second]
#!
def getDateTime():
    strYMD = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    Year = strYMD[0:4]
    Month = strYMD[5:7]
    Day = strYMD[8:10]
    Hour = strYMD[11:13]
    Minute = strYMD[14:16]
    Second = strYMD[17:19]
    Data_List=[]
    Data_List.append(Year)
    Data_List.append(Month)
    Data_List.append(Day)
    Data_List.append(Hour)
    Data_List.append(Minute)
    Data_List.append(Second)
    return Data_List

#!  This Method get current OS time and convert it to BCD Code Format.
#!  Data Item	Length bytes	    Description
#!  Minutes     1                   mm 2-digit,BCD,Range 00-59
#!  Hour	    1	                HH 2-digit, BCD, Range 00-23
#!  Year1	    1	                YY1 (Higher Century Byte)  2-digit, BCD, Range 00-99
#!  Year2	    1	                YY2 (Lower Century Byte)  2-digit, BCD, Range 00-99
#!  Month	    1	                MM  2-digit, BCD, Range 01-12
#!  Date	    1	                DD  2-digit, BCD, Range 01-31
#!  return a string of below:
#!                  nHour + nMinute + nYear1 + nYear2 + nMonth + nDate

def getUTCCommandTime_BCD():
    MyTime = getDateTime()
    Hour = MyTime[3]
    nHour = int_to_bcd(int(Hour,10))

    Minute = MyTime[4]
    nMinute = int_to_bcd(int(Minute,10))

    Year1 = MyTime[0][0:2]
    nYear1 = int_to_bcd(int(Year1,10))

    Year2 = MyTime[0][2:4]
    nYear2 = int_to_bcd(int(Year2,10))

    Month = MyTime[1]
    nMonth = int_to_bcd(int(Month,10))

    Date = MyTime[2]
    nDate = int_to_bcd(int(Date,10))
    print (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)
    return (nHour + nMinute + nYear1 + nYear2 + nMonth + nDate)

"""
<----------------------------------------------------------------
<----------------------------------------------------------------
<----------------------------------------------------------------
End of Common part of public method.
"""
Result = True
RetOfStep = True
strSN = '360Z000008'
strCerFromDevice = ''
StrEnable = '00'
StrDisable = '01'
strNonce = ''
#strWhitelist = 'FFEE0C2ADFEF220E4130303030303030303431303130FFEE0A14DFEF2106373037363131DFEF2106373037363939'
strWhitelist = 'FFEE0C14DFEF211034373631373339303031303130303130'
strCerFromDevice = ''
VP3600 = False
VP5300 = False
VP6300 = False
VP8800 = False
NEOIIStandart = False


def SMFGMasterReset():
    DL.setText("GREEN", 'Do SMFG Master Reset Process:')
    RetOfStep = DL.SendCommand('Get SN (12-01)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("12 00")
        if (Result):
            strResponse = DL.Get_RXResponse(0)
            strResponse = strResponse.replace(" ", "")
            strSerialN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
            if (strSN != ''):
                RetOfStep = DL.SendCommand('Get Device Nonce (91-08)')
                if (RetOfStep):
                    Result = DL.Check_RXResponse("91 00")
                    if (Result):
                        strResponse = DL.Get_RXResponse(0)
                        strResponse = strResponse.replace(" ", "")
                        strNonce = strResponse[28:len(strResponse) - 4]
                        if (strNonce != ''):
                            strSignedCommandData = DL.signMFGCommand(strNonce, '91', '00', strSerialN)
                            if (strSignedCommandData != ""):
                                RetOfStep = DL.SendCommand_ReplaceCommand('SMFG Master Reset (91-00)',
                                                                          strSignedCommandData)
                                if (RetOfStep):
                                    Result = DL.Check_RXResponse("91 00")
                                    DL.setText("GREEN", 'Finish SMFG Master Reset')
                                    Result = True
                                    time.sleep(1)
                                else:
                                    DL.setText("RED", 'SMFG Master Reset Fail')
                                    Result = False
    return  Result


"""
UMFG Activating Process
"""
def UMFGActivating():
    Result = True
    DL.setText("GREEN", 'Do UMFG Activating Prcess:')
    if (Result):
        RetOfStep = DL.SendCommand('UMFG Device Reset')
        strResponse = DL.Get_RXResponse(0)
        strResponse = strResponse.replace(" ", "")
        ErrorCode = strResponse[22:24]
        DL.setText("GREEN", 'Errocode:' + ErrorCode)
        if (ErrorCode == '12')|(ErrorCode == '2A'):
            Result = SMFGMasterReset()
            RetOfStep = DL.SendCommand('UMFG Device Reset')
            if (RetOfStep):
                Result = DL.Check_RXResponse("90 00")
                Result = True

    if (Result):
        mytime = getUTCCommandTime_BCD()
        DL.setText("BLACK", mytime)
        RetOfStep = DL.SendCommand_ReplaceQustionMark('UMFG Set UTC', mytime)
        if (RetOfStep):
            Result = DL.Check_RXResponse("90 00")
    time.sleep(1)
    if (Result):
        RetOfStep = DL.SendCommand('UMFG Activate')
        if (RetOfStep):
            Result = DL.Check_RXResponse("90 00")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strCerFromDevice = strResponse[48:len(strResponse) - 4]
                DL.setText("GREEN", strCerFromDevice)
    time.sleep(1)
    if (Result):
        Result = DL.LoadCerts("90 03", strCerFromDevice, strSN)
        time.sleep(1)

    if (Result):
        RetOfStep = DL.SendCommand('UMFG Validate Certificate Tree')
        if (RetOfStep):
            Result = DL.Check_RXResponse("90 00")
            time.sleep(1)

    if (Result):
        RetOfStep = DL.SendCommand('UMFG Lock')
        if (RetOfStep):
            Result = DL.Check_RXResponse("90 00")
            time.sleep(1)
    Result = True
    return  Result
'''
    DL.setText("GREEN", 'UMFG Lock Success, Set Into SMFG Status!!!')
    if (Result):
        RetOfStep = DL.SendCommand('Restart (77-05)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("77 00")
            time.sleep(1)
    return  Result'''
"""
---------------------------------------------------------------->
Script Begin Now......
---------------------------------------------------------------->
"""
DL.setText("BLACK", 'Case 1:NFC White List.\r\n[Activated and Key Injection-> Swipe PayPass Demo #3 Card Encryption -> Set whitelist (contain Paypass test Card AID) -> Swipe Card Not Encryption -> Clear WhiteList -> PayPass Demo #3 Card Encryption again]')
Result = True
if (Result):
    RetOfStep = DL.SendCommand('Get Firmware Version (29-00)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("29 00")
        if (Result):
            strResponse = DL.Get_RXResponse(0)
            strResponse = strResponse.replace(" ", "")
        if(-1 != strResponse.find("565033363030")):
            DL.setText("BLACK", '[VP3600 Connected]')
            strSN = '360Z000008'
            VP3600 = True
        elif(-1 != strResponse.find("565036333030")):
            DL.setText("BLACK", '[VP6300 Connected]')
            strSN = '630Z000008'
            VP6300 = True
        elif(-1 != strResponse.find("565035333030")):
            DL.setText("BLACK", '[VP5300 Connected]')
            strSN = '530Z000008'
            VP5300 = True
        elif(-1 != strResponse.find("415220332E302E")):
            DL.setText("BLACK", '[VP8800 Connected]')
            strSN = '880Z000001'
            VP8800 = True
        else:
            NEOIIStandart = True
    else:
        Result = False
if (Result):
    RetOfStep = DL.SendCommand_ReplaceQustionMark('SMFG Secure Task Control', StrEnable)
    if (RetOfStep):
        Result = DL.Check_RXResponse("90 00")
        DL.setText("GREEN", 'Enable UMFG Secure Task')
if (Result):
    RetOfStep = UMFGActivating()
    if(RetOfStep):
        DL.setText("GREEN", 'Finish UMFG Activating Process, Device Ready')
        time.sleep(5)
    else:
        DL.setText("RED", 'UMFG Activating Process Fail, Master Reset Deactivated !')
        Result = False
if (Result):
    DL.setText("GREEN", 'UMFG Lock Success, Set Into SMFG Status!!!')
    RetOfStep = DL.SendCommand('Restart (77-05)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("77 00")
        time.sleep(60)

if(VP3600 == True):
    DL.setText("GREEN", '[VP3600: key injection]')
    if (Result):
        RetOfStep = DL.SendCommand('Load KEK')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F2 03 00 5B AE 0A")
            if(Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ","")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if(strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('Load DEK KSN:3333')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if(Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ","")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if(strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('Load PEK KSN:44444')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if(Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ","")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if(strSN != ''):
                    Result = True
    if (Result):
        RetOfStep = DL.SendCommand('Load Mac KSN:FF987')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if(Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ","")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if(strSN != ''):
                    Result = True
if(VP5300 == True):
    DL.setText("GREEN", '[VP5300: key injection]')
    if (Result):
        RetOfStep = DL.SendCommand('KEK5300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F2 03 00 5B AE 0A")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('DEK(KSN:All 1)5300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('PairingKey(KSN:All 9)5300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

if(VP6300 == True):
    DL.setText("GREEN", '[VP6300: key injection]')
    if (Result):
        RetOfStep = DL.SendCommand('KEK6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F2 03 00 5B AE 0A")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('DEK(KSN:All 1)6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('MAC(KSN:All 2)6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

if(VP8800 == True):
    DL.setText("GREEN", '[VP8800: key injection]')
    if (Result):
        RetOfStep = DL.SendCommand('KEK6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F2 03 00 5B AE 0A")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('DEK(KSN:All 1)6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True

    if (Result):
        RetOfStep = DL.SendCommand('MAC(KSN:All 2)6300')
        if (RetOfStep):
            Result = DL.Check_RXResponse("78 46 F3")
            if (Result):
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strSN = DL.getASCIIArray(strResponse[28:len(strResponse) - 4])
                if (strSN != ''):
                    Result = True
					
					
if (Result):
    RetOfStep = DL.SendCommand('Get Key Status (81 0C)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("81 00")
        if(Result):
            strResponse = DL.Get_RXResponse(0)
            strResponse = strResponse.replace(" ","")
            if(-1 != strResponse.find('1400')):
                DL.setText("GREEN", '[Exist LCL KEK] PASS')
            else:
                DL.setText("RED", '[Not Exist LCL KEK] FAIL')
                Result = False
            if(VP3600 == True):
                if(-1 != strResponse.find('0100')):
                    DL.setText("GREEN", '[Exist PEK] PASS')
                else:
                    DL.setText("RED", '[Not Exist PEK] FAIL')
                    Result = False
                if((-1 != strResponse.find('0500'))|(-1 != strResponse.find('0501'))):
                    DL.setText("GREEN", '[Exist MAC Key] PASS')
                else:
                    DL.setText("RED", '[Not Exist MAC Key] FAIL')
                    Result = False
            if (VP5300 == True):
                if (-1 != strResponse.find('0A00')):
                    DL.setText("GREEN", '[Exist Paring Key] PASS')
                else:
                    DL.setText("RED", '[Not Exist Paring Key] FAIL')
                    Result = False
            if(-1 != strResponse.find('0200')):
                DL.setText("GREEN", '[Exist DEK] PASS')
            else:
                DL.setText("RED", '[Not Exist DEK] FAIL')
                Result = False
            if(VP6300):
                if((-1 != strResponse.find('0500'))|(-1 != strResponse.find('0501'))):
                    DL.setText("GREEN", '[Exist MAC Key] PASS')
                else:
                    DL.setText("RED", '[Not Exist MAC Key] FAIL')
                    Result = False
    else:
        DL.setText("RED", 'Get Key Status Fail !!!')
        ErrorCode = strResponse[22:24]
        DL.setText("GREEN", 'Errocode:' + ErrorCode)
        Result = False
if (Result):
    RetOfStep = DL.SendCommand('Set to Default')
    if (RetOfStep):
        Result = DL.Check_RXResponse("04 00")
    time.sleep(4)
Result = True

if (Result):
    RetOfStep = DL.SendCommand('Get SN (12-01)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("12 00")
        if (Result):
            strResponse = DL.Get_RXResponse(0)
            strResponse = strResponse.replace(" ", "")
            strSerialN = DL.getASCIIArray(strResponse[28:48])
            DL.setText("GREEN", 'Get Serial Number:[' + strSerialN + ']')
            Result = True
        else:
            DL.setText("RED", 'Get Serial Number Fail!')
            Result = False

DL.SendCommand('Reconnect')

# Set WL
if (Result):
    RetOfStep = DL.SendCommand_ReplaceQustionMark('SMFG Secure Task Control', StrEnable)
    if (RetOfStep):
        Result = DL.Check_RXResponse("90 00")
        DL.setText("GREEN", 'Enable UMFG Secure Task')
if (Result):
    RetOfStep = DL.SendCommand('Get Device Nonce (91-08)')
    if (RetOfStep):
        strResponse = DL.Get_RXResponse(0)
        strResponse = strResponse.replace(" ","")
    if(strResponse.find("9100") != -1):
        strNonce = strResponse[28:len(strResponse) - 4]
        DL.setText("GREEN", 'Get NONCE:[' + strNonce + ']')
    if(strResponse.find("9121") != -1):
        DL.setText("GREEN", 'Deactived Reader, Do UMFG Active Process!')
        if(UMFGActivating()):
            DL.setText("GREEN", 'Activated')
            time.sleep(5)
            RetOfStep = DL.SendCommand_ReplaceQustionMark('SMFG Secure Task Control', StrEnable)
            if (RetOfStep):
                Result = DL.Check_RXResponse("90 00")
                DL.setText("GREEN", 'Enable UMFG Secure Task')
            RetOfStep = DL.SendCommand('Get Device Nonce (91-08)')
            if (RetOfStep):
                Result = DL.Check_RXResponse("91 00")
                strResponse = DL.Get_RXResponse(0)
                strResponse = strResponse.replace(" ", "")
                strNonce = strResponse[28:len(strResponse) - 4]
                DL.setText("GREEN", 'Get NONCE:['+ strNonce + ']')
                Result = True
        else:
            DL.setText("RED", 'Deactived, Do UMFG Active Process FAIL !!!')
    if(strResponse.find("9100") == -1) & (strResponse.find("9121") == -1):
        DL.setText("RED", 'Get NONCE Wrong !')
        ErrorCode = strResponse[22:24]
        DL.setText("RED", 'Errocode:' + ErrorCode)
        Result = False

if (Result):
    DL.setText("GREEN", 'Load Whitelist:\r\n[' + strWhitelist + ']')
    DL.setText("GREEN", 'SN:\r\n[' + strSerialN + ']')
    DL.setText("GREEN", 'strNonce:\r\n[' + strNonce + ']')
    strSignedCommandData = DL.signMFGCommand(strNonce, '91', '13',strSerialN, strWhitelist)
    if (strSignedCommandData != ""):
        RetOfStep = DL.SendCommand_ReplaceCommand('SMFG Set White List (91-13)',
                                                  strSignedCommandData)
        if (RetOfStep):
            Result = DL.Check_RXResponse("91 00")
            DL.setText("GREEN", 'Finish SMFG Load Whitelist')
            Result = True
            time.sleep(1)
        else:
            DL.setText("RED", 'SMFG Load Whitelist Fail !')
            Result = False

if (Result):
    RetOfStep = DL.SendCommand('Get White List (2C-51)')
    if (RetOfStep):
        Result = DL.Check_RXResponse("2C 00")
        if(Result):
            strResponse = DL.Get_RXResponse(0)
            strResponse = strResponse.replace(" ", "")
        if(strResponse.find(strWhitelist) != -1):
            DL.setText("GREEN", 'Compare response white list same as SMFG seted - PASS')
            Result = True
        else:
            DL.setText("RED", 'Error: 2C-51 retrived MSR white list wrong - FAIL')
            Result = False

#Exchange APDU -- card's PAN in WhiteList
if (Result):
	RetOfStep = DL.SendCommand('PT STOP')
	if (RetOfStep):
		Result = DL.Check_RXResponse("2C") and Result

if (Result):
	RetOfStep = DL.SendCommand(' PT START')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 00 1C 9B") and Result

if (Result):
	RetOfStep = DL.SendCommand(' E P4T 01')
	if (RetOfStep):
		str=DL.Get_RXResponse(1)
		Result = DL.Check_StringAB(str,'56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 07') and Result

if (Result):
	RetOfStep = DL.SendCommand(' PPSE')
	if (RetOfStep):
		Result = DL.Check_RXResponse("2C 00 00 35 6F 31 84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 A5 1F BF 0C 1C 61 1A 4F 07 A0 00 00 00 03 10 10 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 87 01 01 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Select AID')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 49 6F 45 84 07 A0 00 00 00 03 10 10 A5 3A 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 87 01 01 9F 38 0C 9F 66 04 9F 02 06 9F 37 04 5F 2A 02 5F 2D 04 65 73 65 6E 9F 11 01 01 9F 12 0C 50 72 65 66 20 4E 61 6D 65 20 30 31 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' GPO -Contain57')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 77 81 B6 82 02 20 00 94 08 08 01 02 00 10 01 02 01 9F 36 02 00 03 57 13 47 61 73 90 01 01 00 10 D2 01 21 20 00 12 33 99 00 03 1F 9F 10 07 06 01 11 03 90 00 00 9F 26 08 AA BB CC DD EE FF 11 22 5F 34 01 01 9F 6C 02 20 00 9F 5D 06 00 00 00 01 00 00 9F 4B 60 ** 9F 27 01 40 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI1-Recore1')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 B5 70 81 B0 8F 01 51 90 81 90 D2 AB 9F D6 4D EB 30 A3 A0 1F C5 4A E6 EF 00 F8 B0 54 A5 53 A1 7A 2A F2 E9 6B 83 71 CA AB 9E 61 6E EA 73 B7 C6 BB 83 FE 83 8B CF 76 56 29 33 4C 85 10 5F 5C 08 55 16 F4 97 CA 74 39 9D D3 05 EA 4A 62 CC 56 63 C9 8E 9F 5D 86 3D 84 E1 53 A9 B0 FE 14 3E A8 E9 DA D3 F6 E2 DC 0D 8A 97 DF 26 A7 9A DF 81 F6 F0 1B A4 29 A8 FC 26 03 9E F5 74 27 27 24 16 51 8C E9 9D 73 3E EA EA 48 90 43 C4 A5 A8 F1 BB 55 17 BD 1A 3E 35 66 4A F4 61 C7 E7 78 92 14 95 BE 48 F2 C7 7F 93 C8 3F 9F C6 BF EB 72 30 01 F9 8E E7 23 9F 32 01 03 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand('Read Record SFI1-Recored2')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 70 81 9B 9F 46 81 80 A8 6F 37 63 77 22 02 36 1D 0B CA 5E 92 11 BA 95 F5 E1 CD B7 8F 8F 03 ED 77 49 25 E7 2B C9 CE 7D 0D C4 5F 42 BD 7C B3 8B 53 61 13 D0 9E 7F E8 5F EB 61 C1 EA 43 53 1F B2 97 8A 1A F1 59 97 D5 84 B7 BC 27 3D AB 8F 87 5F 06 72 50 09 1B AC AA E1 01 3B 33 F6 ED 7E A1 C8 73 2D 4D 63 A7 C6 F2 F9 77 C1 BD F9 0C 4F 74 96 E7 30 C4 58 5E EA EA 6A E6 81 C1 01 A8 B3 BE 14 A2 02 DD EB 22 65 43 DB 9F 47 03 01 00 01 9F 4A 01 82 9F 48 0A B4 C6 04 13 20 31 38 75 96 C7 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI2-Record1 -ContainPAN')
	if (RetOfStep):
		Result = DL.Check_RXResponse("70 10 5A 08 47 61 73 90 01 01 00 10 5F 24 03 20 12 31 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI2-Record2')
	if (RetOfStep):
		Result = DL.Check_RXResponse("70 0A 9F 69 07 01 11 22 33 44 20 00 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' PT STOP')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 00 1C 9B") and Result

		
#clear White List
if (Result):
	RetOfStep = DL.SendCommand_ReplaceQustionMark('SMFG Secure Task Control', StrEnable)
	if (RetOfStep):
		Result = DL.Check_RXResponse("90 00")
		DL.setText("GREEN", 'Enable UMFG Secure Task')
if (Result):
	RetOfStep = DL.SendCommand('Get Device Nonce (91-08)')
	if (RetOfStep):
		strResponse = DL.Get_RXResponse(0)
    	strResponse = strResponse.replace(" ","")
	if(strResponse.find("9100") != -1):
		strNonce = strResponse[28:len(strResponse) - 4]
		DL.setText("GREEN", 'Get NONCE:[' + strNonce + ']')
		Result = True
	else:
		DL.setText("RED", 'Get NONCE Fail !')
		Result = False

if (Result):
	DL.setText("GREEN", 'Clear Whitelist')
	strSignedCommandData = DL.signMFGCommand(strNonce, '91', '14', strSerialN)
	if (strSignedCommandData != ""):
		RetOfStep = DL.SendCommand_ReplaceCommand('SMFG Clear White List (91-14)',
												  strSignedCommandData)
		if (RetOfStep):
			Result = DL.Check_RXResponse("91 00")
			DL.setText("GREEN", 'Finish SMFG Clear Whitelist' )
			Result = True
			time.sleep(1)
		else:
			DL.setText("RED", 'SMFG Load Clear Fail !')
			Result = False
			
#Exchange APDU -- White list cleared
if (Result):
	RetOfStep = DL.SendCommand('PT STOP')
	if (RetOfStep):
		Result = DL.Check_RXResponse("2C") and Result

if (Result):
	RetOfStep = DL.SendCommand(' PT START')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 00 1C 9B") and Result

if (Result):
	RetOfStep = DL.SendCommand(' E P4T 01')
	if (RetOfStep):
		str=DL.Get_RXResponse(1)
		Result = DL.Check_StringAB(str,'56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 07') and Result

if (Result):
	RetOfStep = DL.SendCommand(' PPSE')
	if (RetOfStep):
		Result = DL.Check_RXResponse("2C 00 00 35 6F 31 84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 A5 1F BF 0C 1C 61 1A 4F 07 A0 00 00 00 03 10 10 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 87 01 01 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Select AID')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 49 6F 45 84 07 A0 00 00 00 03 10 10 A5 3A 50 0C 56 49 53 41 20 54 45 53 54 20 30 31 87 01 01 9F 38 0C 9F 66 04 9F 02 06 9F 37 04 5F 2A 02 5F 2D 04 65 73 65 6E 9F 11 01 01 9F 12 0C 50 72 65 66 20 4E 61 6D 65 20 30 31 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' GPO -Contain57')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 06") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI1-Recore1')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 B5 70 81 B0 8F 01 51 90 81 90 D2 AB 9F D6 4D EB 30 A3 A0 1F C5 4A E6 EF 00 F8 B0 54 A5 53 A1 7A 2A F2 E9 6B 83 71 CA AB 9E 61 6E EA 73 B7 C6 BB 83 FE 83 8B CF 76 56 29 33 4C 85 10 5F 5C 08 55 16 F4 97 CA 74 39 9D D3 05 EA 4A 62 CC 56 63 C9 8E 9F 5D 86 3D 84 E1 53 A9 B0 FE 14 3E A8 E9 DA D3 F6 E2 DC 0D 8A 97 DF 26 A7 9A DF 81 F6 F0 1B A4 29 A8 FC 26 03 9E F5 74 27 27 24 16 51 8C E9 9D 73 3E EA EA 48 90 43 C4 A5 A8 F1 BB 55 17 BD 1A 3E 35 66 4A F4 61 C7 E7 78 92 14 95 BE 48 F2 C7 7F 93 C8 3F 9F C6 BF EB 72 30 01 F9 8E E7 23 9F 32 01 03 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand('Read Record SFI1-Recored2')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 70 81 9B 9F 46 81 80 A8 6F 37 63 77 22 02 36 1D 0B CA 5E 92 11 BA 95 F5 E1 CD B7 8F 8F 03 ED 77 49 25 E7 2B C9 CE 7D 0D C4 5F 42 BD 7C B3 8B 53 61 13 D0 9E 7F E8 5F EB 61 C1 EA 43 53 1F B2 97 8A 1A F1 59 97 D5 84 B7 BC 27 3D AB 8F 87 5F 06 72 50 09 1B AC AA E1 01 3B 33 F6 ED 7E A1 C8 73 2D 4D 63 A7 C6 F2 F9 77 C1 BD F9 0C 4F 74 96 E7 30 C4 58 5E EA EA 6A E6 81 C1 01 A8 B3 BE 14 A2 02 DD EB 22 65 43 DB 9F 47 03 01 00 01 9F 4A 01 82 9F 48 0A B4 C6 04 13 20 31 38 75 96 C7 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI2-Record1 -ContainPAN')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 06") and Result

if (Result):
	RetOfStep = DL.SendCommand(' Read Record SFI2-Record2')
	if (RetOfStep):
		Result = DL.Check_RXResponse("70 0A 9F 69 07 01 11 22 33 44 20 00 90 00") and Result

if (Result):
	RetOfStep = DL.SendCommand(' PT STOP')
	if (RetOfStep):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 2C 00 00 00 1C 9B") and Result