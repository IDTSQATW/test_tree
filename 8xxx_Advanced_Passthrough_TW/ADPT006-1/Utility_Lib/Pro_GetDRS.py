#Pro_GetDRS Py - Get Reader DRS
import sys
import time
import System

DRSCFG=[
	[
		['00','K81 Self Check Error'],
		['00','Normal'],
		['01','Error'],
		['FE','Tamper Case, not check Self check']
	],

	[
		['01','TM4 Check Value Error'],
		['00','Normal'],
		['01','Error'],
		['FE','TM4 command is not success, may be due to TM4 is not working, or tampered']
	],
				
	[
		['02','TM4 Slave Check Value Error'],
		['00','Normal'],
		['01','Error'],
		['FF','TM4 slave not present']
	],

	[
		['10','Battery'],
		['00','Normal'],
		['01','Battery low error'],
		['FE','not check']
	],

	[
		['11','Tamper Switch'],
		['Bit 0','Tamper Switch 0 (0-Normal, 1-Error)'],
		['Bit 1','Tamper Switch 1 (0-Normal, 1-Error)'],
		['Bit 2','Tamper Switch 2 (0-Normal, 1-Error)'],
		['Bit 3','Tamper Switch 3 (0-Normal, 1-Error)'],
		['Bit 4','Tamper Switch 4 (0-Normal, 1-Error)'],
		['Bit 5','Tamper Switch 5 (0-Normal, 1-Error)'],
		['Bit 6','Tamper Switch 6 (0-Normal, 1-Error)'],
		['Bit 7','Tamper Switch 7 (0-Normal, 1-Error)'],
		['FE','not check']
	],

	[
		['12','Temperature'],
		['00','Normal'],
		['01','Temperature High or Low'],
		['FE','not check']
	],

	[
		['13','Voltage'],
		['00','Normal'],
		['01','Voltage High or Low'],
		['FE','not check']
	],

	[
		['14', 'TM4 removal sensor'], 
		['00', 'Normal'],
		['01', 'TM4 sensor remove error'],
		['FE', 'not check']

	],

	[
		['15', 'K81 RTC TOF'], 
		['00', 'Normal'],
		['01', 'RTC time over flow error'],
		['FE', 'not check']
	],

	[
		['16', 'K81 clock CTF'], 
		['00', 'Normal'],
		['01', 'Clock frequency out of range'],
		['FE', 'not check']
	],

	[
		['1F', 'Other(Reserved2)'], 
		['FF', 'not check']
	]
]

class Pro_GetDRS:
	def Run(self, DL):
		Result = True
		RetOfStep = True
		CatchFlag = False
		listx = ['xx', 'xx', 'xx']
		if Result:
			DL.SendIOCommand('IDG', "C7 3A", 3000)
			strResponse = DL.Get_RXResponse(0)
			strResponse = strResponse.replace(" ", "")
			strResponse = strResponse.upper()
			if len(strResponse) > 32:
				strResponse = strResponse[28:len(strResponse) - 4]
				DL.setText("GREEN", 'DRS' + strResponse + '-OK')
				lenx = len(strResponse)
				i = 0
				for j in range(0, lenx / 6):
					CatchFlag = False
					listx[0] = strResponse[i:2 + i]
					listx[1] = strResponse[2 + i:4 + i]
					listx[2] = strResponse[4 + i:6 + i]
					i = i + 6
					item = 0
					for list in DRSCFG:
						if list[0][0] == listx[0]:
							DL.setText("BLACK", list[0][1] + ":" + listx[2])
							if listx[0] != '11':
								for k in range(1, len(list)):
									if listx[2] == list[k][0]:
										DL.setText("GREEN", '[' + list[k][1] + ']')
										CatchFlag = True
										break
							else:
								if '00' == listx[2]:
									DL.setText("GREEN", '[No Tampered]')
								itamper = int(listx[2], 16)
								if itamper & 1:
									DL.setText("GREEN", '[' + list[1][1] + ']')
								if itamper & 2:
									DL.setText("GREEN", '[' + list[2][1] + ']')
								if itamper & 4:
									DL.setText("GREEN", '[' + list[3][1] + ']')
								if itamper & 8:
									DL.setText("GREEN", '[' + list[4][1] + ']')
								if itamper & 16:
									DL.setText("GREEN", '[' + list[5][1] + ']')
								if itamper & 32:
									DL.setText("GREEN", '[' + list[6][1] + ']')
								if itamper & 64:
									DL.setText("GREEN", '[' + list[7][1] + ']')
								if itamper & 128:
									DL.setText("GREEN", '[' + list[8][1] + ']')
								CatchFlag = True
						if CatchFlag == False:
							DL.setText("GREEN", '[Unknown]')
							CatchFlag = True
		return Result and CatchFlag