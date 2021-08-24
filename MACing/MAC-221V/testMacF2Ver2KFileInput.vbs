' 
' This test script is to verify MAC Ver function from 2K file input w/Format2 key
'
 
set sh = CreateObject("WScript.Shell")

' Launch vp with com port 1
sh.Run ("vp.exe 1")

' Wait for the application to come up
WScript.Sleep 1000

' Select baudrate: 9600
sh.SendKeys "3{Enter}" 
WScript.Sleep 1000

' Select Firmware: AR 2.1.3 or later
sh.SendKeys "2" 
WScript.Sleep 1000

' Select options on main menu: Master key operations
sh.SendKeys "4" 
WScript.Sleep 1000

' Select options on master session menu: M/S MAC Generation & Verification test
sh.SendKeys "c" 
WScript.Sleep 1000

' Select options on Key format for Format2
sh.SendKeys "2" 
WScript.Sleep 1000

' Select options on MAC gen & ver menu: MAC Gen/Ver test
sh.SendKeys "1" 
WScript.Sleep 1000

' Select options on MAC Ver menu: File Input
sh.SendKeys "6" 
WScript.Sleep 1000

' In put 1st MAC value:
sh.SendKeys "A2{Enter}" 
WScript.Sleep 1000

' In put 2nd MAC value:
sh.SendKeys "66{Enter}" 
WScript.Sleep 1000

' In put 3rd MAC value:
sh.SendKeys "EF{Enter}" 
WScript.Sleep 1000

' In put 4th MAC value:
sh.SendKeys "FE{Enter}" 
WScript.Sleep 1000

' Enter User input file
sh.SendKeys "macGenVer2kHex.txt{Enter}" 
WScript.Sleep 1000

