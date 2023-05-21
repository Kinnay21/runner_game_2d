import os
import platform
from typing import Tuple

import PyInstaller.__main__

""" This programm generate an executable file that allows to run the projet without running the python project.
"""


def create_executable():
    """Simple program that greets NAME for a total of COUNT times."""

    project_src_path = os.path.join("src")

    # delimiter for the specific OS
    delimiter = ";" if platform.system() == "Windows" else ":"

    project_data = [
        normalize_path("graphics", "graphics"),
        normalize_path("audio", "audio"),
        normalize_path("font", "font"),
    ]

    icon_path = os.path.join(os.path.dirname(__file__), "graphics", "icon.ico")

    PyInstaller.__main__.run(
        # commad line in a terminal
        # pyinstaller --clean --name <inter_name> --onefile -F --add-data "<src>;<dist>"... --icon <icon_path> --windowed <path_to_main.py>
        [
            "--clean",
            "--name=runner_game_2d",
            "--onefile",  # create only one file
            "-F",
            *[
                f"--add-data={data[0]}{delimiter}{data[1]}" for data in project_data
            ],  # add data to the executable: the data is the path to the data in the project and the path to the data in the executable
            f"--icon={icon_path}",
            "--windowed",  # no console
            # "--log-level=DEBUG",
            f"{os.path.join(project_src_path, 'main.py')}",
        ]
    )


def normalize_path(src: str, dst: str) -> Tuple[str, str]:
    """return the normalized path for the current OS"""
    return os.path.normpath(src), os.path.normpath(dst)


if __name__ == "__main__":
    create_executable()
