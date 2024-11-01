import os
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_pages_with_tables_or_images(pdf_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all PDF files in the specified folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing '{filename}'...")

            # Open the PDF file
            with pdfplumber.open(pdf_path) as pdf:
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    has_table = page.extract_tables()
                    has_image = page.images

                    # Check if the page contains tables or images
                    if has_table or has_image:
                        print(f"Extracting page {page_number + 1} from '{filename}'.")

                        # Create a new PDF writer object
                        writer = PdfWriter()
                        
                        # Add the page using PdfReader
                        reader = PdfReader(pdf_path)
                        writer.add_page(reader.pages[page_number])

                        # Save the page to a new PDF file
                        output_pdf_path = os.path.join(output_folder, f"{filename[:-4]}_page_{page_number + 1}.pdf")
                        with open(output_pdf_path, "wb") as output_pdf:
                            writer.write(output_pdf)

# Paths
pdf_folder = "/home/kyle/Desktop/no_git/zainab_human_rights_project/justin_pdf"

output_folder = "/home/kyle/Desktop/no_git/zainab_human_rights_project/pdf_output"

# Call the function to extract pages
extract_pages_with_tables_or_images(pdf_folder, output_folder)
print("Extraction complete.")
