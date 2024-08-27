# PDF to Notion

This repository contains a set of Python scripts designed to process PDF files, particularly lecture slides, and generate distilled notes based on user-defined prompts. The project uses OCR and AI-powered text generation to create personalized summaries and explanations of PDF content.

## Features

- Convert PDF to images
- Extract text from PDFs
- Process PDFs using OCR for better text recognition
- Generate AI-powered summaries and explanations
- Customizable system prompts for different output styles
- Support for both OpenAI and Anthropic AI models

## Prerequisites

- Python 3.9+
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pdf_2_notion.git
   cd pdf_2_notion
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   - Open `utils/api.py`
   - Replace `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` with your actual API keys

## Usage

### PDF to Images

To convert a PDF to images:

```
python pdf_2_image.py
```

You will be prompted to enter the file path of the PDF. The script will create a folder with the same name as the PDF file and save each page as a separate PNG image.

### PDF to Text

To extract text from a PDF:

```
python pdf_to_text.py
```

You will be prompted to enter the file path of the PDF. The extracted text will be copied to your clipboard.

### PDF to Writing (Main Script)

This is the main script that processes PDFs and generates summaries:

```
python pdf_to_writing.py <system_prompt_file_path> <model> <first_pagenum> <end_pagenum> <chunk_num>
```

- `<system_prompt_file_path>`: Path to the system prompt file (found in the `system_prompt` folder)
- `<model>`: Choose between "openai" (for GPT-4 Turbo) or "anthropic" (for Claude 3 Sonnet)
- `<first_pagenum>`: Starting page number (0-indexed)
- `<end_pagenum>`: Ending page number (0-indexed, use 0 for all pages)
- `<chunk_num>`: Number of chunks to split the PDF into for processing

Example:
```
python pdf_to_writing.py system_prompt/pdf_to_notion_eng_3.txt anthropic 0 0 3
```

You will then be prompted to enter the path to the PDF file you want to process.

The script will:
1. Convert the PDF pages to images
2. Perform OCR on the images
3. Generate summaries based on the system prompt
4. Save the output in the `response` folder and copy it to your clipboard

I have included a sample prompt and a few response that I have used personally for my study. You can find them in the `system_prompt` and `response` folders.

## Customizing Prompts

You can create your own system prompts in the `system_prompt` folder. These prompts guide the AI in generating summaries and explanations. Existing prompts include:

- `pdf_cleaner.txt`: For cleaning and formatting PDF text
- `pdf_explainer.txt`: For generating explanations of PDF content
- `pdf_to_notion_eng_3.txt`: For creating English summaries suitable for Notion
- `pdf_to_notion_kor.txt`: For creating Korean summaries
- `transcript_to_blog.txt`: For converting transcripts to blog-style content

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
