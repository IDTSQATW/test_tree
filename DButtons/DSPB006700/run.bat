@echo off 
del DOCKLIGHT_LOG_hex.txt
set var=test
%var%.pl
copy DOCKLIGHT_LOG_hex.txt DSPB006700_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt
