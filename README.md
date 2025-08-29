# Integration Veeam with Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-fr-yellow.svg)](README-fr.md)  
This project enables the integration of Veeam Backup with the Visual TOM scheduler.

Two solutions are provided here:

Solution 1: Windows-only integration based on PowerShell commands

Solution 2: Generic Windows/Linux integration to execute jobs on Veeam agents

Two Python scripts are used together with their associated queue wrappers:

Windows integration: veeam_wnt.py with submit_queue_veeam_wnt.bat

Windows/Linux integration: veeam.py with submit_queue_veeam.bat (Windows) or tom_submit.veeam (Linux)

# Disclaimer
No Support and No Warranty are provided by Absyss SAS for this project and related material. The use of this project's files is at your own risk.
Absyss SAS assumes no liability for damage caused by the usage of any of the files offered here via this Github repository.
Consultings days can be requested to help for the implementation.

# Prerequisites

  * Visual TOM 7.1.2 or higher
  * Windows with PowerShell installed
  * Python 3.x or higher
  * Veeam.Backup.PowerShell module installed and accessible

# Instructions
Solution 1: Veeam Backup (Windows-only)
The script calls Veeam PowerShell commands from Python using subprocess. It supports the following actions:
  * Start a job (incremental or full)
  * Stop a job
  * Enable / disable a job
  * Check the status of a job

Solution 2: Multi-platform (Windows/Linux) – Veeam Agent + Veeam Config Tool (veeamconfig)
Veeam Agent (Windows/Linux): allows backups locally, to network shares, or to Veeam repositories.
 - veeamconfig (Linux)
 - Veeam.Agent.Configurator.exe (Windows)

The script calls Veeam commands through Python using subprocess. It manages the following:
  * Start a job for backup
  * Check the status of jobs
  * List available jobs

# Usage Guidelines

The application model should be imported depending on the chosen solution (1/2).
The Visual TOM job must be executed either from the Veeam server (Solution 1) or from a Veeam agent (Solution 2).

Notes:
The Python script veeam_wnt.py uses generic variables.
The script veeam.py requires specifying the installation path of Veeam commands for the Windows part: Veeam.Agent.Configurator.exe.

Tests with Solution 1
Direct execution (Python only)
  ``` Python
python veeam_wnt.py "JobName" --start
python veeam_wnt.py "JobName" --status
python veeam_wnt.py --list
  ```
 
  ```Execution via queue
queue_veeam_wnt.bat JobName START FULL
queue_veeam_wnt.bat JobName START INCR
queue_veeam_wnt.bat JobName STOP
queue_veeam_wnt.bat JobName ENABLE
queue_veeam_wnt.bat JobName DISABLE
queue_veeam_wnt.bat JobName STATUS
  ```

# License
This project is licensed under the Apache 2.0 License - see the [LICENSE](license) file for details


# Code of Conduct
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md) as its Code of Conduct, and we expect project participants to adhere to it. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.
