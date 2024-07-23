import os
import re
from pathlib import Path

class EpubProcessor:
    def __init__(self, base_path, character_limit=350000):
        self.base_path = Path(base_path)
        self.order_file = self.base_path / "files_order.txt"
        self.order = self.read_order_file()
        self.character_limit = character_limit

    def read_order_file(self):
        with open(self.order_file, 'r', encoding='utf-8') as file:
            order = file.readlines()
        return [x.strip() for x in order]

    def clean_html_content(self, text):
        text = re.sub(r"\s+", " ", text)  # Collapses all whitespace into single spaces for cleaner processing
        
        text = re.sub(r"<div[^>]*>", "", text)
        text = re.sub(r"</div>", "\n", text)
        text = re.sub(r"<p[^>]*>", "", text)
        text = re.sub(r"</p>", "\n", text)
        text = re.sub(r"<h1[^>]*>", "", text)
        text = re.sub(r"</h1>", "\n", text)
        text = re.sub(r"<a[^>]*>", "", text)
        text = re.sub(r"</a>", "\n", text)
        text = re.sub(r"<span[^>]*>", "", text)
        text = re.sub(r"<link[^>]*/>", "", text)
        text = re.sub(r"</span>", "\n", text)
        text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        text = re.sub(r"<.*?>", "", text)

        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        
        return '\n'.join(non_empty_lines)

    def process_files(self):
        processed_files = []
        skipped_files = []
        copyright_keywords = [
            "copyright", "all rights reserved",
            "ISBN", "Library of Congress"
        ]
        for file_name in self.order:
            full_file_path = self.base_path / file_name
            if full_file_path.is_file():
                with open(full_file_path, 'r', encoding='utf-8', errors='replace') as file:
                    file_content = file.read()

                    html_content = re.findall("<.*?>", file_content)
                    html_content_length = sum(len(tag) for tag in html_content)
                    total_content_length = len(file_content)

                    if html_content_length / total_content_length > 0.9:
                        print(f"File {file_name} is mainly HTML, skipping.")
                        skipped_files.append(full_file_path)
                        continue

                    cleaned_content = self.clean_html_content(file_content)
                    lines = cleaned_content.split('\n')
                    non_empty_lines = [line for line in lines if line.strip() != '']

                    if any(keyword in cleaned_content.lower() for keyword in copyright_keywords):
                        print(f"File {file_name} detected as a copyright page, skipping.")
                        skipped_files.append(full_file_path)
                        continue

                    if len(non_empty_lines) < 5 or (sum(len(line) for line in non_empty_lines) / len(non_empty_lines)) < 40:
                        print(f"File {file_name} seems to be an index or footnote, skipping.")
                        skipped_files.append(full_file_path)
                        continue

                    output_file = self.base_path / f"{Path(file_name).stem}.txt"
                    with open(output_file, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(cleaned_content)
                    processed_files.append(output_file.name)

                # Remove the original file after processing
                try:
                    full_file_path.unlink()
                except PermissionError as e:
                    print(f"Error deleting file {full_file_path}: {e}")
            else:
                print(f"File {file_name} not found, skipping.")
                skipped_files.append(full_file_path)
        
        # Remove skipped files
        for file_path in skipped_files:
            try:
                file_path.unlink()
            except PermissionError as e:
                print(f"Error deleting skipped file {file_path}: {e}")

        # Update files_order.txt with processed files only
        with open(self.order_file, 'w', encoding='utf-8') as order_file:
            for file in processed_files:
                order_file.write(file + "\n")
        return processed_files

def process_epub(book_path, character_limit):
    book_path = Path(book_path)
    if book_path.is_dir():
        print(f"----Processing files in {book_path}----")
        processor = EpubProcessor(book_path, character_limit)
        processor.process_files()
