"""
extracted_lines = []
extract = False

path = "/home/c_spino/research/NLP_ultrasound_report/data/raw_data/txt/surgical/168 O.txt"

for line in open(path):

    if extract == False and "OPERATIVE PROCEDURE:".lower() in line.strip().lower():
        extract = True

    if extract:
        extracted_lines.append(line)
        if "MONTREAL CHILDREN’S HOSPITAL".lower() in line.strip().lower():
            extract = False  # or break

print("".join(extracted_lines), file=open("results.txt", "a"))

extracted_lines1 = []
extract1 = False
for line in open(path):

    if extract1 == False and "-2-".lower() in line.strip().lower():
        extract1 = True

    if extract1:
        extracted_lines1.append(line)
        if "Dictated".lower() in line.strip().lower():
            extract1 = False  # or break
print("".join(extracted_lines1), file=open("results1.txt", "a"))


filenames = ["results.txt", "results1.txt"]

with open("finalresults.txt", "w") as outfile:

    for names in filenames:

        with open(names) as infile:

            outfile.write(infile.read())

infile = "finalresults.txt"
outfile = "cleaned.txt"

delete_list = [
    "-2-",
    "OPERATION REPORT / PROTOCOLE OPERATOIRE",
    "MONTREAL CHILDREN’S HOSPITAL",
    "HOPITAL DE MONTREAL POUR ENFANTS",
    "OPERATIVE PROCEDURE:",
]
fin = open(infile)
fout = open(outfile, "w+")
for line in fin:
    for word in delete_list:
        line = line.replace(word, "")
    fout.write(line)
fin.close()
fout.close()
"""

import os
import re
from typing import List, Union, Pattern

from langdetect import DetectorFactory, detect


def marker_is_in_text(
    marker: Union[str, List[str]], text: str, case_insensitive: bool = True
) -> bool:
    marker = marker if isinstance(marker, list) else [marker]
    if case_insensitive:
        marker = [m.lower() for m in marker]
        text = text.lower()
    return any(m in text for m in marker)


def extract_text_between_markers(
    start_marker: Union[str, List[str]],
    end_marker: Union[str, List[str]],
    text_as_list: List[str],
) -> List[str]:
    start_marker = start_marker if isinstance(start_marker, list) else [start_marker]
    end_marker = end_marker if isinstance(end_marker, list) else [end_marker]
    extracted_start_text = []
    skip_line = True
    for line in text_as_list:
        if not skip_line:
            extracted_start_text.append(line)
        else:
            skip_line = not marker_is_in_text(start_marker, line)
    extracted_end_text = []
    for line in extracted_start_text:
        if marker_is_in_text(end_marker, line):
            break
        else:
            extracted_end_text.append(line)
    return extracted_end_text


def delete_text_between_markers(
    start_markers: List[List[str]],
    end_markers: List[List[str]],
    text_as_list: List[str],
) -> List[str]:
    assert len(start_markers) == len(
        end_markers
    ), "You should have the same number of start and end markers"
    marker_index = 0
    preserved_text = []
    skip_line = False
    for i, line in enumerate(text_as_list):
        if marker_index > len(start_markers) - 1:
            preserved_text += text_as_list[i:]
            break
        else:
            if marker_is_in_text(start_markers[marker_index], line):
                skip_line = True
            elif marker_is_in_text(end_markers[marker_index], line):
                skip_line = False
                marker_index += 1
            elif not skip_line:
                preserved_text.append(line)
    return preserved_text


def remove_whitespace_lines(text_as_list: List[str]) -> List[str]:
    return [line for line in text_as_list if line.strip() != ""]


def remove_lines_containing_pattern(
    patterns: List[Union[str, Pattern]], text_as_list: List[str], case_insensitive: bool = True
) -> List[str]:
    if case_insensitive:
        text_as_list = [line.lower() for line in text_as_list]
        patterns = [p.lower() if isinstance(p, str) else p for p in patterns]
    preserved_text = []
    for line in text_as_list:
        for pattern in patterns:
            if (isinstance(pattern, str) and not pattern in line) or (
                isinstance(pattern, Pattern) and re.search(pattern, line) is None
            ):
                preserved_text.append(line)
    return preserved_text


