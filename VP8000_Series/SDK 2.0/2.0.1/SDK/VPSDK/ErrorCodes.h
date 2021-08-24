//=============================================================================
//
// File Name
// 
//    ErrorCodes.h
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


#ifndef ERRORCODES_H_
#define ERRORCODES_H_


//=============================================================================
// ViVOpay READER LOW LEVEL ERROR STATES
//=============================================================================
#define ERR_OK										0x00
#define ERR_INCORRECT_FRAME_HEADER_TAG				0x01
#define ERR_INCORRECT_FRAME_TYPE_UNKNOWN_COMMAND	0x02
#define ERR_UNKNOWN_FRAME_TYPE_SUB_COMMAND			0x03
#define ERR_UNKNOWN_COMMAND_CRC_ERROR				0x04
#define ERR_UNKNOWN_SUB_COMMAND_INCORRECT_PARAMETER	0x05
#define ERR_CRC_ERROR_PARAMETER_NOT_SUPPORTED		0x06
#define ERR_FAILED_MALFORMED_DATA					0x07
#define ERR_TIMEOUT									0x08
#define ERR_INCORRECT_PARAMETER_FAILED_NACK			0x0A
#define ERR_COMMAND_NOT_SUPPORTED_NOT_ALLOWED		0x0B
#define ERR_SUB_COMMAND_NOT_SUPPORTED_NOT_ALLOWED	0x0C
#define ERR_PARAMETER_NOT_SUPPORTED_BUFFER_OVERFLOW	0x0D
#define ERR_USER_INTERFACE_EVENT					0x0E
#define ERR_REQUEST_ONLINE_AUTHORIZATION			0x23

//=============================================================================
// SDK Error Codes
//=============================================================================
#define ERR_NO_DATA_TO_READ							0xA0
#define ERR_DATA_CANNOT_WRITE						0xA1
#define ERR_DEVICE_CANNOT_OPEN						0xA2
#define	ERR_DEVICE_CANNOT_CLOSE						0xA3
#define ERR_DEVICE_CLOSED							0xA4
#define ERR_INVALID_DATA_FROM_DEVICE				0xA5
#define ERR_RESPONSE_TIMEOUT						0xA6
#define ERR_RECEIVE_DATA_CRC_ERROR					0xA7
#define ERR_SYSTEM_ERROR							0xA8
#define ERR_INPUT_PARAMETER_INVALID					0xA9
#define ERR_EVENT_NOTIFICATION_ALREADY_REGISTERED	0xAA
#define ERR_EVENT_NOTIFICATION_NOT_REGISTERED		0xAB
#define ERR_ILLEGAL_BUTTON_CAPTION					0xAC
#define ERR_REQUIRED_DATA_NOT_AVAILABLE				0xAD
#define ERR_CANNOT_FREE_MEMORY						0xAE
#define ERR_RESPONSE_REDIRECTED_TO_CALLBACK			0xAF
#define ERR_NO_EVENT_NOTIFICATION_TO_UNREGISTER		0xB0
#define ERR_DEVICE_BUSY								0xB1
#define ERR_CANNOT_PERFORM_SEARCH					0xB2




#endif  //ERROR_CODES_H
