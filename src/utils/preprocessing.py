import re
from typing import List, Pattern

from nltk.tokenize import word_tokenize
from nltk.tokenize.stanford import StanfordTokenizer
from src import REPO_DIRECTORY
from src.utils.json import read_jsonlines


def remove_patterns_from_text(
    dataset: List[dict], patterns_to_remove: List[Pattern]
) -> List[dict]:
    """
    Remove headers from the text component of the dataset.
    Also works with an empty list of patterns. In this case, no
    pattern is removed, the text is simply stripped.
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
    """
    Convert the measures into individual words e.g. 11.2mm -> 11.2 mm
    and 11.2x13.2cm -> 11.2 x 13.2 cm
    """
    # Split all measures that look like 11.2x12.3cm into 11.2 x 12.3cm
    # and all measures that loop like 11.2x12.3x13.4cm into 11.2 x 12.3 x 13.4cm
    for elt in dataset:
        elt["text"] = re.sub(
            r"(\d+\.\d)x(\d+\.\d)x(\d+\.\d)", r"\1 x \2 x \3", elt["text"]
        )
        elt["text"] = re.sub(r"(\d+\.\d)x(\d+\.\d)", r"\1 x \2", elt["text"])

    # Split all measure that look like 11.2mm into 11.2 mm
    for elt in dataset:
        # Decimal numbers
        elt["text"] = re.sub(r"(\d+\.\d)([cm]m)", r"\1 \2", elt["text"])
        # Whole number
        elt["text"] = re.sub(r"(\d+)([cm]m)", r"\1 \2", elt["text"])

    return dataset


def lowercase_dataset(dataset: List[dict]) -> List[dict]:
    """
    Lowercase the text component of the dataset.
    """
    for elt in dataset:
        elt["text"] = elt["text"].lower()
    return dataset


def tokenize_dataset(dataset: List[dict], tokenizer_type: str) -> List[dict]:
    """Tokenizes the text component of the dataset. NOTE: This leaves
    the text component as a list of tokens.

    TODO:
    - RNN neural models will require an embedding step.
    - Neural models like BERT will require their own tokenizer
    from huggingface.
    """
    for elt in dataset:
        if tokenizer_type == "nltk":
            elt["text"] = word_tokenize(elt["text"])
        elif tokenizer_type == "standford":
            elt["text"] = StanfordTokenizer().tokenize(elt["text"])
        else:
            raise ValueError(f"Unknown tokenizer type {tokenizer_type}.")
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

dataset = lowercase_dataset(dataset)

dataset = tokenize_dataset(dataset, "nltk")