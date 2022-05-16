import re
from typing import List, Pattern
from src import REPO_DIRECTORY
from src.utils.json import read_jsonlines


def remove_patterns_from_text(dataset: List[dict], patterns_to_remove: List[Pattern]) -> List[dict]:
    """
    Remove headers from the text component of the dataset.
    """
    assert isinstance(dataset, list) and all(
        isinstance(elt, dict) and "text" in elt for elt in dataset
    ), "dataset must be a list of dicts which should each contain a text field."
    for elt in dataset:
        for pattern in patterns_to_remove:
            elt["text"] = re.sub(pattern, "", elt["text"])
        elt["text"] = elt["text"].strip()
    return dataset


def split_measure_text(dataset: List[dict]) -> List[dict]:
    # Split all measure that look like 11.2mm into 11.2 mm
    for elt in dataset:
        elt["text"] = re.sub(r"(\d+\.\d)([cm]m)", r"\1 \2", elt["text"])

    # Split all measures that look like 11.2x12.3cm into 11.2 x 12.3 cm
    # and all measures that loop like 11.2x12.3x13.4cm into 11.2 x 12.3 x 13.4 cm
    for elt in dataset:
        elt["text"] = re.sub(r"(\d+\.\d)x(\d+\.\d)([cm]m)", r"\1 x \2 \3", elt["text"])
        elt["text"] = re.sub(
            r"(\d+\.\d)x(\d+\.\d)x(\d+\.\d)([cm]m)", r"\1 x \2 x \3 \4", elt["text"]
        )
    return dataset


dataset_path = (
    REPO_DIRECTORY / "data" / "processed_data" / "ultrasound" / "dataset.jsonl"
)
dataset = read_jsonlines(dataset_path)

HEADERS = [
    re.compile(r"RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION[:]?"),
    re.compile(r"PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT[:]?"),
    re.compile(r"ULTRASOUND\s*(OF|OF THE)?\s*ABDOMEN AND PELVIS( WITH DOPPLER)?"),
    re.compile(r"ULTRASOUND\s*(OF|OF THE)?\s*ABDOMEN( WITH DOPPLER)?"),
    re.compile(r"ABDOMINAL AND PELVIC ULTRASOUND( WITH DOPPLER)?"),
    re.compile(r"FINDINGS[:]?"),
    re.compile(r"(IMPRESSION|[Ii]mpression)s?:?"),
]
patterns_to_remove = HEADERS

dataset = remove_patterns_from_text(dataset, patterns_to_remove)

dataset = split_measure_text(dataset)
