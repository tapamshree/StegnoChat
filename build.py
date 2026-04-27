import subprocess
import sys

def build():
    print("Building WA-Stego...")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "WA-Stego",
        "main.py"
    ])
    print("Build complete.")

if __name__ == "__main__":
    build()
