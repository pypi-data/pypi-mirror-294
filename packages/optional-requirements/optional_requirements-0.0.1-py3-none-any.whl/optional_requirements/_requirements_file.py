from pathlib import Path
from typing import Generator

from packaging.requirements import Requirement


def parse_requirements_file(p: Path) -> Generator[Requirement, None, None]:
    """
    Parse a `requirements.txt` file.

    Args:
        p: The path to the `requirements.txt` file.

    Returns:
        A list of parsed requirements.
    """
    with p.open("r") as f:
        for line in f.readlines():
            # Remove comments and extra whitespace from the line
            line = line.split("#")[0].strip()

            if not len(line):
                continue

            yield Requirement(line)


def find_requirements_file(*, start: Path, name: str) -> Path | None:
    """
    Find a `requirements.txt` file, starting at the given directory, going upwards until we are no longer inside a
    python package (i.e., there is no `__init__.py` file).

    Args:
        start: The directory to start searching from.
        name: The name of the requirements file to find.
    """
    p = start

    while True:
        if not (p / "__init__.py").exists():
            return None

        if (p / name).exists():
            return p / name

        p = p.parent
