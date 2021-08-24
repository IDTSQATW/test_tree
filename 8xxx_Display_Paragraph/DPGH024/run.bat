@echo off 
Rem set default port
set PORT=1

Rem set DELAY=pause
set DELAY=ping -n 1 -w 5000 111.111.111.111

Rem enter comm port
echo.&set /p PORT=Please enter comm port to be used:
echo comm port set is %PORT% 
%DELAY%


Rem full screen
tp %PORT% 3999 0 0 0 0 1 2 3
Rem %DELAY%

Rem specified area
Rem tp %PORT% 3999 30 30 420 220 1 2 3
Rem %DELAY%


del DOCKLIGHT_LOG_hex.txt
test_1.pl
copy /Y DOCKLIGHT_LOG_hex.txt DPGH024_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt

