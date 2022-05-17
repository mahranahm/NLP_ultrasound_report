from script.pdf_txt.utils import read_args, read_pdf_text, write_text


def main():
    """
    Goal of this python script is to extract the text from pdf reports
    and create a txt version of it with the same name.

    Example:
    python pdf_txt.py --report_type=ultrasound --pdf_folder_input_path=pdf --text_folder_output_path=txt
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
    (
        report_type,
        pdf_folder_input_path,
        text_folder_output_path,
        image_output_folder_path,
    ) = read_args()
    # Read pdf files and convert to text files
    print("Reading pdf files...")
    pdf_text_dict = read_pdf_text(
        pdf_folder_input_path, report_type, image_output_folder_path
    )
    # Write out each text file using the same pdf file name
    print("Writing text files...")
    write_text(pdf_text_dict, text_folder_output_path)


if __name__ == "__main__":
    main()
