@ ECHO OFF

:: Set Variables
SET APSIMDIR="C:\Program Files (x86)\Apsim74-r2286"
SET SOILDIR=%APSIMDIR%\\UserInterface\\ToolBoxes
SET PYTHONDIR="C:\Python27\Lib\site-packages"
SET APSIMPACKAGE="apsimRegions"

:: Copy files to Apsim model directory
ROBOCOPY scripts\apsimRun %APSIMDIR%\\Model

:: Create a directory with the same name as the package and
:: copy all apsimRegions files to Python site-packages directory
MD %PYTHONDIR%\\%APSIMPACKAGE%
ROBOCOPY %APSIMPACKAGE% %PYTHONDIR%\\%APSIMPACKAGE% /S

:: Copy soil data to apsim toolbox directory
ROBOCOPY examples\\soils %SOILDIR% hc27_v1_1.soils

ECHO Installation complete!
PAUSE