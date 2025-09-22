
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
   
    os.chmod(path, stat.S_IWRITE)
    func(path)

def create_backup():
    
    if os.path.exists(deploy_directory):
        
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        backup_location = os.path.join(backup_directory, f"{app_name}_{timestamp}")
        
       
        shutil.copytree(deploy_directory, backup_location, dirs_exist_ok=True)
        print(f" backup created: {backup_location}")
    else:
        print(" cannot create ")

def deploy_new_code():
    
    
    if os.path.exists(deploy_directory):
        print(" previous deployment removing")
        shutil.rmtree(deploy_directory, onerror=handle_readonly_files)
        print(" previous deployment removed.")

   
    print(f"{git_repository}...")
    subprocess.check_call(["git", "clone", git_repository, deploy_directory])
    print(" sucessful")

def install_dependencies():
    
    requirements_path = os.path.join(deploy_directory, requirements_file)
    
    if os.path.exists(requirements_path):
        
        subprocess.check_call([
            python_executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            requirements_path
        ])
        print(" successfully.")
    else:
        print(" skiping")

def restart_application():
 
    

    print(" halt existing process")
    os.system("taskkill /F /IM python.exe /T")
    
  
    print("start")
    app_script = os.path.join(deploy_directory, "app.py")
    
  
    subprocess.Popen([python_executable, "app.py"], cwd=deploy_directory)
    print(" app restarted successfully.")


if __name__ == "__main__":
    print("=" * 30)
    print("   script starting")
    print("=" * 30)
    
    try:
        
        print(" creating backup")
        create_backup()
        
        
        print(" deploying newcode")
        deploy_new_code()
        
      
        print(" installig")
        install_dependencies()
        
        print(" restarting")
        restart_application()
        
        print("\n" + "=" * 30)
        print("  complete")
        print("=" * 30)
        
    except Exception as e:
        print(f"\n[ERROR] failes: {e}")
        
