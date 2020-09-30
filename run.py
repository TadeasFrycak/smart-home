import subprocess
import sys
import os

# subprocess.run(["pkill", "-f", "app.py"])
subprocess.run(["pkill", "-f", "start.py"])
subprocess.Popen([sys.executable, "start.py"])