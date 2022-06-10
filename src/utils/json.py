import jsonlines
from pathlib import Path
from typing import List


def read_jsonlines(file_path: Path) -> List[dict]:
    """
    Reads a jsonlines file and returns a list of dictionaries.
    """
    with jsonlines.open(file_path) as reader:
        return [line for line in reader]


def write_jsonlines(data: List[dict], file_path: Path, mode: str = "w") -> None:
    """
    Writes a list of dictionaries to a jsonlines file.
    """
    with jsonlines.open(file_path, mode=mode) as writer:
        for line in data:
            writer.write(line)
