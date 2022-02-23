import argparse
import os
from pathlib import Path
from typing import Dict, Tuple

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def read_args() -> Tuple[Path, Path]:
    parser = argparse.ArgumentParser(
        description="Convert pdf files in a directory to text files with the same name."
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
        help="The folder path that will be sued to write out the converted text files.",
        required=True,
    )
    args = parser.parse_args()
    pdf_folder_input_path = Path(args.pdf_folder_input_path)
    text_folder_output_path = Path(args.text_folder_output_path)
    assert (
        pdf_folder_input_path.exists() and pdf_folder_input_path.is_dir()
    ), "The input pdf folder does not exist or is not a folder directory."
    if not text_folder_output_path.exists():
        print("The output text folder does not exists, creating it.")
        os.makedirs(text_folder_output_path)
    return pdf_folder_input_path, text_folder_output_path


def read_pdf_text(pdf_file_path: Path) -> Dict[str, str]:
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


def write_text(pdf_text_dict: Dict[str, str], text_folder_output_path: Path) -> None:
    for path_stem, text in pdf_text_dict.items():
        output_file_path = os.path.join(text_folder_output_path, f"{path_stem}.txt")
        with open(output_file_path, "w") as file:
            file.write(text)


def main():
    """
    Goal of this python script is to extract the text from pdf reports 
    and create a txt version of it with the same name.

    Example:
    python pdf_txt.py --pdf_folder_input_path=pdf --text_folder_output_path=txt
    Input:
    pdf
     ├─a.pdf
     ├─b.pdf
     └─c.pdf
    Result:
    txt
     ├─a.txt
     ├─b.txt
     └─c.txt
    """
    # Read command line arguments
    pdf_folder_input_path, text_folder_output_path = read_args()
    # Read pdf files and convert to text files
    print("Reading pdf files...")
    pdf_text_dict = read_pdf_text(pdf_folder_input_path)
    # Write out each text file using the same pdf file name
    print("Writing text files...")
    write_text(pdf_text_dict, text_folder_output_path)


if __name__ == "__main__":
    main()
