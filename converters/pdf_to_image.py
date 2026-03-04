import os
import sys
from pdf2image import convert_from_path
from .base_converter import BaseConverter

class PdfToImageConverter(BaseConverter):
    
    def _get_poppler_path(self):
        # Check if the application is running as a bundled executable
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller extracts bundled files to a temporary folder called sys._MEIPASS
            return os.path.join(sys._MEIPASS, 'poppler')
        else:
            # When running as a normal Python script, use the local development path
            # IMPORTANT: Make sure this matches your local poppler bin path!
            return r"C:\poppler\poppler-24.02.0\Library\bin"
        
    def convert(self, input_file_path: str, output_folder_path: str) -> str:
        # Extract the base file name without the extension
        file_name = os.path.basename(input_file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        try:
            # Update this path to exactly where you extracted the poppler 'bin' folder on your machine
            POPPLER_BIN_PATH = self._get_poppler_path() 
            
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