# EpubSummarizer

EpubSummarizer is a tool designed to extract content from EPUB files, consolidate the extracted content into text files, and summarize the chapters using the OpenAI API. The summaries highlight key ideas, golden nuggets, practical and applicable principles, and paradigms and thinking models.

## Features

- Extract content from single or multiple EPUB files.
- Clean and consolidate extracted content into plain text files.
- Summarize chapters with key ideas, golden nuggets, practical advice, and paradigms.

## Prerequisites

- Python 3.x
- OpenAI API Key

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd EpubSummarizer
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory to store your OpenAI API key:
   ```sh
   echo OPENAI_API_KEY=your-api-key > .env
   ```

## Usage

### Extracting EPUB Files

To extract content from an EPUB file or a directory containing EPUB files, use the `run.py` script.

1. Extract a single EPUB file:

   ```sh
   python run.py path/to/your/file.epub
   ```

2. Extract multiple EPUB files in a directory:
   ```sh
   python run.py path/to/your/directory
   ```

The extracted files will be saved in the `books` directory.

### Consolidating Extracted Content

The `consolidate_epub.py` script consolidates the extracted XHTML and HTML files into text files and saves them in the same `books` directory.

1. Run the consolidation process (this is done automatically after extraction if using `run.py`):
   ```sh
   python consolidate_epub.py path/to/extracted/book/folder
   ```

### Summarizing Chapters

To summarize the chapters of the book, use the `send_prompts.py` script. This script reads the extracted and consolidated text files, sends them to the OpenAI API, and saves the responses in the `responses` folder.

1. Make sure your `base_prompt.txt` is in the same folder as the `send_prompts.py` script.

2. Run the summarization process:
   ```sh
   python send_prompts.py path/to/consolidated/book/folder
   ```

The summaries will be saved in the `responses` directory within the specified book folder.

## Base Prompt

The `base_prompt.txt` file should contain the prompt you want to use for summarizing the chapters. Here is an example prompt:

```

You are an expert in book summarization. Please summarize the given chapter of the book with the following details:

- **Key Ideas**: Highlight the main points and arguments presented.
- **Golden Nuggets**: Extract the most valuable and insightful quotes or concepts.
- **Practical and Applicable**: Identify the principles or advice that can be immediately applied in real life.
- **Paradigms and Thinking Models**: Outline the paradigms or thinking models introduced or discussed in the chapter.

Ensure the summary is concise, clear, and well-structured. Use bullet points for key ideas and golden nuggets for ease of understanding, and provide actionable steps where applicable. Focus on delivering value that can be applied across different disciplines.

```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

```

```
