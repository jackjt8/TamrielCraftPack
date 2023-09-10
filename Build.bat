@ECHO OFF
REM This is for satefy. Do NOT remove.
CD /d %~dp0

REM ~~~
ECHO TamrielCraftPack Auto Build
ECHO ===
ECHO #
SET "file_copy=Changelog.txt extras.txt pack.mcmeta pack.png"
SET "optifine_disables= foliage\reeds foliage\sand_snow glass\white random\cauldron stone\orange_concrete stone\stone_brick_pillar"
REM ~~~

REM Find and set Excalibur and Excalibur Extras
FOR /f "delims=" %%a IN ('DIR /s /b %~dp0Excalibur*.zip') DO SET "ex_name=%%~na"
FOR /f "delims=" %%a IN ('DIR /s /b %~dp0Excalibur_Extras*.zip') DO SET "exextras_name=%%~na"

IF "%ex_name%"=="" (GOTO :notdefined)
IF "%exextras_name%"=="" (GOTO :notdefined)

REM ~~~
REM Safety Check
IF EXIST %~dp0%ex_name% (
	ECHO %~dp0%ex_name% Already exists...
	ECHO Deleting ...%ex_name%
	RD /S /Q %~dp0%ex_name%
	ECHO #
)
IF EXIST %~dp0%exextras_name% (
	ECHO %~dp0%exextras_name% Already exists...
	ECHO Deleting ...%exextras_name%
	RD /S /Q %~dp0%exextras_name%
	ECHO #
)

REM Expand Archives
ECHO Extracting Archive %~dp0%ex_name%.zip
POWERSHELL Expand-Archive %~dp0%ex_name%.zip
ECHO #

ECHO Extracting Archive %~dp0%exextras_name%.zip
POWERSHELL Expand-Archive %~dp0%exextras_name%.zip
ECHO #

REM ~~~
ECHO Copying files
REM Do exextra >>> ex
XCOPY /Y /S /Q %~dp0%exextras_name%\assets %~dp0%ex_name%\assets
REM Do TCP >>> ex+exextra
XCOPY /Y /S /Q %~dp0\assets %~dp0%ex_name%\assets
(FOR %%a IN (%file_copy%) DO (
	XCOPY /Y /Q %~dp0%%a %~dp0%ex_name%
))
ECHO #

REM ~~~
REM Debloat
ECHO Removing unneeded terrain.png
DEL %~dp0%ex_name%\terrain.png
ECHO #

REM ~~~
ECHO Disabling OptiFine Features
(FOR %%b in (%optifine_disables%) DO (
	DEL /Q "%~dp0%ex_name%\assets\minecraft\optifine\ctm\%%b"
))
ECHO #

REM ~~~
REM Excluded root archive creation
ECHO Compressing Archive
IF EXIST %~dp0TCP_dev.zip (
	DEL /Q %~dp0TCP_dev.zip
)
"C:\Program Files\7-Zip\7z.exe" a "%~dp0TCP_dev.zip" "%~dp0%ex_name%\*"

ECHO #

ECHO Cleanup
IF EXIST %~dp0%ex_name% (
	ECHO Removing folder %ex_name%
	RD /S /Q %~dp0%ex_name%
	ECHO #
)
IF EXIST %~dp0%exextras_name% (
	ECHO Removing folder %~dp0%exextras_name%
	RD /S /Q %~dp0%exextras_name%
	ECHO #
)

ECHO DONE.
PAUSE
EXIT /B

:notdefined
ECHO ex or exextra are NOT defined
PAUSE
EXIT /B
