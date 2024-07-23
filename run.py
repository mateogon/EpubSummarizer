import sys
from pathlib import Path
from epub_extractor import extract
from consolidate_epub import consolidate

def main(path):
    character_limit = 9999999999

    # Extract files from the specified .epub file or directory
    extract(path)

    # Consolidate .xhtml files into text files
    path = Path(path)
    books_folder = Path('books')
    if path.is_dir():
        for epub_file in path.glob('*.epub'):
            book_folder = books_folder / "".join([c for c in epub_file.stem if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            if book_folder.exists():
                consolidate(book_folder, character_limit)
    elif path.is_file() and path.suffix == '.epub':
        book_folder = books_folder / "".join([c for c in path.stem if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        if book_folder.exists():
            consolidate(book_folder, character_limit)
    else:
        print(f"Invalid path or no .epub files found in: {path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run.py <path_to_epub_file_or_folder>")
    else:
        path = sys.argv[1]
        main(path)