@echo off 

Rem set default port
set PORT=1

Rem set DELAY=pause
set DELAY=ping -n 1 -w 5000 111.111.111.111

Rem enter comm port
echo.&set /p PORT=Please enter comm port to be used:
echo comm port set is %PORT% 
%DELAY%


download mono_30x24.png mono_30x24.png %PORT%
%DELAY%

download mono_30x24.bmp mono_30x24.bmp %PORT%
%DELAY%

download mono_33x26.png mono_33x26.png %PORT%
%DELAY%

download mono_33x26.bmp mono_33x26.bmp %PORT%
%DELAY%

download mono_32x27.png mono_32x27.png %PORT%
%DELAY%

download mono_32x27.bmp mono_32x27.bmp %PORT%
%DELAY%

del DOCKLIGHT_LOG_hex.txt
test_1.pl
copy /Y DOCKLIGHT_LOG_hex.txt V3-025-LD_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt

