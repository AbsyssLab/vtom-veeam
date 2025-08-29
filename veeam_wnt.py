import subprocess
import argparse
import sys

def run_powershell_command(cmd):
    full_cmd = ["powershell.exe", "-NoProfile", "-Command", cmd]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution :\n{e.stderr}")
        sys.exit(1)

def start_job(job_name, full=False):
    cmd = f"Start-VBRComputerBackupJob -Job \"{job_name}\""
    if full:
        cmd += " -FullBackup"
    print(f"Lancement du job '{job_name}' (Full: {full})...")
    output = run_powershell_command(cmd)
    print(output)

def stop_job(job_name):
    cmd = f"$job = Get-VBRComputerBackupJob -Name \"{job_name}\"; Stop-VBRComputerBackupJob -Job $job"
    print(f"Arrêt du job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def disable_job(job_name):
    cmd = f"Get-VBRComputerBackupJob -Name \"{job_name}\" | Disable-VBRComputerBackupJob"
    print(f"Désactivation du job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def enable_job(job_name):
    cmd = f"Get-VBRComputerBackupJob -Name \"{job_name}\" | Enable-VBRComputerBackupJob"
    print(f"Activation du job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def get_job_status(job_name):
    cmd = f"(Get-VBRComputerBackupJob -Name \"{job_name}\").LastResult"
    status = run_powershell_command(cmd)
    print(f"Statut du dernier job '{job_name}' : {status}")

def list_jobs():
    cmd = "Get-VBRComputerBackupJob | Select-Object -ExpandProperty Name"
    jobs = run_powershell_command(cmd)
    print("Liste des jobs disponibles :")
    print(jobs)

def main():
    parser = argparse.ArgumentParser(description="Gestion des backups Veeam via Python")
    parser.add_argument("job_name", nargs="?", help="Nom du job Veeam")
    parser.add_argument("--start", action="store_true", help="Démarrer le job")
    parser.add_argument("--full", action="store_true", help="Forcer un full backup")
    parser.add_argument("--stop", action="store_true", help="Arrêter le job")
    parser.add_argument("--enable", action="store_true", help="Activer le job")
    parser.add_argument("--disable", action="store_true", help="Désactiver le job")
    parser.add_argument("--status", action="store_true", help="Afficher le statut du job")
    parser.add_argument("--list", action="store_true", help="Lister tous les jobs")

    args = parser.parse_args()

    if args.list:
        list_jobs()
        return

    if not args.job_name:
        print("Erreur : le nom du job est requis sauf si --list est utilisé.")
        sys.exit(1)

    if args.start:
        start_job(args.job_name, full=args.full)
    elif args.stop:
        stop_job(args.job_name)
    elif args.enable:
        enable_job(args.job_name)
    elif args.disable:
        disable_job(args.job_name)
    elif args.status:
        get_job_status(args.job_name)
    else:
        print("Aucune action spécifiée. Utilisez --help pour voir les options.")

if __name__ == "__main__":
    main()
