"""Sets up a virtual environment for easily continuing an existing project"""

#---------------------------Import modules----------------------------#

import os
import subprocess

#---------------------------Get directories---------------------------#

# Sets the director the where the file is being executed from
DIR = os.path.dirname(__file__)
DIR_IGNORE = [".vscode"]
BAT = os.path.join(DIR, "temp.bat")

#venv_dir = "C:\\Users\\username\\Envs" To be implemented

#---------------------------Define functions--------------------------#


def execute_bat(project):
    """Creates and executes temp.bat
    Writes all commands in bat_cmd to temp.bat before executing.
    """
    bat_cmd.insert(0, f"TITLE Working on {project}")
    bat_cmd.append("cmd /k cls" if os.name == 'nt' else "clear")
    os.system(f"attrib -h {BAT}")
    with open(BAT, "w", encoding="UTF-8") as bat:
        bat.write("\n".join(command for command in bat_cmd))
        os.system(f"attrib +h {BAT}")
    subprocess.call([BAT])


def create_virtualenv(project):
    """Creates command for creating virtual environment.    
    Determines if a virtual environment with the given project name
    exists, formatting command to either 'workon' or 'mkvirtualenv'
    based on the outcome.
    """
    temp = f"cmd /c workon {project}"
    if "does not exist" in subprocess.check_output(temp, text=True):
        temp = input("Create virtual environment? y/n (y): ")
        if temp in ["y", ""]:
            bat_cmd.append(f"cmd /k mkvirtualenv {project}")
    else:
        bat_cmd.append(f"cmd /k workon {project}")

    execute_bat(project)


def get_project():
    """Determine a project name.
    Lists all folders in directory from which this module was called.
    User is requested to select a folder from the list which is then
    returned as the project to work on.
    """
    dirs = [dir[1] for dir in os.walk(DIR)][0]
    dirs = [dir for dir in dirs if dir not in DIR_IGNORE]


    while True:
        os.system("cls" if os.name == 'nt' else "clear")
        print("Which project would you like to work on?")
        for i, proj_dir in enumerate(dirs):
            print(i,"<-->", proj_dir)
        project = input("project: ")

        if project.isnumeric():
            try:
                project = dirs[int(project)]
            except IndexError:
                print(f"\"{project}\" is not a valid index")
                input("Press ENTER to retry")
                continue
        if project in dirs:
            bat_cmd.append(f"cd {DIR}\\{project}")
            create_virtualenv(project)
            break

        print(f"The folder \"{project}\" does not exist.")
        input("Press ENTER to retry")


while True:
    os.system("TITLE Project manager")
    bat_cmd = []    # Initialize list of commands to put in temp.bat   
    try:
        get_project()
    except KeyboardInterrupt:
        break
