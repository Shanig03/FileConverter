from abc import ABC, abstractmethod

# Abstract base class to enforce a strict contract for all file converters
class BaseConverter(ABC):
    
    @abstractmethod
    def convert(self, input_file_path: str, output_folder_path: str) -> str:
        # Convert the file and return the path to the newly created file
        pass