import pytest
import re
from src.utils.text_extraction import (
    delete_text_between_markers,
    extract_text_between_markers,
    remove_lines_containing_pattern,
    remove_whitespace_lines,
    strip_text_lines,
)


@pytest.fixture
def text_as_list():
    return [
        "Centre Universitaire de Santé McGill\n",
        "US US ABDOMEN/PELVIS- APPENDICITIS -AB\n",
        "Date d'examen / Exam Date\n",
        "April 15, 2014 10:28\n",
        "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:\n",
        "XXX.\n",
        "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:\n",
        "ULTRASOUND OF ABDOMEN AND PELVIS\n",
        "XXX.\n",
        "IMPRESSION:\n",
        "XXX.\n",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
        "Page 1 of 2\n",
        "Centre Universitaire de Santé McGill\n",
        "Rapport/Report:\n",
        "XXX\n",
        " \n",
        " \n",
        "Electronically signed by: XXX\n",
        "Radiologiste/Reporting MD:\n",
        "Date Dictée/Dictated:\n",
        "Transcription par/by:\n",
        "Date de transcription/Date Typed:\n",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
        "Page 2 of 2\n",
    ]


@pytest.fixture
def start_marker():
    return "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION"


@pytest.fixture
def end_marker():
    return ["Case dictated by", "Electronically signed by", "Dossier/MRN:"]


@pytest.fixture
def start_between_markers():
    return ["Hôpital de Montréal pour Enfants / Montreal Children's Hospital"]


@pytest.fixture
def end_between_markers():
    return ["Rapport/Report"]


@pytest.fixture
def patterns_to_remove():
    return [
        re.compile(r".*XXX.*"),
        re.compile(r"Page \d of \d", re.IGNORECASE),
        "Hôpital de Montréal pour Enfants",
    ]


@pytest.fixture
def expected_extract_text_between_markers():
    return [
        "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:\n",
        "XXX.\n",
        "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:\n",
        "ULTRASOUND OF ABDOMEN AND PELVIS\n",
        "XXX.\n",
        "IMPRESSION:\n",
        "XXX.\n",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
        "Page 1 of 2\n",
        "Centre Universitaire de Santé McGill\n",
        "Rapport/Report:\n",
        "XXX\n",
        " \n",
        " \n",
    ]


@pytest.fixture
def expected_delete_text_between_markers():
    return [
        "Centre Universitaire de Santé McGill\n",
        "US US ABDOMEN/PELVIS- APPENDICITIS -AB\n",
        "Date d'examen / Exam Date\n",
        "April 15, 2014 10:28\n",
        "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:\n",
        "XXX.\n",
        "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:\n",
        "ULTRASOUND OF ABDOMEN AND PELVIS\n",
        "XXX.\n",
        "IMPRESSION:\n",
        "XXX.\n",
        "XXX\n",
        " \n",
        " \n",
        "Electronically signed by: XXX\n",
        "Radiologiste/Reporting MD:\n",
        "Date Dictée/Dictated:\n",
        "Transcription par/by:\n",
        "Date de transcription/Date Typed:\n",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
        "Page 2 of 2\n",
    ]


@pytest.fixture
def expected_stripped_text():
    return [
        "Centre Universitaire de Santé McGill",
        "US US ABDOMEN/PELVIS- APPENDICITIS -AB",
        "Date d'examen / Exam Date",
        "April 15, 2014 10:28",
        "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:",
        "XXX.",
        "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:",
        "ULTRASOUND OF ABDOMEN AND PELVIS",
        "XXX.",
        "IMPRESSION:",
        "XXX.",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1",
        "Page 1 of 2",
        "Centre Universitaire de Santé McGill",
        "Rapport/Report:",
        "XXX",
        "Electronically signed by: XXX",
        "Radiologiste/Reporting MD:",
        "Date Dictée/Dictated:",
        "Transcription par/by:",
        "Date de transcription/Date Typed:",
        "Hôpital de Montréal pour Enfants / Montreal Children's Hospital",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1",
        "Page 2 of 2",
    ]


@pytest.fixture
def expected_remove_lines_containing_pattern():
    return [
        "Centre Universitaire de Santé McGill\n",
        "US US ABDOMEN/PELVIS- APPENDICITIS -AB\n",
        "Date d'examen / Exam Date\n",
        "April 15, 2014 10:28\n",
        "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:\n",
        "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:\n",
        "ULTRASOUND OF ABDOMEN AND PELVIS\n",
        "IMPRESSION:\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
        "Centre Universitaire de Santé McGill\n",
        "Rapport/Report:\n",
        " \n",
        " \n",
        "Radiologiste/Reporting MD:\n",
        "Date Dictée/Dictated:\n",
        "Transcription par/by:\n",
        "Date de transcription/Date Typed:\n",
        "1001 boul. Décarie, Montréal, Québec, H4A 3J1\n",
    ]


def test_extract_text_between_markers(
    text_as_list, start_marker, end_marker, expected_extract_text_between_markers
):
    extracted_text = extract_text_between_markers(
        start_marker, end_marker, text_as_list
    )
    assert extracted_text == expected_extract_text_between_markers


def test_delete_text_between_markers(
    text_as_list,
    start_between_markers,
    end_between_markers,
    expected_delete_text_between_markers,
):
    extracted_text = delete_text_between_markers(
        start_between_markers, end_between_markers, text_as_list
    )
    assert extracted_text == expected_delete_text_between_markers


def test_strip_lines_and_whitepsace(text_as_list, expected_stripped_text):
    stripped_text = strip_text_lines(text_as_list)
    stripped_text = remove_whitespace_lines(stripped_text)
    assert stripped_text == expected_stripped_text


def test_remove_lines_containing_pattern(
    text_as_list, patterns_to_remove, expected_remove_lines_containing_pattern
):
    filtered_text = remove_lines_containing_pattern(patterns_to_remove, text_as_list)
    print(filtered_text)
    print(len(filtered_text))
    print(len(text_as_list))
    assert filtered_text == expected_remove_lines_containing_pattern
