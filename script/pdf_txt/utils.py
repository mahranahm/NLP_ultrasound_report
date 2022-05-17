import argparse
import os
from pathlib import Path
from typing import Dict, Tuple
from PIL import Image

import pdf2image
import pytesseract
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

REPORT_TYPES = {"surgical", "ultrasound", "pathology"}


def read_args() -> Tuple[Path, Path]:
    parser = argparse.ArgumentParser(
        description="Convert pdf files in a directory to text files with the same name."
    )
    parser.add_argument(
        "-r",
        "--report_type",
        help=f"The type of report to be converted. Accepts one of {REPORT_TYPES}",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--pdf_folder_input_path",
        help="The folder path that contains the pdf files.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--text_folder_output_path",
        help="The folder path that will be used to write out the converted text files.",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--image_folder_output_path",
        help="The folder path that will be used to save the images of the pdf"
        + " (not required for ultrasound reports).",
        required=False,
    )
    args = parser.parse_args()
    report_type = args.report_type
    pdf_folder_input_path = Path(args.pdf_folder_input_path)
    text_folder_output_path = Path(args.text_folder_output_path)
    image_folder_output_path = args.image_folder_output_path
    assert report_type in REPORT_TYPES, f"Invalid report type: {report_type}"
    assert (
        pdf_folder_input_path.exists() and pdf_folder_input_path.is_dir()
    ), "The input pdf folder does not exist or is not a folder directory."
    if not text_folder_output_path.exists():
        print("The output text folder does not exist, creating it.")
        os.makedirs(text_folder_output_path)
    if report_type != "ultrasound":
        assert (
            image_folder_output_path is not None
        ), "The image folder output path is required for {report_type} report types."
        image_folder_output_path = Path(image_folder_output_path)
        if not image_folder_output_path.exists():
            print("The output image folder does not exist, creating it.")
            os.makedirs(image_folder_output_path)
    return (
        report_type,
        pdf_folder_input_path,
        text_folder_output_path,
        image_folder_output_path,
    )


def read_pdf_text(
    pdf_file_path: Path, report_type: str, image_output_folder_path: Path
) -> Dict[str, str]:
    if report_type == "ultrasound":
        return read_pdf_text_directly(pdf_file_path)
    else:
        return read_pdf_text_indirectly(pdf_file_path, image_output_folder_path)


def read_pdf_text_directly(pdf_file_path: Path) -> Dict[str, str]:
    pdf_text_dict = {}
    for path in Path(pdf_file_path).glob("*.pdf"):
        with path.open("rb") as file:
            parser = PDFParser(file)
            document = PDFDocument(parser, "")
            if not document.is_extractable:
                continue

            manager = PDFResourceManager()
            params = LAParams()

            device = PDFPageAggregator(manager, laparams=params)
            interpreter = PDFPageInterpreter(manager, device)

            text = ""

            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                for obj in device.get_result():
                    if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
                        text += obj.get_text()
            pdf_text_dict[path.stem] = text
    return pdf_text_dict


def read_pdf_text_indirectly(
    pdf_file_path: Path, image_output_folder_path: Path
) -> Dict[str, str]:
    pdf_text_dict = {}
    for path in Path(pdf_file_path).glob("*.pdf"):
        file_path_stem = path.stem
        pdf_text_dict[file_path_stem] = []
        # Convert the pdf to images
        images = pdf2image.convert_from_path(path)
        for i, image in enumerate(images):
            image_path = os.path.join(
                image_output_folder_path, f"{file_path_stem}_{i}.png"
            )
            image.save(image_path, "PNG")
            img = Image.open(image_path)
            pdf_text_dict[file_path_stem].append(pytesseract.image_to_string(img))
        pdf_text_dict[file_path_stem] = "".join(pdf_text_dict[file_path_stem])
    return pdf_text_dict


def write_text(pdf_text_dict: Dict[str, str], text_folder_output_path: Path) -> None:
    for path_stem, text in pdf_text_dict.items():
        output_file_path = os.path.join(text_folder_output_path, f"{path_stem}.txt")
        with open(output_file_path, "w") as file:
            file.write(text)
