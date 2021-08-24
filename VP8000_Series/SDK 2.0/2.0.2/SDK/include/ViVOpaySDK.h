//=============================================================================
//
// File Name
// 
//    ViVOpaySDK.h
//
// Description
//
//                                                      
//
// COPYRIGHT (c) 2009 ViVOtech, Inc.
// All rights reserved.
//                                                                         
//=============================================================================
//
// Revision History
//
// Date        Author   Change
// ----------  ------   -------------------------------------------------------
// 
//
// 
//=============================================================================


#ifndef __VPSDKINTERFACE_H
#define __VPSDKINTERFACE_H

#ifdef __cplusplus
 extern "C" {
#endif

#define VIVOAPI __stdcall 


typedef DWORD StatusCode;		//status or errors
typedef DWORD ControlID;
typedef DWORD EventType;
typedef DWORD DeviceCatagory;

//=============================================================================
// Enum Definitions
//=============================================================================

typedef enum _DeviceModel
{
	VP8600		=	0x00,
	VP8800		=	0x01

} DeviceModel;

typedef enum _Polling
{
	POLL_AUTO		=	0x00,
	POLL_ON_DEMAND	=	0x01

} Polling;

typedef enum _Events
{

	EVENT_NONE = 0,
	EVENT_MSR_GOOD_SWIPE,	
	EVENT_PIN_SUCCESS,												
	
	
	EVENT_SIG_DATA,
	EVENT_PIN_CANCEL,
	EVENT_BUTTON_CLICK,
	EVENT_PIN_FAILURE,
	EVENT_MSR_BAD_SWIPE,
	EVENT_CHECKBOX_CHECK,
	EVENT_CHECKBOX_UNCHECK,
	EVENT_RADIO_BUTTON_CLICK,
	EVENT_ERROR_EVENT,

	EVENT_KEYPAD_ENTER,
	EVENT_KEYPAD_CANCEL,
	EVENT_KEYPAD_CLEAR,
	EVENT_KEYPAD_1,
	EVENT_KEYPAD_2,
	EVENT_KEYPAD_3,
	EVENT_KEYPAD_4,
	EVENT_KEYPAD_5,
	EVENT_KEYPAD_6,
	EVENT_KEYPAD_7,
	EVENT_KEYPAD_8,
	EVENT_KEYPAD_9,
	EVENT_KEYPAD_0,

	EVENT_TIMEOUT

} Events;

typedef enum _LEDPanel
{
	LED_0	=	0x00,
	LED_1	=	0x01,
	LED_2	=	0x02,
	LED_3	=	0x03,
	LED_All =	0xFF

}LEDPanel;

typedef enum _Beeper
{
	BEEP_No				= 0x00,
	BEEP_OneShort		= 0x01,
	BEEP_TwoShort		= 0x02, 
	BEEP_ThreeShort		= 0x03,
	BEEP_FourShort		= 0x04,
	BEEP_OneLong_200ms	= 0x05,
	BEEP_OneLong_400ms	= 0x06,
	BEEP_OneLong_600ms	= 0x07,
	BEEP_OneLong_800ms	= 0x08

}Beeper;


typedef enum _Unit
{
	Firmware = 0x00,
	Bootloader = 0x01,
	SDK = 0x02

}Unit;

typedef enum _Module
{
	ALL_READER_VARIABLES			=		0x00,
	PRODUCT_TYPE					=		0x01,
	PROCESSOR_TYPE					=		0x02,
	MAIN_FIRMWARE_VERSION			=		0x03,
	FIRMWARE_SUBSYSTEM_SUITE		= 		0x04,
	SERIAL_PROTOCOL_SUITE			=		0x06,
	LAYER_1_PAYPASS_VERSION			=		0x07,
	LAYER_1_ACR_VERSION				=		0x08,
	LAYER_2_CARD_APPLICATION_SUITE	= 		0x0A,
	USER_EXPERIENCE_SUITE			= 		0x0C,
	SYSTEM_INFORMATION_SUITE		= 		0x0E,
	PATCH_VERSION_NUMBER			= 		0X0F

}Module;

typedef enum _CardType
{
	TypeA = 0x01,
	TypeB = 0x02

}CardType;

typedef enum _CardInformation
{
	Track1Available = 0x01,
	Track2Available = 0x02,
	Track3Available = 0x04,

	SwipeCard		= 0x80

}CardInformation;

typedef enum _SigFormat
{
	Bitmap = 1,
	Png = 2,
	Raw  = 3

}SigFormat;

typedef enum _DisplayProperties
{
	ClearScreen = 1,			// Any of fallowing values can be "OR" ed.
	DisplayCenterAtY = 0,
	DisplayAtXY  = 2,
	DisplayCenterOnScreen = 4

}DisplayProperties;


typedef enum _CheckState
{
	Checked = 1,
	Unchecked = 0

}CheckState;


typedef enum _SigAreaFormat
{
	DrawBox = 1,
	DrawLine = 2

}SigAreaFormat;

typedef enum _ListProperties				// Any of fallowing values can be "OR" ed.
{
	ShowVerticalScrollArrow = 1,			
	DrawListItemBorder		= 2,			
	DrawScrollArrowBorder	= 4,			
	EnableTouchSensitivity  = 8,			
	EnableAutoScroll		= 16			

}ListProperties; 


typedef enum _InputFieldProperties
{
	NoBorder = 0,
	ShowBorder = 1

}InputFieldProperties;


typedef enum _MessageDisplayProperties
{
	AlignCenter = 0,
	AlignRight = 2

}MessageDisplayProperties;


//=============================================================================
// Structure Definitions
//=============================================================================


typedef struct _StructInfo
{
	DWORD dwStructrueID;
    DWORD dwAllocated;
    DWORD dwUsed;

} StructInfo;


typedef struct _Data
{
	StructInfo	StructInfo;
	DWORD       dwDataBuffSize;
	LPBYTE      lpDataBuff;

}Data;

typedef struct _Image		//currently not in use
{
	char* path;

} Image;

typedef struct _Color
{
	unsigned char red;
	unsigned char green;
	unsigned char blue;

}Color;

typedef struct _Appearance
{
	int x;
	int y;
	int width;
	int height;
	Color backcolor;
	Image backgroundImage;

} Appearance;

typedef struct _Font
{
	int type;
	int size;
	Color color;

}Font;

typedef struct _ButtonOptions
{
	DisplayProperties displayProperties;

}ButtonOptions;

typedef struct _TextBoxOptions
{
	DisplayProperties displayProperties;

}TextBoxOptions;

typedef struct _AmountBoxOptions
{
	DisplayProperties displayProperties;

}AmountBoxOptions;

typedef struct _CheckBoxOptions
{
	Color foreColor;
	CheckState checkedState;

}CheckBoxOptions;

typedef struct _SignatureOptions
{
	Color foreColor;
	SigFormat sigFormat;
	SigAreaFormat areaFormat;

}SignatureOptions;

typedef struct _ListOptions
{
	int columnCount;
	int rawCount;
	ListProperties listProperties;

}ListOptions;

typedef struct _InputFieldOptions
{
	Color borderColor;
	InputFieldProperties inputFieldProperties;

}InputFieldOptions;

typedef struct _ReaderOptions
{
	Color logoForeColor;
	Color logoBackColor;
	Font topmsgFont;
	Color topmsgBackColor;
	MessageDisplayProperties topmsgDisplayProperties;
	char* topmsg;
	Font bottommsgFont;
	Color bottommsgBackColor;
	MessageDisplayProperties bottommsgDisplayProperties;
	char* bottommsg;

}ReaderOptions;

typedef struct _PINOptions
{
	Color foreColor;
	Color backColor;

}PINOptions;

typedef struct _TrackData
{
	StructInfo	StructInfo;
	Data Track1;
	Data Track2;
	Data Track3;
	Data DiscretionaryData;

}TrackData;


//=============================================================================
// Function Definitions
//=============================================================================


typedef void (*ONEVENT) (Events event);

StatusCode VIVOAPI System_SearchForDevice(char* deviceCatagory , char* devicePath[]); 
StatusCode VIVOAPI System_OpenDevice(char* devicePath);
StatusCode VIVOAPI System_CloseDevice();
StatusCode VIVOAPI System_Ping();
StatusCode VIVOAPI System_FreeMemory(void* pVoid);
StatusCode VIVOAPI System_SetBaudRate(int baudRate);
StatusCode VIVOAPI System_DirectIOCall(unsigned char* data, int dataLength, Data* responseData, unsigned int responseTimeout);
StatusCode VIVOAPI System_GetLastErrorCode();
StatusCode VIVOAPI System_GetLastExtendedErrorCode();	
const char*  VIVOAPI System_GetLastErrorInformation();	
StatusCode VIVOAPI System_SetColor(Color foreColor, Color backColor);
StatusCode VIVOAPI System_SetDefaultParameters();
StatusCode VIVOAPI System_RegisterEventCallback(ONEVENT callbackFunction);
StatusCode VIVOAPI System_UnRegisterEventCallback();
StatusCode VIVOAPI System_EnableCustomDisplayMode(BOOL doEnable);
StatusCode VIVOAPI System_SetBuzzerAndLED(Beeper beepStyle, LEDPanel LEDNumber, BOOL doLEDOn);
StatusCode VIVOAPI System_SetLED(LEDPanel LEDNumber, BOOL doLEDOn);
StatusCode VIVOAPI System_SetBuzzer(Beeper beepStyle);
StatusCode VIVOAPI System_GetVersion(Unit unitForVersion, Data* version);
StatusCode VIVOAPI System_GetSerialNumber(Data* serialNumber);
StatusCode VIVOAPI System_GetModuleInformation(Module module, Data* moduleInformation);
StatusCode VIVOAPI System_CancelTransaction();
StatusCode VIVOAPI System_SetPollingMode(Polling pollingMode);
StatusCode VIVOAPI System_EnableAntenna(BOOL doEnable);
StatusCode VIVOAPI System_ResetToInitialState();
StatusCode VIVOAPI System_RebootDevice();
StatusCode VIVOAPI System_EnterBootloaderMode();
StatusCode VIVOAPI System_ContinueBootup();
StatusCode VIVOAPI System_UpgradeFirmware(char* filePath);

StatusCode VIVOAPI Passthrough_StartMode(BOOL doStart);
StatusCode VIVOAPI Passthrough_PollForToken(int timeOutMS, Data* tokenInfomation);
StatusCode VIVOAPI Passthrough_ExchangeContactlessData(unsigned char* apduCommand, int apduCommandLength,  Data* responseApdu);
StatusCode VIVOAPI Passthrough_ExchangePCDSingleCommand(unsigned char* data, int dataLength,  Data* responseData);
StatusCode VIVOAPI Passthrough_GetPCDPICCParameters(Data* responseData);
StatusCode VIVOAPI Passthrough_ExecuteEnhancedMode(unsigned char* command, int commandLength);
StatusCode VIVOAPI Passthrough_AuthenticateMifareBlock(unsigned char block, unsigned char keyType, unsigned char* key);
StatusCode VIVOAPI Passthrough_ReadMifareBlocks(unsigned char cardAndBlockCount, unsigned char startBlock, Data* readData);
StatusCode VIVOAPI Passthrough_WriteMifareBlocks(unsigned char cardAndBlockCount, unsigned char startBlock, unsigned char* writeData, int writeDataLength);
StatusCode VIVOAPI Passthrough_ExecuteMifareEpurse(unsigned char mode, unsigned char* purseFunctionBlocks, int purseFunctionBlocksLength);
StatusCode VIVOAPI Passthrough_Halt(CardType cardType); 

StatusCode VIVOAPI GUI_DisplayButton(Appearance appearance, Font font, ButtonOptions options, char* caption, ControlID* controlID);
StatusCode VIVOAPI GUI_DisplayText(Appearance appearance, Font font, TextBoxOptions options, char* label, ControlID* controlID);
StatusCode VIVOAPI GUI_ChangeText(ControlID controlID, char* label);
StatusCode VIVOAPI GUI_DisplayAmount(Appearance appearance, Font font, AmountBoxOptions options, char* currency, char* amount, ControlID* controlID);
StatusCode VIVOAPI GUI_ChangeAmount(ControlID controlID, char* currency, char* amount);
StatusCode VIVOAPI GUI_DisplayCheckBox(Appearance appearance, CheckBoxOptions options, ControlID* controlID);
StatusCode VIVOAPI GUI_ClearDisplay();
StatusCode VIVOAPI GUI_ClearEventQueue();
StatusCode VIVOAPI GUI_EnableTouchSensitivity(ControlID controlID, BOOL doEnable);
StatusCode VIVOAPI GUI_GetInputEvent(int timeout, EventType* eventType, ControlID* controlID);
StatusCode VIVOAPI GUI_GetInputEventData(BOOL doFlush, ControlID* controlID, Data* eventData);		

StatusCode VIVOAPI SIG_DisplayBuiltInScreen(int timeout, SigFormat sigFormat);
StatusCode VIVOAPI SIG_GetBuiltInScreenData(BOOL doFlush, Data* signatureData);	
StatusCode VIVOAPI SIG_DisplayCustomControl(Appearance appearance, SignatureOptions  options, ControlID* controlID);
StatusCode VIVOAPI SIG_GetCustomControlData(ControlID controlID, Data* signatureData);
StatusCode VIVOAPI SIG_Clear(ControlID controlID);

StatusCode VIVOAPI List_Create(Appearance appearance, Font font, ListOptions  options, ControlID* controlID);
StatusCode VIVOAPI List_AddItem(ControlID controlID, char* displayText, char* returnTextOnSelection, BOOL isSelected);
StatusCode VIVOAPI List_Delete(ControlID controlID);
StatusCode VIVOAPI List_GetSelectedItem(ControlID controlID, Data* returnTextOnSelection);	
StatusCode VIVOAPI List_GetInformation(ControlID controlID, Data* listInformation);	

StatusCode VIVOAPI Inputfield_Create(Appearance appearance, Font font, InputFieldOptions  options, char* preFillText, char* formatText, ControlID* controlID);
StatusCode VIVOAPI Inputfield_GetValue(ControlID controlID, Data* value);
StatusCode VIVOAPI Inputfield_Clear(ControlID controlID);	

StatusCode VIVOAPI Payment_ActivateTransaction(int timeout, unsigned char* transactionData, int transactionDataLength, ReaderOptions options);
StatusCode VIVOAPI Payment_GetCardData(BOOL doFlush, TrackData* trackData);	
StatusCode VIVOAPI Payment_FlushTrackData();
StatusCode VIVOAPI Payment_UpdateBalance(unsigned char statusCode, unsigned char* transactionData, int transactionDataLength, Data* responseTransactionData);
StatusCode VIVOAPI Payment_GetTransactionResult(TrackData* trackData);	
StatusCode VIVOAPI Payment_GetFullTrackData(unsigned char* cardInformation, TrackData* trackData);

StatusCode VIVOAPI MXI_ActivateTransaction(int timeout, unsigned char* transactionData, int transactionDataLength);
StatusCode VIVOAPI MXI_GetCardData(BOOL doFlush, Data* responseTransactionData); 
StatusCode VIVOAPI MXI_WriteDebit(unsigned char* transactionData, int transactionDataLength, Data* responseTransactionData);	
StatusCode VIVOAPI MXI_WriteData(unsigned char* ticket, int ticketLength);	

StatusCode VIVOAPI Security_DisplayDUKPTPinEntryScreen(int timeout, unsigned char* accountNo, int accountNoLength, PINOptions options);
StatusCode VIVOAPI Security_DisplayMasterSessionPinEntryScreen(int timeout, unsigned char* accountNo, int accountNoLength, unsigned char* workingKey, int workingKeyLength, PINOptions options);
StatusCode VIVOAPI Security_GetPinData(BOOL doFlush, Data* pinData);
StatusCode VIVOAPI Security_CheckMasterKeysPresent(unsigned int* masterKeyLocations);	 
StatusCode VIVOAPI Security_GetMasterKeyInformation(unsigned char masterKeyLocation, Data* masterKeyInformation);	//chkMasterKeyRequest
StatusCode VIVOAPI Security_SelectMasterKey(unsigned char masterKeyLocation);
StatusCode VIVOAPI Security_ReturnMasterKeyInUse(unsigned int* masterKeyLocation);
StatusCode VIVOAPI Security_SetCAPublicKey(unsigned char* CAPublicKeyData, int CAPublicKeyDataLength);
StatusCode VIVOAPI Security_DeleteCAPublicKey(unsigned char* RIDKeyIndex, int RIDKeyIndexLength);
StatusCode VIVOAPI Security_DeleteAllCAPublicKeys();

StatusCode VIVOAPI AID_SetConfiguration(unsigned char* configurationData, int configurationDataLength);
StatusCode VIVOAPI AID_GetConfiguration(Data* configurationData);
StatusCode VIVOAPI AID_SetConfigurableAID(unsigned char* configurableData, int configurableDataLength);
StatusCode VIVOAPI AID_SetConfigurableGroup(unsigned char* configurableData, int configurableDataLength);
StatusCode VIVOAPI AID_GetConfigurableAID(unsigned char* command, int commandLength,  Data* responseConfigurableData);
StatusCode VIVOAPI AID_GetConfigurableGroup(unsigned char* command, int commandLength,  Data* responseConfigurableData);
StatusCode VIVOAPI AID_DeleteConfigurableAID(unsigned char* applicationIdentifier, int applicationIdentifierLength);
StatusCode VIVOAPI AID_DeleteConfigurableGroup(unsigned char* group, int groupLength);
StatusCode VIVOAPI AID_GetAllAIDs(Data* applicationIdentifier);
StatusCode VIVOAPI AID_GetAllGroups(Data* group);

#ifdef __cplusplus
 }
#endif

#endif		// __VPSDKINTERFACE_H