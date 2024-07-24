import os
from pathlib import Path

def convert_txt_to_md(folder_path):
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"Invalid folder path: {folder_path}")
        return
    
    txt_files = list(folder.glob('*.txt'))
    if not txt_files:
        print(f"No .txt files found in: {folder_path}")
        return
    
    for txt_file in txt_files:
        md_file = txt_file.with_suffix('.md')
        txt_file.rename(md_file)
        print(f"Converted {txt_file} to {md_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python convert_txt_to_md.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        convert_txt_to_md(folder_path)
