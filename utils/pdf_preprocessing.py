import fitz  # PyMuPDF
import asyncio
import base64
import itertools
from pdf2image import convert_from_path
from PIL import Image
import subprocess
import random
import io
import sys
from utils.api import query
from anthropic import AsyncAnthropic


ocr_client = AsyncAnthropic(api_key="YOUR_ANTHROPIC_API_KEY")

async def display_spinner(task):
    async def spinner():
        for frame in itertools.cycle('|/-\\'):
            sys.stdout.write(f'\rProcessing: {frame}')
            sys.stdout.flush()
            await asyncio.sleep(0.1)

    spinner_task = asyncio.create_task(spinner())
    try:
        result = await task
    finally:
        spinner_task.cancel()
        sys.stdout.write('\r' + ' ' * (len('Processing: ') + 1) + '\r')
        sys.stdout.flush()
    return result

async def process_chunk(pdf_path, start_page, end_page, system_prompt, model):
    user_prompt = pdf_to_text(pdf_path, start_page, end_page)
    user_prompt += "\n\n<instruction>"+ system_prompt +"</instruction>"
    system_prompt = ""

    response = await display_spinner(query(model, system_prompt, user_prompt))
    print(f"\nChunk response (start_page: {start_page}, end_page: {end_page}): {response[:50]}\n")
    return response

def pdf_to_text(pdf_pathname, first_page_num=0, last_page_num=None):
    # Initialize an string with a filename to accumulate text from each page
    pdf_filename = pdf_pathname.split("/")[-1]
    accumulated_text = "Filename: " + pdf_filename + "\n"

    # Open the PDF file
    with fitz.open(pdf_pathname) as pdf:
        # Iterate over each page in the PDF file
        if last_page_num is None:
            last_page_num = pdf.page_count - 1
        for page_num in range(first_page_num, last_page_num + 1):
            print(f"Processing page {page_num + 1}...")
            page = pdf[page_num]
            # Extract text from the page
            text = page.get_text()
            # Append the text to the accumulated text
            accumulated_text += f"Page {page_num + 1}:\n{text}\n"

    return accumulated_text

def determine_total_pages(pdf_pathname):
    with fitz.open(pdf_pathname) as pdf:
        return pdf.page_count
    
def read_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def copy_to_clipboard(text):
    cmd = "pbcopy"
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = proc.communicate(input=text.encode('utf-8'))

    if proc.returncode == 0:
        print("\nResponse copied to clipboard successfully.\n")
    else:
        print(f"\nError copying to clipboard: {stderr_value.decode('utf-8')}")

async def spinner(delay, message):
    spinner_chars = itertools.cycle('|/-\\')
    while True:
        sys.stdout.write(f'\r{next(spinner_chars)} {message}')
        sys.stdout.flush()
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            break
    sys.stdout.write('\r')
    sys.stdout.flush()

async def display_progress(task, message):
    spinner_task = asyncio.create_task(spinner(0.2, message))
    try:
        result = await task
    finally:
        spinner_task.cancel()
    return result

async def process_chunk_ocr(pdf_path, start_page, end_page, system_prompt, model):
    print(f"Converting pages {start_page} to {end_page} to images...")
    images_base64 = await display_progress(asyncio.to_thread(pdf_to_images_base64, pdf_path, start_page, end_page), "Converting PDF to images...")
    
    print(f"Performing OCR on pages {start_page} to {end_page}...")
    ocr_tasks = []
    for i, image_base64 in enumerate(images_base64, start=start_page):
        message_list = [
            {
                "role": 'user',
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_base64}},
                    {"type": "text", "text": f"Transcribe this lecture slide for pages {i} and {i+1}. Please present the given text, code, and table in markdown format. Output only the transcription."}
                ]
            }
        ]

        ocr_task = ocr_client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=1000,
            messages=message_list,
            temperature=0.0
        )
        ocr_tasks.append(ocr_task)

    # ocr_results = await display_progress(asyncio.gather(*ocr_tasks), "Performing OCR...")
    # query the model sequentially, waiting for 0.5 seconds between each query
    ocr_results = []
    for ocr_task in ocr_tasks:
        ocr_result = asyncio.create_task(ocr_task)
        ocr_results.append(await display_progress(ocr_result, "Performing OCR..."))
        # await asyncio.sleep(0.5)

    
    user_prompt = "\n".join([result.content[0].text for result in ocr_results])
    
    print(f"Querying the model for pages {start_page} to {end_page}...")


    user_prompt += "\n\n<instruction>"+ system_prompt +"</instruction>"
    system_prompt = ""
    
    response = await display_progress(query(model, system_prompt, user_prompt), "Querying the model...")
    
    print(f"\nChunk response (start_page: {start_page}, end_page: {end_page}): {response[:20]}\n")
    return response

def pdf_to_images_base64(file_path, start_page, end_page):
    pages = convert_from_path(file_path, dpi=200, first_page=start_page, last_page=end_page)
    images_base64 = []
    for i in range(0, len(pages), 2):
        if i == len(pages) - 1:
            images_base64.append(image_to_base64(pages[i]))
            break
        first_page = pages[i]
        second_page = pages[i + 1]
        # downscale first and second page 4 times
        first_page = first_page.resize((first_page.width // 4, first_page.height // 4))
        second_page = second_page.resize((second_page.width // 4, second_page.height // 4))

        total_height = first_page.height + second_page.height
        combined_image = Image.new('RGB', (first_page.width, total_height))
        combined_image.paste(first_page, (0, 0))
        combined_image.paste(second_page, (0, first_page.height))
        images_base64.append(image_to_base64(combined_image))


    return images_base64

def image_to_base64(pil_img):
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

def calculate_page_ranges(first_pagenum, end_pagenum, chunk_num):
    total_pages_to_process = end_pagenum - first_pagenum + 1
    base_pages_per_chunk = total_pages_to_process // chunk_num
    remainder_pages = total_pages_to_process % chunk_num
    ranges = []
    for i in range(chunk_num):
        start_page = first_pagenum + i * base_pages_per_chunk + min(i, remainder_pages)
        end_page = start_page + base_pages_per_chunk - 1 + (1 if i < remainder_pages else 0)
        if i == chunk_num - 1:
            end_page = end_pagenum
        ranges.append((start_page, end_page))
    return ranges