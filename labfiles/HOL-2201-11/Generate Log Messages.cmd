@echo off
setlocal enabledelayedexpansion
set logdir=c:\log
set logfile=APP-LOG.txt
echo.
echo.
echo **********************************************
echo    Adding lines; %logdir%\%logfile%
echo **********************************************
echo.
echo.

if not exist %logdir%\nul mkdir "%logdir%"

for /l %%a in (1,1,20) do ( 
		set /a rnd1 =!random!*10/32768
		set /a rnd2 =!random!*100/32768
		set /a rnd3 =!random!*1000/32768
		ping localhost -n 1>nul 2>&1
   for /l %%b in (0,1,10) do (
		if %%b geq 9  (
			set state=on
		) else if %%b leq 1 (
			set state=off
		) else (
			set state=unknown
		)
echo !rnd1!,!rnd2!,!rnd3!,batch=!random!,sub:%%a-%%b,status:!state!,%computername%,%userdomain%,%logonserver%,date:%date%,time:%time% >> "%logdir%\%logfile%" 
		set /a rnd1 =!random!*10/32768
		set /a rnd2 =!random!*100/32768
		set /a rnd3 =!random!*1000/32768
		ping -n 1 %computername%  >nul 2>&1
)
)