def delete_gibberish_lines(text_as_list: List[str]) -> List[str]:
    DetectorFactory.seed = 0
    NOT_LANGUAGE_KEY = "nl"
    # Only keep the line if it has a majority vote for 'en'
    english_text = []
    for line in text_as_list:
        try:
            if detect(line) != NOT_LANGUAGE_KEY:
                english_text.append(line)
            else:
                print("-" * 60)
                print("Removing the following line: ", line)
        except Exception as e:
            print("-" * 60)
            print(
                f"Exception caught during gibberish deletion: {repr(e)}\nfor the line: {line}"
            )
            english_text.append(line)
            print(text_as_list)
    return english_text


cwd = os.getcwd()
surgical_folder_path = os.path.join(cwd, "..", "data", "raw_data", "txt", "surgical")
test_file_path = os.path.join(
    cwd, "..", "data", "raw_data", "txt", "surgical", "168 O.txt"
)
# Print a test file
with open(test_file_path, "r") as f:
    print(f.read())

# NOTE: In some of these cases (e.g. "OPERATIVE NOTE", "OPERATIVE REPORT") we seem to be ignoring clinical history
START_MARKERS = [
    "OPERATIVE PROCEDURE",
    "PROCEDURE",
    "OPERATIVE NOTE",
    "OPERATIVE REPORT",
]
END_MARKERS = ["Dictated", "ESTIMATED BLOOD LOSS"]
START_DELETE_MARKERS = ["User:"]
END_DELETE_MARKERS = ["OPERATION REPORT"]
DELETION_PATTERNS = [
    "MONTREAL CHILDREN’S HOSPITAL",
    "HOPITAL DE MONTREAL POUR ENFANTS",
    "ESTIMATED BLOOD LOSS",
    "COMPLICATIONS",
    "SPECIMENS",
    "DOCUMENT TRANSCRIT CONSIDERE COMME NON REVISE SI NON SIGNE PAR UN MEDECIN",
    "TRANSCRIBED DOCUMENT CONSIDERED NOT REVIEWED IF NOT SIGNED BY A PHYSICIAN",
    "imprimé a partir de Mediscribe",
    "Site:",
    "Date de l’opération / Operation",
    "date (AAYY-MM-JD):",
    "Anesthésiste / Anesthetist:",
    "Chirurgien / Surgeon:",
    "Assistant(s):",
    "Diagnostic préopératoire:",
    "Pre-operative diagnosis:",
    "Diagnostic postopératoire:",
    "Post-operative diagnosis:",
    "Opération / Operation:",
    "Tissu envoyé en pathologie:",
    "Tissue sent to pathology:",
    "Anesthésie / Anesthesia:",
    "Historique et constatations opératoires / History and operative findings:",
    "Clinical note:",
    "DATE/DATE",
    "OPERATION REPORT / PROTOCOLE OPERATOIRE",
    "User:",
    "INTRAOPERATIVE FINDINGS:",
    "ANESTHESIE / ANAESTHETIC:",
    "RAPPORT / REPORT",
]

# Do all the text files have a procedure section that starts with "OPERATIVE PROCEDURE:"?
surgical_reports_path = [
    os.path.join(surgical_folder_path, filename)
    for filename in os.listdir(surgical_folder_path)
    if filename.endswith(".txt")
]
number_surgical_reports = len(surgical_reports_path)
count = 0
# end_marker = "Dictated"
for i, surgical_report_path in enumerate(surgical_reports_path):
    with open(surgical_report_path, "r") as f:
        surgical_report_text = f.read()
    if (
        marker_is_in_text(START_MARKERS, surgical_report_text)
        and marker_is_in_text(END_MARKERS, surgical_report_text)
        and marker_is_in_text(
            START_DELETE_MARKERS + END_DELETE_MARKERS, surgical_report_text
        )
    ):
        count += 1
    else:
        print("Surgical report that is misbehaving: ", surgical_report_path)
print(count)
print(number_surgical_reports)

for i, surgical_report_path in enumerate(surgical_reports_path):
    with open(surgical_report_path, "r") as f:
        surgical_report_text_lines = f.readlines()
        surgical_report_extracted_text = extract_text_between_markers(
            START_MARKERS, END_MARKERS, surgical_report_text_lines
        )
        surgical_report_extracted_text = delete_text_between_markers(
            START_DELETE_MARKERS, END_DELETE_MARKERS, surgical_report_extracted_text
        )
        surgical_report_extracted_text = remove_whitespace_lines(
            surgical_report_extracted_text
        )
        # surgical_report_extracted_text = remove_lines_starting_containing()
        print(surgical_report_path)
        print("".join(surgical_report_extracted_text))
        break
        # TODO: Rethink this process
        # surgical_report_extracted_text = delete_gibberish_lines(
        #     surgical_report_extracted_text
        # )
