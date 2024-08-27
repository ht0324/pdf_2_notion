import asyncio
import sys
import subprocess
from utils.pdf_preprocessing import read_txt, determine_total_pages, process_chunk, copy_to_clipboard, process_chunk_ocr, calculate_page_ranges
from utils.api import query

MODEL_ANTHROPIC = "claude-3-5-sonnet-20240620"
MODEL_OPENAI = "gpt-4-turbo"

def parse_args():
    if len(sys.argv) < 6:
        print("Usage: python3 pdf_to_writing.py <system_prompt_file_path> <model> <first_pagenum> <end_pagenum> <chunk_num>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

async def process_pdf(system_prompt, model, first_pagenum, end_pagenum, chunk_num, user_prompt_file_path):
    page_ranges = calculate_page_ranges(first_pagenum, end_pagenum, chunk_num)
    tasks = []
    for i, (start_page, end_page) in enumerate(page_ranges):
        # task = asyncio.create_task(process_chunk(user_prompt_file_path, start_page, end_page, system_prompt, model))
        task = asyncio.create_task(process_chunk_ocr(user_prompt_file_path, start_page, end_page, system_prompt, model))
        tasks.append(task)
        print(f"Processing chunk {i + 1} of {chunk_num} from page {start_page} to page {end_page}...")
        print("")

    # sleep for 20.5 seconds to avoid rate limiting
    await asyncio.sleep(20.5)
    
    responses = await asyncio.gather(*tasks)
    return "\n\n".join(responses)

async def main():
    system_prompt_file_path, model, first_pagenum, end_pagenum, chunk_num = parse_args()
    system_prompt = read_txt(system_prompt_file_path)
    models = {"openai": MODEL_OPENAI, "anthropic": MODEL_ANTHROPIC}
    model = models.get(model, MODEL_ANTHROPIC)
    user_prompt_file_path = input("Enter the user prompt file path: ")

    if end_pagenum == 0:
        end_pagenum = determine_total_pages(user_prompt_file_path)

    try:
        concatenated_response = await process_pdf(system_prompt, model, first_pagenum, end_pagenum, chunk_num, user_prompt_file_path)
        print("Done!")
        response_filename = user_prompt_file_path.split("/")[-1].split(".")[0] + "_response.txt"
        with open("response/" + response_filename, "w") as file:
            file.write(concatenated_response)
        print(f"\nResponse saved in: {response_filename}")
        copy_to_clipboard(concatenated_response)
    except FileNotFoundError:
        print(f"File not found: {user_prompt_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())