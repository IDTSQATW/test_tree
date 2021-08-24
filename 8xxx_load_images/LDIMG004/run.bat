@echo off 

Rem set default port
set PORT=1

Rem set DELAY=pause
set DELAY=ping -n 1 -w 5000 111.111.111.111

Rem enter comm port
echo.&set /p PORT=Please enter comm port to be used:
echo comm port set is %PORT% 
%DELAY%

download subwayLogo.png subwayLogo.png %PORT%
%DELAY%

download subwayLogo2.png subwayLogo2.png %PORT%
%DELAY%

Rem download subwayLogo3.png subwayLogo3.png %PORT%
Rem %DELAY%

download swImg01.png swImg01.png %PORT%
%DELAY%

download swImg02.png swImg02.png %PORT%
%DELAY%

download swImg03.png swImg03.png %PORT%
%DELAY%

download swImg04.png swImg04.png %PORT%
%DELAY%

del DOCKLIGHT_LOG_hex.txt
test_1.pl
copy /Y DOCKLIGHT_LOG_hex.txt LDIMG004_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt

