import os
import shutil
import subprocess
import datetime

# CONFIGURATION
APP_NAME = "app"
DEPLOY_DIR = r"C:\intern\test\app"
BACKUP_DIR = r"C:\intern\test\backup"
GIT_REPO = r"https://github.com/rohittdhakal/testRepo.git"
PYTHON_ENV = r"C:\deploy-demo\venv\Scripts\python.exe"
REQUIREMENTS_FILE = "requirements.txt"

def backup_existing():
    """Backup current deployment with timestamp."""
    if os.path.exists(DEPLOY_DIR):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"{APP_NAME}_{timestamp}")
        shutil.copytree(DEPLOY_DIR, backup_path)
        print(f"[+] Backup created at {backup_path}")

def deploy_code():
    """Deploy new code from GitHub repo."""
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
        print("[*] Old deployment removed.")

    # Clone latest code
    subprocess.check_call(["git", "clone", GIT_REPO, DEPLOY_DIR])
    print("[+] New code cloned.")

def install_dependencies():
    """Install Python dependencies."""
    req_path = os.path.join(DEPLOY_DIR, REQUIREMENTS_FILE)
    if os.path.exists(req_path):
        subprocess.check_call([PYTHON_ENV, "-m", "pip", "install", "-r", req_path])
        print("[+] Dependencies installed.")
    else:
        print("[!] No requirements.txt found, skipping dependencies.")

def restart_app():
    """Restart app (example with Flask)."""
    # Kill old process (if running on port 5000)
    os.system("taskkill /F /IM python.exe /T")

    # Start new process
    subprocess.Popen([PYTHON_ENV, "app.py"], cwd=DEPLOY_DIR)
    print("[+] App restarted successfully.")

if __name__ == "__main__":
    print("=== Starting Deployment ===")
    backup_existing()
    deploy_code()
    install_dependencies()
    restart_app()
    print("=== Deployment Completed ===")
