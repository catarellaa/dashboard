import subprocess
import sys


google_script = subprocess.Popen([sys.executable, "quickstart.py"])
main_screen = subprocess.Popen([sys.executable, "main_screen.py"])
month_calendar = subprocess.Popen([sys.executable, "month_calendar.py"])

google_script.wait()
main_screen.wait()
month_calendar.wait()

print("success")