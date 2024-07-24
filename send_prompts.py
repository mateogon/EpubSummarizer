import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

class PromptProcessor:
    def __init__(self, book_path, api_key):
        self.book_path = Path(book_path)
        self.order_file = self.book_path / "files_order.txt"
        self.base_prompt_file = "base_prompt.txt"
        self.responses_dir = self.book_path / "responses"
        self.responses_dir.mkdir(exist_ok=True)
        self.client = OpenAI(api_key=api_key)
        self.base_prompt = self.read_base_prompt()

    def read_order_file(self):
        with open(self.order_file, 'r', encoding='utf-8') as file:
            order = file.readlines()
        return [x.strip() for x in order]

    def read_base_prompt(self):
        with open(self.base_prompt_file, 'r', encoding='utf-8') as file:
            base_prompt = file.read()
        return base_prompt

    def read_file_content(self, file_name):
        file_path = self.book_path / file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def process_files(self):
        ordered_files = self.read_order_file()
        total_files = len(ordered_files)
        print(f"Processing {total_files} files...")
        
        for i, file_name in enumerate(ordered_files, 1):
            print(f"Reading file {i}/{total_files}: {file_name}")
            content = self.read_file_content(file_name)
            full_prompt = f"{self.base_prompt}\n\n{content}"
            print(f"Sending prompt for file {i}/{total_files}")
            response = self.send_prompt(full_prompt)
            response_file = self.responses_dir / f"{Path(file_name).stem}_response.md"
            with open(response_file, 'w', encoding='utf-8') as file:
                file.write(response)
            print(f"Response for file {i}/{total_files} saved to {response_file}")

        print("All files processed successfully.")

def main(book_folder):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return
    
    prompt_processor = PromptProcessor(book_folder, api_key)
    prompt_processor.process_files()
    print(f"Responses saved in {prompt_processor.responses_dir}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python send_prompts.py <path_to_consolidated_book_folder>")
    else:
        book_folder = sys.argv[1]
        main(book_folder)
