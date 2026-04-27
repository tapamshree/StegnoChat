import subprocess
import sys

def build():
    print("Building Stegnochat...")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "Stegnochat",
        "main.py"
    ])
    print("Build complete.")

if __name__ == "__main__":
    build()
