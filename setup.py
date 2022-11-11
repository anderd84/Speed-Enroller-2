import subprocess
import sys

print("setting up...")

subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

print("done")