@echo off

REM echo Setting power plan to 'High Performance'...
REM powercfg -s 432ad5c6-b993-416e-bdd5-0e797acb78c5

set arcpy=C:\Python27\ArcGIS10.2\python.exe
set intel=C:\Users\putzr\anaconda3\python.exe

IF %1 == 0 %arcpy% .\main.py
IF %1 == 1 %intel% .\model\main.py