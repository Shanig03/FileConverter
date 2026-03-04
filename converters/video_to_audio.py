import os
# Updated import for newer versions of MoviePy (v2.0+)
from moviepy import VideoFileClip
from .base_converter import BaseConverter

class VideoToAudioConverter(BaseConverter):
    
    def convert(self, input_file_path: str, output_folder_path: str) -> str:
        # Extract the base file name without the extension
        file_name = os.path.basename(input_file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        # Define the new output path with the .mp3 extension
        output_file_path = os.path.join(output_folder_path, f"{name_without_ext}.mp3")
        
        try:
            # Load the video file into memory
            video_clip = VideoFileClip(input_file_path)
            
            # Extract the audio track and write it to the output file
            # logger=None prevents moviepy from spamming the console with progress bars
            video_clip.audio.write_audiofile(output_file_path, logger=None)
            
            # Close the resources to free up memory
            video_clip.audio.close()
            video_clip.close()
            
            return output_file_path
            
        except Exception as e:
            # Raise a descriptive error if the conversion fails
            raise RuntimeError(f"Failed to convert video to audio: {e}")