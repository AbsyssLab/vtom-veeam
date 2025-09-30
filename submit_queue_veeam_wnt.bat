@echo OFF

set PATH_PYTHON=C:\Users\Jdoe\AppData\Local\Programs\Python\Python311\
set PATH=%PATH_PYTHON%;%PATH%

call submit_aff.bat %*
echo _______________________________________________________________________
echo Debut de l'execution du script...
date /T
time /T
echo _______________________________________________________________________

rem TEST Mode
if "%TOM_JOB_EXEC%" == "TEST" (
	echo Job execute en mode TEST
	%ABM_BIN%\tsend -sT -r0 -m"Traitement termine (mode TEST)"
	%ABM_BIN%\vtgestlog
	goto FIN
)

set JOB_BACKUP=%1
set ACTION=%2
set BACKUP_TYPE=%3

set VEEAM_CMD=%PATH_PYTHON%\python %ABM_BIN%\veeam.py %JOB_BACKUP%

echo Execute Veeam backup Job
echo.

REM A different execution for each option
if "%ACTION%" == "START" (
	if "%BACKUP_TYPE%" == "FULL" (
		echo -- Full Backup --
		call %VEEAM_CMD% --start --full
	) else if "%BACKUP_TYPE%" == "INCR" (
		echo -- Incremental Backup --
		call %VEEAM_CMD% --start
	)
) else if "%ACTION%" == "STOP" (
		echo -- Stop Job --
		call %VEEAM_CMD% --stop
) else if "%ACTION%" == "ENABLE" (
		echo -- Enable Job --
		call %VEEAM_CMD% --enable
) else if "%ACTION%" == "DISABLE" (
		echo -- Disable Job --
		call %VEEAM_CMD% --disable
) else if "%ACTION%" == "STATUS" (
		echo -- Job Status --
		call %VEEAM_CMD% --status
)
echo.

set RETCODE=%ERRORLEVEL%
if %RETCODE% equ 0 goto TERMINE
goto ERREUR

:ERREUR
%ABM_BIN%\tsend -sE -r%RETCODE% -m"Traitement en erreur (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution du script
date /T
time /T
echo Exit [%RETCODE%] donc pas d'acquittement
echo _______________________________________________________________________
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:TERMINE
%ABM_BIN%\tsend -sT -r%RETCODE% -m"Traitement termine (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution du script
date /T
time /T
echo Exit [%RETCODE%] donc acquittement
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:FIN
