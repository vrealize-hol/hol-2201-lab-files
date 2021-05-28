import urllib3
import sys
import subprocess

#temp fix for v0.5
print('temp fix for v0.5')
subprocess.run(["powershell", "-Command", '[microsoft.win32.registry]::SetValue("HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services", "fSingleSessionPerUser", 1)'])
