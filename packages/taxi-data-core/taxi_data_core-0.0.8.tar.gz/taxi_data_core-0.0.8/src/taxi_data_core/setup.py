from subprocess import check_call, CalledProcessError
from sys import executable
from os import path

def install_requirements(requirements_file: str = 'requirements.txt') -> None:
    try:
        check_call([executable, "-m", "pip", "install", "-r", requirements_file])
    except CalledProcessError as e:
        print(f"An error occurred while installing the packages: {e}")
    else:
        print("Requirements installed successfully.")


def main() -> None:
    parent_dir = path.dirname(path.abspath(__file__))
    requirements_file = f"{parent_dir}/requirements.txt"

    install_requirements(requirements_file)

if __name__ == "__main__":
        main()