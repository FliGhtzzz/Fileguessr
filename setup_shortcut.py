import os
import sys
import subprocess

def create_shortcut():
    # 1. Get paths
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    if not os.path.exists(desktop):
        # Fallback if Desktop is redirected to OneDrive etc.
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop, _ = winreg.QueryValueEx(key, "Desktop")
        except:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    shortcut_path = os.path.join(desktop, "File Guessr.lnk")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(project_root, "launcher_bg.py")
    vbs_path = os.path.join(project_root, "start.vbs")
    
    python_exe = sys.executable
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    
    if not os.path.exists(pythonw_exe):
        pythonw_exe = python_exe

    # 1.5 Update/Create start.vbs with ABSOLUTE paths for maximum reliability
    vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\n' \
                  f'WshShell.Run """{pythonw_exe}"" ""{script_path}""", 0, False\n'
    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(vbs_content)

    icon_path = os.path.join(project_root, "static", "favicon.ico")

    print(f"Project Root: {project_root}")
    print(f"Targeting Python: {pythonw_exe}")
    # 2. PowerShell command
    icon_ps = f'$Shortcut.IconLocation = "{icon_path}"' if os.path.exists(icon_path) else ""
    ps_command = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
    $Shortcut.TargetPath = "{vbs_path}"
    $Shortcut.WorkingDirectory = "{project_root}"
    $Shortcut.Description = "File Guessr - Natural Language Search"
    {icon_ps}
    $Shortcut.Save()
    """
    
    try:
        # Run PS with -ExecutionPolicy Bypass to be safe
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_command], check=True)
        print(f"\n✅ Shortcut UPDATED on your Desktop!")
        print(f"Directory: {project_root}")
        print(f"Target: {pythonw_exe}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    create_shortcut()
    input("\nPress Enter to exit...")
