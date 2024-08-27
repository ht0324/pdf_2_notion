from utils.pdf_preprocessing import pdf_to_text
import subprocess
import asyncio

async def main():
    file_path = input("Enter the user prompt file path: ")
    text = pdf_to_text(file_path)

    cmd = "pbcopy"
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = proc.communicate(input=text.encode('utf-8'))

    if proc.returncode == 0:
        print("\nResponse copied to clipboard successfully.\n")
    else:
        print(f"\nError copying to clipboard: {stderr_value.decode('utf-8')}")

if __name__ == "__main__":
    asyncio.run(main())