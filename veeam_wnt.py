import subprocess
import argparse
import sys

def run_powershell_command(cmd):
    """Run a PowerShell command and return the output."""
    full_cmd = ["powershell.exe", "-NoProfile", "-Command", cmd]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error while executing command:\n{e.stderr}")
        sys.exit(1)

def start_job(job_name, full=False):
    """Start a Veeam backup job."""
    cmd = f"Start-VBRComputerBackupJob -Job \"{job_name}\""
    if full:
        cmd += " -FullBackup"
    print(f"Starting job '{job_name}' (Full backup: {full})...")
    output = run_powershell_command(cmd)
    print(output)

def stop_job(job_name):
    """Stop a Veeam backup job."""
    cmd = f"$job = Get-VBRComputerBackupJob -Name \"{job_name}\"; Stop-VBRComputerBackupJob -Job $job"
    print(f"Stopping job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def disable_job(job_name):
    """Disable a Veeam backup job."""
    cmd = f"Get-VBRComputerBackupJob -Name \"{job_name}\" | Disable-VBRComputerBackupJob"
    print(f"Disabling job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def enable_job(job_name):
    """Enable a Veeam backup job."""
    cmd = f"Get-VBRComputerBackupJob -Name \"{job_name}\" | Enable-VBRComputerBackupJob"
    print(f"Enabling job '{job_name}'...")
    output = run_powershell_command(cmd)
    print(output)

def get_job_status(job_name):
    """Get the last result/status of a Veeam backup job."""
    cmd = f"(Get-VBRComputerBackupJob -Name \"{job_name}\").LastResult"
    status = run_powershell_command(cmd)
    print(f"Last run status of job '{job_name}': {status}")

def list_jobs():
    """List all available Veeam backup jobs."""
    cmd = "Get-VBRComputerBackupJob | Select-Object -ExpandProperty Name"
    jobs = run_powershell_command(cmd)
    print("Available jobs:")
    print(jobs)

def main():
    parser = argparse.ArgumentParser(description="Manage Veeam backups via Python")
    parser.add_argument("job_name", nargs="?", help="Name of the Veeam job")
    parser.add_argument("--start", action="store_true", help="Start the job")
    parser.add_argument("--full", action="store_true", help="Force a full backup")
    parser.add_argument("--stop", action="store_true", help="Stop the job")
    parser.add_argument("--enable", action="store_true", help="Enable the job")
    parser.add_argument("--disable", action="store_true", help="Disable the job")
    parser.add_argument("--status", action="store_true", help="Show the job status")
    parser.add_argument("--list", action="store_true", help="List all jobs")

    args = parser.parse_args()

    if args.list:
        list_jobs()
        return

    if not args.job_name:
        print("Error: job name is required unless --list is used.")
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
        print("No action specified. Use --help to see available options.")

if __name__ == "__main__":
    main()
