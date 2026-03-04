import os
from PIL import Image
from .base_converter import BaseConverter

class ImageToPdfConverter(BaseConverter):
    
    def convert(self, input_file_path: str, output_folder_path: str) -> str:
        # Extract the base file name without the extension
        file_name = os.path.basename(input_file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        # Define the new output path with the .pdf extension
        output_file_path = os.path.join(output_folder_path, f"{name_without_ext}.pdf")
        
        try:
            # Open the image using Pillow
            image = Image.open(input_file_path)
            
            # Convert the image to RGB mode if it is not already (e.g., RGBA or P)
            # This is required because PDFs do not support transparency in the same way
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Save the image as a PDF file
            image.save(output_file_path, "PDF", resolution=100.0)
            
            return output_file_path
            
        except Exception as e:
            # Raise a descriptive error if the conversion fails
            raise RuntimeError(f"Failed to convert image to PDF: {e}")