#Pro_MSRData Py - excuse original txt format
import sys

CAPTURE_ENCODE_TYPE_ISOABA = 0
CAPTURE_ENCODE_TYPE_AAMVA = 1
CAPTURE_ENCODE_TYPE_Other = 2
CAPTURE_ENCODE_TYPE_Raw = 3
CAPTURE_ENCODE_TYPE_JisI_II = 4
CAPTURE_ENCODE_TYPE_UNKNOWN = 5

class cardFiled:
	cardType = 0x80;
	track1MaskData = "";
	track2MaskData = "";
	track3MaskData = "";
	track1ClearData = "";
	track2ClearData = "";
	track3ClearData = "";
	track1EncrytionData = "";
	track2EncrytionData = "";
	track3EncrytionData = "";

class Pro_MSRData:
	Key="0123456789abcdeffedcba9876543210"
	PAN=''
	CompairEncryptType=0;
	CompairEncryptMode=1;

	#global Card4909
	#global AAMVA
	#global Standard 
	#global NEOIICard4909 
	Card4909 = cardFiled()
	AAMVA = cardFiled()
	Standard = cardFiled()
	NEOIICard4909=cardFiled()

	Card4909.track1MaskData="%*4547**3*****0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
	Card4909.track2MaskData=";4547**3*****0000=1102***************?*"
	Card4909.track3MaskData=";0145474*******0000=*********************************1102**********************************************?*"
	Card4909.track1ClearData="%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?."
	Card4909.track2ClearData=";4547570001070000=1102101000003060000?8"
	Card4909.track3ClearData=";014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?5"

	AAMVA.track1MaskData="%NYNEW YORK^LEEABCDEFGHI$BRUCEABCDEFGHJRABCDEFG655 N. BERRY ST., #K^?!"
	AAMVA.track2MaskData=";636014028898856=1011196399280123=?<";
	AAMVA.track3MaskData="%##92821-00440AABBBBBBBBBBTTTTF507125BRWBLK0123456789                CCCCCCSSSS?V";

	Standard.track1MaskData="%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?C"
	Standard.track2MaskData=";2121212121767676070707767676762121212?0";
	Standard.track3MaskData=";33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?2";

	NEOIICard4909.track1MaskData="%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
	NEOIICard4909.track2MaskData=";4547********0000=1102***************?*"
	NEOIICard4909.track3MaskData=";014547********0000=***********************************************************************************?*"
	NEOIICard4909.track1ClearData="%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?."
	NEOIICard4909.track2ClearData=";4547570001070000=1102101000003060000?8"
	NEOIICard4909.track3ClearData=";014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?5"
 