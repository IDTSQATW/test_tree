@echo off 
del DOCKLIGHT_LOG_hex.txt
set var=test
%var%.pl
copy DOCKLIGHT_LOG_hex.txt MF000100-4K_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt
