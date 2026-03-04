import os
from pypdf import PdfWriter
from .base_converter import BaseConverter

class MergePdfsConverter(BaseConverter):
    
    def convert(self, input_file_paths: list, output_folder_path: str) -> str:
        # Initialize the PDF writer object
        merger = PdfWriter()
        
        # Define the name for the output merged file
        output_file_path = os.path.join(output_folder_path, "Merged_Document.pdf")
        
        try:
            # Iterate through the provided list of PDF paths
            for pdf_path in input_file_paths:
                # Append each PDF to the merger in the order they were selected
                merger.append(pdf_path)
            
            # Write the final merged content to the destination
            merger.write(output_file_path)
            
            # Close the merger object to free up system resources
            merger.close()
            
            return output_file_path
            
        except Exception as e:
            # Raise a descriptive error if the merge process fails
            raise RuntimeError(f"Failed to merge PDF files: {e}")