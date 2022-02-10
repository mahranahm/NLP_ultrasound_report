#Goal of this python module is extract the text from pdf reports and create a txt version of it with the same name
# pdf_txt.py
# pdf
#  ├─a.pdf
#  ├─b.pdf
#  └─c.pdf
# txt
    
# all the pdf miner packages can simply be simpified to:
# from pdfminer.high_level import extract_text
#text = extract_text(file)

def main():
    #These are the packages needed to create this, the important package here is called pdfminer
    from pathlib import Path
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine
    from pdfminer.converter import PDFPageAggregator

    for path in Path("pdf").glob("*.pdf"):
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
        with open("txt/{}.txt".format(path.stem), "w") as file:
            file.write(text)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
