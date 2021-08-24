' 
' This test script is to verify MAC Verification function from 2K file input 
'
 
set sh = CreateObject("WScript.Shell")

' Launch vp with com port 1
sh.Run ("vp.exe 1")

' Wait for the application to come up
WScript.Sleep 1000

' Select baudrate: 115200
sh.SendKeys "6{Enter}" 
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

' Select options on MAC generation & verification menu: Verification test
sh.SendKeys "3" 
WScript.Sleep 1000

' Select options on MAC generation menu: File Input
sh.SendKeys "2" 
WScript.Sleep 1000

' Enter User input
sh.SendKeys "macGenVer2kHex.txt{Enter}" 
WScript.Sleep 1000

