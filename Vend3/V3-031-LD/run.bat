@echo off 

Rem set default port
set PORT=1

Rem set DELAY=pause
set DELAY=ping -n 1 -w 5000 111.111.111.111

Rem enter comm port
echo.&set /p PORT=Please enter comm port to be used:
echo comm port set is %PORT% 
%DELAY%


download lcdalloff128-64.bmp lcdalloff128-64.bmp %PORT%
%DELAY%

download lcdchecker128-64.bmp lcdchecker128-64.bmp %PORT%
%DELAY%


del DOCKLIGHT_LOG_hex.txt
test_1.pl
copy /Y DOCKLIGHT_LOG_hex.txt V3-031-LD_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt
