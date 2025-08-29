@echo OFF

rem Force l'utilisation West European Latin
chcp 1252 > nul

rem Inclut le repertoire binaire powershell dans le path
set PATH_PYTHON=C:\Users\Jdoe\AppData\Local\Programs\Python\Python311\
set PATH=%PATH_PYTHON%;%PATH%

call submit_aff.bat %*
echo _______________________________________________________________________
echo Debut de l'execution ...
date /T
echo %time:~+0,8%
echo _______________________________________________________________________

rem Mode TEST
if "%TOM_JOB_EXEC%" == "TEST" (
	echo Job execute en mode TEST
	%ABM_BIN%\tsend -sT -r0 -m"Traitement termine (mode TEST)"
	%ABM_BIN%\vtgestlog
	goto FIN
)

set JOBNAME=%1
set ACTION=%2
set BACKUP_TYPE=%3

if "%ACTION%" == "START" (
	if "%BACKUP_TYPE%" == "FULL" (
		echo FULL BACKUP
		call :LAUNCH %JOBNAME% --start --full
	) else if "%BACKUP_TYPE%" == "INCR" (
		echo INCREMENTAL BACKUP
		call :LAUNCH %JOBNAME% --start
) else if "%ACTION%" == "STOP" (
		echo ENABLE JOB
		call :LAUNCH %JOBNAME% --stop		
) else if "%ACTION%" == "ENABLE" (
		echo ENABLE JOB
		call :LAUNCH %JOBNAME% --enable
) else if "%ACTION%" == "DISABLE" (
		echo DISABLE JOB
		call :LAUNCH %JOBNAME% --disable
) else if "%ACTION%" == "STATUS" (
		echo JOB STATUS
		call :LAUNCH %JOBNAME% --status
echo.

:LAUNCH
echo Lancement du script de sauvegarde Veeam
echo %PATH_PYTHON%\python %ABM_BIN%\veeam.py %*
%PATH_PYTHON%\python %ABM_BIN%\veeam.py %*
set RETCODE=%ERRORLEVEL%
if %RETCODE% equ 0 goto TERMINE
goto ERREUR

:ERREUR
%ABM_BIN%\tsend -sE -r%RETCODE% -m"Traitement en erreur (%RETCODE%)"
%ABM_BIN%\vtgestlog
exit %RETCODE%

:TERMINE
%ABM_BIN%\tsend -sT -r%RETCODE% -m"Traitement termine (%RETCODE%)"
%ABM_BIN%\vtgestlog
exit %RETCODE%

:FIN
