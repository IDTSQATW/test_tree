@echo off 
del DOCKLIGHT_LOG_hex.txt
set var=test
%var%.pl
copy DOCKLIGHT_LOG_hex.txt UI_Flow6_hex.txt
remove_dates.pl DOCKLIGHT_LOG_hex.txt
