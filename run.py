import subprocess
import sys

subprocess.run(["pkill", "-f", "app.py"])
subprocess.Popen([sys.executable, "app.py"])
