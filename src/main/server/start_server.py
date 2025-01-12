import os
import sys
import subprocess
import webbrowser
from time import sleep

skip_req = False


def create_virtualenv(project_dir):
    """
    Creates a virtual environment in the specified directory.

    This function checks if a virtual environment already exists in the
    provided directory (`project_dir`). If not, it creates the virtual
    environment using the `venv` module. If the environment already
    exists, it sets a global flag `skip_req` to `True` to indicate
    that the environment should not be created again.

    Args: project_dir:
        project_dir (str): The path to the directory where the virtual
                            environment will be created.

    Returns:
        str: The path to the created or existing virtual environment directory.

    Global Variables:
        skip_req (bool): A global flag indicating whether the virtual
                                 environment creation was skipped. Set to `True`
                                 if the environment already exists.

    """
    env_dir = os.path.join(project_dir, 'venv')
    global skip_req

    if not os.path.exists(env_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', env_dir])
    else:
        skip_req = True

    return env_dir




def install_requirements(env_dir, project_dir):
    """
    Install dependencies from the requirements.txt file.

    This function installs the dependencies listed in the requirements.txt
    file located in the provided directory (`project_dir`). If the global flag
    `skip_req` is set to `True`, the installation is skipped.

    Args:
        env_dir (str): The path to the virtual environment directory.
        project_dir (str): The path to the directory containing the requirements.txt file.

    """
    global skip_req
    if skip_req: return


    requirements_file = os.path.join(project_dir, 'requirements.txt')

    if not os.path.exists(requirements_file):
        print("No requirements.txt found.")
        return

    print("Installing dependencies from requirements.txt...")

    if sys.platform != 'win32':
        pip_executable = os.path.join(env_dir, 'bin', 'pip')
    else:
        pip_executable = os.path.join(env_dir, 'Scripts', 'pip')

    subprocess.check_call([pip_executable, 'install', '-r', requirements_file])




def start_flask_server(env_dir, project_dir):
    """
    Start the Flask server.

    This function starts the Flask server by running the server.py file
    located in the provided directory (`project_dir`).

    Args:
        env_dir (str): The path to the virtual environment directory.
        project_dir (str): The path to the directory containing the server.py file.

    """
    print("Starting Flask server...")
    app_file = os.path.join(project_dir, 'src\\main\\server\\server.py')

    if sys.platform != 'win32':
        python_executable = os.path.join(env_dir, 'bin', 'python')
    else:
        python_executable = os.path.join(env_dir, 'Scripts', 'python')

    subprocess.Popen([python_executable, app_file])




def open_browser():
    """
    Open the web browser.

    This function opens the default web browser and navigates to the
    site URL after a short delay.
    """
    print("Opening web browser...")
    frontend = os.path.join(project_dir, 'src', 'frontend', 'index.html')
    sleep(3)
    webbrowser.open('file://' + os.path.realpath(frontend))




def print_welcome_message():
    """
    Print a welcome message.

    This function prints a welcome message to the console.
    """
    print("\n\n#-----------------------------------------------#")
    print("|             Wellcome to Diggaren!             |")
    print("#-----------------------------------------------#")





if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Missing project_dir argument.")
        sys.exit(1)

    project_dir = sys.argv[1]
    print(f"dir: {project_dir}")

    env_dir = create_virtualenv(project_dir)
    install_requirements(env_dir, project_dir)
    print_welcome_message()
    start_flask_server(env_dir, project_dir)
    open_browser()


