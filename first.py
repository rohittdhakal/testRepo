# import os
# import shutil
# import subprocess
# import datetime
# import stat


# APP_NAME = "app"
# DEPLOY_DIR = r"C:\intern\test\app"
# BACKUP_DIR = r"C:\intern\test\backup"
# GIT_REPO = r"https://github.com/rohittdhakal/testRepo.git"
# PYTHON_ENV = r"C:\deploy-demo\venv\Scripts\python.exe"
# REQUIREMENTS_FILE = "requirements.txt"


# def remove(func, path, excinfo):
    
#     os.chmod(path, stat.S_IWRITE)
#     func(path)

# def backup():
    
#     if os.path.exists(DEPLOY_DIR):
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         backup_path = os.path.join(BACKUP_DIR, f"{APP_NAME}_{timestamp}")
#         shutil.copytree(DEPLOY_DIR, backup_path, dirs_exist_ok=True)
#         print(f"[+] Backup created at {backup_path}")

# def deploy():
    
#     if os.path.exists(DEPLOY_DIR):
#         shutil.rmtree(DEPLOY_DIR, onerror=remove)
#         print("[*] Old deployment removed.")

#     subprocess.check_call(["git", "clone", GIT_REPO, DEPLOY_DIR])
#     print("[+] New code cloned.")

# def dependencies():
    
#     req_path = os.path.join(DEPLOY_DIR, REQUIREMENTS_FILE)
#     if os.path.exists(req_path):
#         subprocess.check_call([PYTHON_ENV, "-m", "pip", "install", "-r", req_path])
#         print("[+] Dependencies installed.")
#     else:
#         print("[!] No requirements.txt found, skipping dependencies.")

# def restart_app():
    
    
#     os.system("taskkill /F /IM python.exe /T")

   
#     subprocess.Popen([PYTHON_ENV, "app.py"], cwd=DEPLOY_DIR)
#     print("[+] App restarted successfully.")


# if __name__ == "__main__":
#     print("=== Starting Deployment ===")
#     backup()
#     deploy()
#     dependencies()
#     restart_app()
#     print("=== Deployment Completed ===")
import os
import shutil
import subprocess
import datetime
import stat


app_name = "app"
deploy_directory = r"C:\intern\test\app"
backup_directory = r"C:\intern\test\backup"  
git_repository = r"https://github.com/rohittdhakal/testRepo.git"
python_executable = r"C:\deploy-demo\venv\Scripts\python.exe"
requirements_file = "requirements.txt"

def handle_readonly_files(func, path, excinfo):
    """
    Windows sometimes makes files read-only which blocks deletion
    This function helps remove those pesky read-only permissions
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def create_backup():
    """Create a backup of current deployment before updating"""
    if os.path.exists(deploy_directory):
        
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        backup_location = os.path.join(backup_directory, f"{app_name}_{timestamp}")
        
       
        shutil.copytree(deploy_directory, backup_location, dirs_exist_ok=True)
        print(f"[+] Backup successfully created at: {backup_location}")
    else:
        print("[!] No existing deployment found to backup")

def deploy_new_code():
    """Remove old deployment and clone fresh code from git"""
    
    if os.path.exists(deploy_directory):
        print("[*] Removing old deployment...")
        shutil.rmtree(deploy_directory, onerror=handle_readonly_files)
        print("[*] Old deployment cleaned up.")

   
    print(f"[*] Cloning code from {git_repository}...")
    subprocess.check_call(["git", "clone", git_repository, deploy_directory])
    print("[+] Fresh code successfully cloned.")

def install_dependencies():
    """Install Python dependencies if requirements.txt exists"""
    requirements_path = os.path.join(deploy_directory, requirements_file)
    
    if os.path.exists(requirements_path):
        print("[*] Installing Python dependencies...")
        subprocess.check_call([
            python_executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            requirements_path
        ])
        print("[+] Dependencies installed successfully.")
    else:
        print("[!] No requirements.txt found - skipping dependency installation.")

def restart_application():
    """
    Restart the application by killing existing python processes and starting new one
    Note: This is a bit aggressive - kills ALL python.exe processes
    TODO: Maybe find a more targeted approach later
    """
    

    print("[*] Stopping existing application processes...")
    os.system("taskkill /F /IM python.exe /T")
    
  
    print("[*] Starting application...")
    app_script = os.path.join(deploy_directory, "app.py")
    
  
    subprocess.Popen([python_executable, "app.py"], cwd=deploy_directory)
    print("[+] Application restarted successfully.")


if __name__ == "__main__":
    print("=" * 30)
    print("   DEPLOYMENT SCRIPT STARTING")
    print("=" * 30)
    
    try:
        
        print("\n1. Creating backup...")
        create_backup()
        
        
        print("\n2. Deploying new code...")
        deploy_new_code()
        
      
        print("\n3. Installing dependencies...")
        install_dependencies()
        
        print("\n4. Restarting application...")
        restart_application()
        
        print("\n" + "=" * 30)
        print("   DEPLOYMENT COMPLETED! 🎉")
        print("=" * 30)
        
    except Exception as e:
        print(f"\n[ERROR] Deployment failed: {e}")
        print("Check the logs above for more details.")
