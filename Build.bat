@ECHO OFF
REM This is for satefy. Do NOT remove.
CD /d %~dp0

REM ~~~
ECHO TamrielCraftPack Auto Build
ECHO ===
ECHO #
SET "file_copy=assets Changelog.txt pack.mcmeta pack.png"
SET "optifine_disables= foliage\reeds foliage\sand_snow glass\1.png glass\glass_white.properties random\cauldron random\dragonegg stone\orange_concrete stone\stone_pillar"
REM ~~~

FOR /f "delims=" %%a IN ('DIR /s /b %~dp0Excalibur*.zip') DO SET "ex_name=%%~na"

REM ~~~
IF EXIST %~dp0%ex_name% (
	ECHO %~dp0%ex_name% Already exists...
	ECHO Deleting ...%ex_name%
	RD /S /Q %~dp0%ex_name%
	ECHO #
)

ECHO Extracting Archive %~dp0%ex_name%.zip
POWERSHELL Expand-Archive %~dp0%ex_name%.zip
ECHO #

REM ~~~
ECHO Copying files
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
POWERSHELL Compress-Archive -Path %~dp0%ex_name%\* -DestinationPath %~dp0TCP.zip -Force
ECHO #

ECHO DONE.
PAUSE
