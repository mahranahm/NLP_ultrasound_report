import argparse
import os
from pathlib import Path
from typing import List

from src.utils.text_extraction import (
    extract_text_between_markers,
    delete_text_between_markers,
    remove_whitespace_lines,
    strip_text_lines,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract the main text components from the ultrasound text files. Place them in processed folder."
    )
    parser.add_argument(
        "-u",
        "--ultrasound_folder_input_path",
        help="The folder path that contains the ultrasound text files.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_folder_path",
        help="The folder path that will be used to save the extracted text from the ultrasound text files.",
        required=True,
    )
    args = parser.parse_args()
    ultrasound_folder_input_path = Path(args.ultrasound_folder_input_path)
    output_folder_path = Path(args.output_folder_path)

    assert (
        ultrasound_folder_input_path.exists() and ultrasound_folder_input_path.is_dir()
    ), "The ultrasound text file folder either does not exist or is not a folder directory."

    if not output_folder_path.exists():
        print("The output folder does not exist, creating it.")
        os.makedirs(output_folder_path)

    return ultrasound_folder_input_path, output_folder_path


def get_ultrasound_text_file_paths(
    ultrasound_folder_input_path: Path, excluded_files: List[str]
) -> List[Path]:
    ultrasound_text_files = os.listdir(ultrasound_folder_input_path)
    ultrasound_folder_input_path = [
        Path(os.path.join(ultrasound_folder_input_path, text_file))
        for text_file in ultrasound_text_files
        if text_file.endswith(".txt") and text_file not in excluded_files
    ]
    assert (
        len(ultrasound_folder_input_path) > 0
    ), "No ultrasound text files found. Are you sure this is the right directory?"
    return ultrasound_folder_input_path


def get_ultrasound_text_body(
    ultrasound_text_file_path: Path,
    body_begin_markers: List[str],
    body_end_markers: List[str],
    body_between_start_markers: List[str],
    body_between_end_markers: List[str],
) -> str:
    with open(ultrasound_text_file_path, "r") as f:
        ultrasound_text_file_lines = f.readlines()
        extracted_body = extract_text_between_markers(
            body_begin_markers, body_end_markers, ultrasound_text_file_lines
        )
        extracted_body = delete_text_between_markers(
            body_between_start_markers, body_between_end_markers, extracted_body
        )
        extracted_body = remove_whitespace_lines(extracted_body)
        extracted_body = strip_text_lines(extracted_body)
        return extracted_body


def get_ultrasound_text_bodies(
    ultrasound_text_file_paths: List[Path],
    body_begin_markers: List[str],
    body_end_markers: List[str],
    body_between_start_markers: List[str],
    body_between_end_markers: List[str],
) -> List[str]:
    ultrasound_text_bodies = []
    for ultrasound_text_file_path in ultrasound_text_file_paths:
        ultrasound_text_bodies.append(
            get_ultrasound_text_body(
                ultrasound_text_file_path,
                body_begin_markers=body_begin_markers,
                body_end_markers=body_end_markers,
                body_between_start_markers=body_between_start_markers,
                body_between_end_markers=body_between_end_markers,
            )
        )
    return ultrasound_text_bodies


def write_ultrasound_text_bodies(
    ultrasound_text_bodies: List[str],
    output_folder_path: Path,
    ultrasound_text_file_paths: List[Path],
):
    for ultrasound_text_body, ultrasound_file_path in zip(
        ultrasound_text_bodies, ultrasound_text_file_paths
    ):
        ultrasound_output_file_path = output_folder_path / ultrasound_file_path.name
        with open(ultrasound_output_file_path, "w") as f:
            f.write(" ".join(ultrasound_text_body))
