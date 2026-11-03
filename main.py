import subprocess
import sys


google_script = subprocess.Popen([sys.executable, "quickstart.py"])
main_screen = subprocess.Popen([sys.executable, "main_screen.py"])

google_script.wait()
main_screen.wait()

print("success")