:: Run this script by double clicking on it in Windows explorer

@ECHO OFF
TITLE ApsimRun.py
:: Change 'data' to the directory where the .apsim file(s) that need to be run are located
:: ie "C:\Users\<user>\Documents\mydata"
CD data
"C:/Program Files (x86)/Apsim74-r2286/Model/ApsimRun.py"
