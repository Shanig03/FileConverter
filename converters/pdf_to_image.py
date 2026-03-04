import os
from pdf2image import convert_from_path
from .base_converter import BaseConverter

class PdfToImageConverter(BaseConverter):
    
    def convert(self, input_file_path: str, output_folder_path: str) -> str:
        # Extract the base file name without the extension
        file_name = os.path.basename(input_file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        try:
            # Update this path to exactly where you extracted the poppler 'bin' folder on your machine
            POPPLER_BIN_PATH = r"C:\poppler\poppler-25.12.0\Library\bin" 
            
            # Convert the PDF file using the explicit poppler path for Windows
            pages = convert_from_path(input_file_path, poppler_path=POPPLER_BIN_PATH)
            
            if not pages:
                raise ValueError("The PDF file is empty or could not be read.")
                
            # Iterate through all pages and save them as individual JPEG files
            for i, page in enumerate(pages):
                output_file_path = os.path.join(output_folder_path, f"{name_without_ext}_page_{i+1}.jpg")
                page.save(output_file_path, 'JPEG')
                
            return f"Saved {len(pages)} images for {file_name} in {output_folder_path}"
            
        except Exception as e:
            # Raise a descriptive error if the conversion fails
            raise RuntimeError(f"Failed to convert PDF to image: {e}")