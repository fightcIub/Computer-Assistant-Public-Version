import subprocess
import platform

def run(assistant):
    try:
        system_platform = platform.system()

        if system_platform == "Windows":
            subprocess.Popen("calc.exe")
        elif system_platform == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Calculator"])
        elif system_platform == "Linux":
            subprocess.Popen(["gnome-calculator"])
        else:
            print("❌ Unsupported operating system for opening Calculator.")
            return

        print("✅ Calculator opened successfully!")

    except Exception as e:
        print(f"❌ Failed to open Calculator: {e}")
# written by @GWSURYA