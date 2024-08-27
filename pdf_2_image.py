from pdf2image import convert_from_path
import os

def pdf_to_images(file_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert each page of the PDF to an image
    pages = convert_from_path(file_path, dpi=200)
    
    # Loop through each page in the pages list
    for i, page in enumerate(pages):
        # Construct image file path
        image_file_path = os.path.join(output_folder, f'page_{i + 1}.png')
        
        # Save the image to the file system
        page.save(image_file_path, 'PNG')

        print(f'Saved page {i + 1} as {image_file_path}')

# take input from terminal
input = input("Enter the file path: ")

# strip the input file and make the output folder
output = input.split('.')[0]

# Example usage
pdf_to_images(input, output)
