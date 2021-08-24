@echo off 

Rem set default port
set PORT=1

Rem set DELAY=pause
set DELAY=ping -n 1 -w 5000 111.111.111.111

Rem enter comm port
echo.&set /p PORT=Please enter comm port to be used:
echo comm port set is %PORT% 
%DELAY%

download hdLogo1.png hdLogo1.png %PORT%
%DELAY%

download hdLogo.png hdLogo.png %PORT%
%DELAY%

download hdCoupon.png hdCoupon.png %PORT%
%DELAY%


del DOCKLIGHT_LOG_hex.txt
test_1.pl
copy /Y DOCKLIGHT_LOG_hex.txt LDIMG003_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt

