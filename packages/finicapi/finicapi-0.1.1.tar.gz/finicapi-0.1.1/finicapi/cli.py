import os
import sys


def create_finic_app(argv=sys.argv):
    if len(argv) < 2:
        print("Please specify the project directory:\n create-finic-app <project-name>")
        return
    directory_name = argv[1]

    os.system(
        f"git clone https://github.com/finic-ai/create-finic-app {directory_name}"
    )
    print(
        f"Finic app created successfully. cd into /{directory_name} and run `poetry install` to install dependencies"
    )
