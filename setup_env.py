import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and exit on failure."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    print("Setting up virtual environment...")
    run_command(f"{sys.executable} -m venv .venv")

    venv_activate = (
        ".venv\\Scripts\\activate" if os.name == "nt" else "source .venv/bin/activate"
    )
    print("Activating virtual environment...")
    print(f"Run '{venv_activate}' to activate the environment after setup.")

    print("Upgrading pip, setuptools, and wheel...")
    run_command(f"{venv_activate} && pip install --upgrade pip setuptools wheel")

    print("Installing project in editable mode...")
    run_command(f"{venv_activate} && pip install -e .")

    print("Setup complete!")

if __name__ == "__main__":
    main()
