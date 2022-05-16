import argparse
import os
from pathlib import Path
from typing import List
import jsonlines


TEXT_TO_REMOVE = [
    "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:",
    "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:",
    "IMPRESSION",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge the ultrasound text files with their corresponding labels and"
        + "write to a .jsonl file"
    )
    parser.add_argument(
        "-u",
        "--ultrasound_folder_input_path",
        help="The folder path that contains the ultrasound text files. They should have the format id.txt",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--labels_file_path",
        help="The path to the .jsonl file containing the labels for each text file.",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--features_file_path",
        help="The path to the .jsonl file containing the features for each text file.",
    )
    parser.add_argument(
        "-o",
        "--output_file_path",
        help="The path to the .jsonl file containing the merged text, features and labels.",
        required=True,
    )
    args = parser.parse_args()
    ultrasound_folder_input_path = Path(args.ultrasound_folder_input_path)
    labels_file_path = Path(args.labels_file_path)
    features_file_path = (
        Path(args.features_file_path) if args.features_file_path is not None else ""
    )
    output_file_path = Path(args.output_file_path)

    assert (
        ultrasound_folder_input_path.exists() and ultrasound_folder_input_path.is_dir()
    ), "The ultrasound text file folder either does not exist or is not a folder directory."
    assert (
        labels_file_path.exists() and labels_file_path.suffix == ".jsonl"
    ), f"The labels file either does not exist or is not a .jsonl file, {labels_file_path.suffix}"
    # assert (features_file_path.exists() and features_file_path.suffix == ".jsonl"), (
    #         ), f"The labels file either does not exist or is not a .jsonl file, {features_file_path.suffix}")
    assert (
        output_file_path.suffix == ".jsonl"
    ), f"The output file should be a .jsonl file, {output_file_path.suffix}"
    if not output_file_path.parent.exists():
        os.makedirs(output_file_path.parent)

    return (
        ultrasound_folder_input_path,
        labels_file_path,
        features_file_path,
        output_file_path,
    )


def get_ultrasound_text_dict(ultrasound_folder_input_path: Path) -> dict[str, str]:
    """
    Get a dictionary of ultrasound text with ids as their key
    :param ultrasound_folder_input_path: The path to the folder containing the ultrasound text files
    :return: A dictionary of ultrasound text with ids as their key
    """
    ultrasound_text_dict = {}
    for file_path in ultrasound_folder_input_path.glob("*.txt"):
        id = file_path.stem
        with open(file_path, "r") as f:
            text = f.read()
        ultrasound_text_dict[id] = text
    assert len(ultrasound_text_dict) > 0, "No ultrasound text files found."
    return ultrasound_text_dict


def get_ultrasound_labels(labels_file_path: Path) -> dict[str, int]:
    ultrasound_labels_dict = {}
    with jsonlines.open(labels_file_path) as reader:
        for obj in reader:
            assert (
                len(obj.items()) == 1
            ), "The labels file should contain only one key-value pair per line."
            [(id_, label)] = obj.items()
            ultrasound_labels_dict[id_] = label
    assert len(ultrasound_labels_dict) > 0, "No labels found."
    return ultrasound_labels_dict


def get_ultrasound_features(features_file_path: Path) -> dict[int, list]:
    # TODO: What will the features look like?
    pass


def merge_ultrasound_dataset(
    ultrasound_text_dict: dict[int, str],
    ultrasound_labels_dict: dict[int, int],
    ultrasound_features_dict: dict[int, list],
) -> List[dict]:
    assert len(ultrasound_text_dict) == len(ultrasound_labels_dict), (
        "The number of ultrasound text files and labels should be the same."
        + f"Texts: {len(ultrasound_text_dict)}, Labels: {len(ultrasound_labels_dict)}"
    )
    assert set(ultrasound_text_dict.keys()) == set(
        ultrasound_labels_dict.keys()
    ), "The ids of the ultrasound text files and labels should be the same."
    merged_ultrasound_dataset_dicts = []
    for id_ in ultrasound_text_dict.keys():
        merged_ultrasound_dataset_dicts.append(
            {
                "id": id_,
                "text": ultrasound_text_dict[id_],
                "label": ultrasound_labels_dict[id_],
                "features": [],
            }
        )
    return merged_ultrasound_dataset_dicts


def write_merged_dataset_to_jsonl(
    merged_ultrasound_dataset_dicts: List[dict], output_file_path: Path
) -> None:
    with jsonlines.open(output_file_path, mode="w") as writer:
        for merged_ultrasound_dataset_dict in merged_ultrasound_dataset_dicts:
            writer.write(merged_ultrasound_dataset_dict)


def main():
    # Get arguments
    (
        ultrasound_folder_input_path,
        labels_file_path,
        features_file_path,
        output_file_path,
    ) = parse_args()
    # Get dictionary of ultrasound text with ids as their key
    ultrasound_text_dict = get_ultrasound_text_dict(ultrasound_folder_input_path)
    # Get the labels
    ultrasound_labels_dict = get_ultrasound_labels(labels_file_path)
    # Get the features
    ultrasound_features_dict = get_ultrasound_features(features_file_path)
    # Merge the text, labels and features as a list of dictionaries
    merged_ultrasound_dataset_dicts = merge_ultrasound_dataset(
        ultrasound_text_dict, ultrasound_labels_dict, ultrasound_features_dict
    )
    # Write the merged dataset to a .jsonl file
    write_merged_dataset_to_jsonl(merged_ultrasound_dataset_dicts, output_file_path)


if __name__ == "__main__":
    main()
