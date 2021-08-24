@echo off 

set scriptToRun=actTrans02-01M.pts

path=%PATH%C:\Program Files\FuH\Docklight Scripting V1.9\
path

Rem define Delay
set DELAY=ping -n 1 -w 5000 111.111.111.111
echo Start display Paragraph testing ...


DLcommTest.exe

Rem %DELAY%
Rem Docklight_Scripting.exe -r %scriptToRun%
