@echo off
REM ======================================
REM 2012.02.12 by gsyan
REM
REM 2012.02.13 updated
REM ======================================

REM get the CurrenDirectory
REM 依是否帶有括號,擷取出目錄名稱
set currentDirQuoted=%0
set currentDirQuoted=%currentDirQuoted:~1,-18%
set currentDirNoQuoted=%0
set currentDirNoQuoted=%currentDirNoQuoted:~0,-17%

REM get the apk filename
REM 依是否帶有括號,擷取出 apk 去掉副檔名以後的路徑
set filenameQuoted=%1
set filenameQuoted=%filenameQuoted:~1,-5%
set filenameNoQuoted=%1
set filenameNoQuoted=%filenameNoQuoted:~0,-4%

set notquoted=%0
set notquoted=%notquoted:~1,-1%
IF %0=="%notquoted%" (
   REM 有括號的
   set jar="%currentDirQuoted%\signapk.jar" "%currentDirQuoted%\certificate.pem" "%currentDirQuoted%\key.pk8"
) ELSE (
   REM 無括號的
   REM set CD=%0
   REM set CD=%CD:~1,-17%
   REM set jar=%CD%\signapk.jar %CD%\certificate.pem %CD%\key.pk8
   set jar=%currentDirNoQuoted%\signapk.jar %currentDirNoQuoted%\certificate.pem %currentDirNoQuoted%\key.pk8
)

set notquoted=%1
set notquoted=%notquoted:~1,-1%
IF %1=="%notquoted%" (
   REM 有括號的
   set apk="%filenameQuoted%.apk"  "%filenameQuoted%-new.apk"
) ELSE (
   REM 無括號的
   set apk=%filenameNoQuoted%.apk  %filenameNoQuoted%-new.apk
)


REM ressign the apk
java -jar %jar% %apk%

@echo.
