import logging
from pathlib import Path
import zipfile
from xml.etree import ElementTree
import os
from collections import defaultdict
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)

class EpubExtractor:
    def __init__(self, epub_path: str):
        self.epub_path = Path(epub_path)
        self.output_folder = self.create_output_folder()

    def create_output_folder(self) -> Path:
        """Creates an output folder based on the epub file name."""
        books_folder = Path("books")
        books_folder.mkdir(exist_ok=True)

        epub_folder_name = "".join([c for c in self.epub_path.stem if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        epub_folder = books_folder / epub_folder_name
        epub_folder.mkdir(exist_ok=True)

        return epub_folder

    def find_opf_file(self, myzip: zipfile.ZipFile) -> Optional[str]:
        """Finds the .opf file in the entire .epub file and extracts the order of files."""
        for file in myzip.namelist():
            if file.endswith('.opf'):
                with myzip.open(file) as opf_file:
                    tree = ElementTree.parse(opf_file)

                manifest_items = tree.findall('.//{http://www.idpf.org/2007/opf}item')

                files_order = [item.attrib['href'] for item in manifest_items if 'html' in item.attrib['href'] or item.attrib['href'].endswith('.htm')]
                self.save_order_to_file(files_order)

                return file
        return None

    def extract_xhtml_files(self) -> None:
        """Extracts all .xhtml and .html files from the epub file."""
        with zipfile.ZipFile(self.epub_path, 'r') as myzip:
            for file in myzip.namelist():
                if file.endswith('.xhtml') or file.endswith('.html') or file.endswith('.htm'):
                    with myzip.open(file) as content_file:
                        content = content_file.read()

                    output_file_path = self.output_folder / Path(file).name
                    with open(output_file_path, 'wb') as new_file:
                        new_file.write(content)
                    logging.info(f"Extracted file: {output_file_path}")

    def save_order_to_file(self, files_order: list) -> None:
        """Saves the order of XHTML and HTML files to a text file."""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        order_file_path = self.output_folder / "files_order.txt"
        with open(order_file_path, 'w') as order_file:
            for file in files_order:
                file_name = os.path.basename(file)
                order_file.write(file_name + "\n")
        logging.info(f"Files order saved to {order_file_path}")

def extract(epub_path):
    epub_path = Path(epub_path)
    if epub_path.is_dir():
        for epub_file in epub_path.glob('*.epub'):
            print(f"Extracting {epub_file}")
            extractor = EpubExtractor(epub_file)
            with zipfile.ZipFile(epub_file, 'r') as myzip:
                extractor.find_opf_file(myzip)
            extractor.extract_xhtml_files()
    elif epub_path.is_file():
        print(f"Extracting {epub_path}")
        extractor = EpubExtractor(epub_path)
        with zipfile.ZipFile(epub_path, 'r') as myzip:
            extractor.find_opf_file(myzip)
        extractor.extract_xhtml_files()
    else:
        print(f"Invalid path: {epub_path}")
