import re
from typing import List, Union, Pattern


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
    assert isinstance(start_marker, str) or isinstance(
        start_marker, list
    ), "start_marker should be a string or a list of strings"
    assert isinstance(end_marker, str) or isinstance(
        end_marker, list
    ), "end_marker should be a string or a list of one string"
    start_marker = start_marker if isinstance(start_marker, list) else [start_marker]
    end_marker = end_marker if isinstance(end_marker, list) else [end_marker]
    skip_line = True
    start_index = 0
    for index, line in enumerate(text_as_list):
        skip_line = not marker_is_in_text(start_marker, line)
        if not skip_line:
            start_index = index
            break
    extracted_start_text = text_as_list[start_index:]
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
    assert (
        isinstance(start_markers, list) and len(start_markers) > 0
    ), f"start_markers must be a list of one or more strings but it looks like: {start_markers}"
    assert (
        isinstance(start_markers, list) and len(start_markers) > 0
    ), f"end_markers must be a list of one or more strings but it looks like: {end_markers}"
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


def strip_text_lines(text_as_list: List[str]) -> List[str]:
    return [line.strip() for line in text_as_list]


def remove_lines_containing_pattern(
    patterns: List[Union[str, Pattern]],
    text_as_list: List[str],
    case_insensitive: bool = True,
) -> List[str]:
    # Case insensitivity for the regex goes to the pattern i.e. re.compile(pattern, re.IGNORECASE)
    assert all(
        isinstance(pattern, (str, Pattern)) for pattern in patterns
    ), "All patterns should be strings or compiled regexes"
    preserved_text = []
    for line in text_as_list:
        if all(
            (
                isinstance(pattern, str)
                and not (
                    pattern.lower() in line.lower()
                    if case_insensitive
                    else pattern in line
                )
            )
            or (isinstance(pattern, Pattern) and re.search(pattern, line) is None)
            for pattern in patterns
        ):
            preserved_text.append(line)
    return preserved_text
