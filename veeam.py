import subprocess
import platform
import argparse
import sys
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erreur : {e.stderr}")
        sys.exit(1)

def detect_os():
    return platform.system()

def list_jobs():
    os_type = detect_os()
    if os_type == "Linux":
        return run_command("veeamconfig job list")
    elif os_type == "Windows":
        return run_command("\"C:\\Program Files\\Veeam\\Endpoint Backup\\Veeam.Agent.Configurator.exe\" list")
    else:
        print("Système non supporté")
        sys.exit(1)

def start_job(job_name):
    os_type = detect_os()
    if os_type == "Linux":
        cmd = f"veeamconfig job start --name \"{job_name}\""
    elif os_type == "Windows":
        exe = "\"C:\\Program Files\\Veeam\\Endpoint Backup\\Veeam.Agent.Configurator.exe\""
        cmd = f"{exe} -start -name \"{job_name}\""
    else:
        print("Système non supporté")
        sys.exit(1)
    return run_command(cmd)

def get_status():
    os_type = detect_os()
    if os_type == "Linux":
        return run_command("veeamconfig session list")
    elif os_type == "Windows":
        exe = "\"C:\\Program Files\\Veeam\\Endpoint Backup\\Veeam.Agent.Configurator.exe\""
        return run_command(f"{exe} -listSessions")
    else:
        print("Système non supporté")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Script générique Veeam Backup (Linux/Windows)")
    parser.add_argument("--list", action="store_true", help="Lister les jobs")
    parser.add_argument("--start", metavar="JOB_NAME", help="Démarrer un job")
    parser.add_argument("--status", action="store_true", help="Afficher le statut des jobs")

    args = parser.parse_args()

    if args.list:
        print(list_jobs())
    elif args.start:
        print(start_job(args.start))
    elif args.status:
        print(get_status())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
