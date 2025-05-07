import os
import subprocess
import sys

def run(assistant):
    try:
        if sys.platform == "win32":
            # Correct: separate executable and arguments
            update_exe = os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Local\Discord\Update.exe")
            subprocess.Popen([update_exe, "--processStart", "Discord.exe"])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Discord"])
        elif sys.platform == "linux":
            subprocess.Popen(["discord"])
        else:
            print("Unsupported OS.")
            return
        print("✅ Discord launched successfully!")
    except Exception as e:
        print(f"🚫 Failed to open Discord: {e}")
        # written by @GWSURYA
