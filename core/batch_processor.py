import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from converters.base_converter import BaseConverter

# Global helper function for the ProcessPoolExecutor
def _process_single_file(converter: BaseConverter, input_file: str, output_folder: str):
    # Execute the conversion logic specific to the passed converter
    return converter.convert(input_file, output_folder)

class BatchProcessor:
    def __init__(self, converter: BaseConverter, output_folder: str):
        # Inject the desired converter strategy and set the destination
        self.converter = converter
        self.output_folder = output_folder
        
        # Ensure the destination folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def process_files(self, file_paths: list):
        results = []
        
        # Execute the conversion in parallel using multiple CPU cores
        with ProcessPoolExecutor() as executor:
            # Map each file to a parallel future task
            futures = {
                executor.submit(_process_single_file, self.converter, path, self.output_folder): path 
                for path in file_paths
            }
            
            # Yield results as soon as they finish processing
            for future in as_completed(futures):
                try:
                    result_path = future.result()
                    results.append(result_path)
                    # TODO: Trigger a UI callback here to update a progress bar
                except Exception as e:
                    original_path = futures[future]
                    print(f"Failed to process {original_path}: {e}")
                    
        return results