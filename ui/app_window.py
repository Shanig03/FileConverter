import customtkinter as ctk
import threading
import time
from tkinter import filedialog 

# Fixes the 'BatchProcessor is not defined' error
from core.batch_processor import BatchProcessor 

# Import the converter strategy
from converters.video_to_audio import VideoToAudioConverter
# from converters.pdf_to_image import PdfToImageConverter
# from converters.image_to_pdf import ImageToPdfConverter

# Set the overall appearance and color theme of the CustomTkinter UI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppWindow:
    def __init__(self):
        # Initialize the main application window
        self.root = ctk.CTk()
        self.root.title("Concurrent File Converter")
        self.root.geometry("500x400")
        
        # Build the user interface elements
        self.setup_ui()

    def setup_ui(self):
        # Main title label
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="File Converter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(30, 20))

        # Dropdown menu to select the desired conversion strategy
        self.conversion_type_combo = ctk.CTkComboBox(
            self.root, 
            values=["PDF to Image", "Image to PDF", "Video to Audio (MP3)"],
            width=250
        )
        self.conversion_type_combo.pack(pady=15)

        # Button to trigger the conversion process
        self.convert_btn = ctk.CTkButton(
            self.root, 
            text="Start Conversion", 
            command=self.on_start_conversion_clicked,
            width=200,
            height=40
        )
        self.convert_btn.pack(pady=20)

        # Status label to provide feedback to the user
        self.status_label = ctk.CTkLabel(
            self.root, 
            text="Ready to convert", 
            text_color="gray"
        )
        self.status_label.pack(pady=10)

    def on_start_conversion_clicked(self):
        # Disable the button to prevent multiple concurrent clicks
        self.convert_btn.configure(state="disabled")
        self.status_label.configure(text="Processing... Please wait", text_color="orange")

        # Spawn a background thread to handle the heavy lifting
        # This prevents the main UI loop from freezing
        worker_thread = threading.Thread(target=self._run_conversion_thread, daemon=True)
        worker_thread.start()

    def _run_conversion_thread(self):
        # Retrieve the selected conversion type from the UI combo box
        selected_type = self.conversion_type_combo.get()
        print(f"User selected: {selected_type}")

        # 1. Ask the user to select input files
        # Returns a tuple of file paths, or an empty tuple if cancelled
        input_files = filedialog.askopenfilenames(
            title="Select files to convert"
        )
        
        # Check if the user clicked 'Cancel' in the file dialog
        if not input_files:
            print("No input files selected. Aborting.")
            self.root.after(0, self._on_conversion_aborted)
            return

        # Ask the user to select a destination folder for the converted files
        output_folder = filedialog.askdirectory(
            title="Select destination folder"
        )

        # Check if the user clicked 'Cancel' in the folder dialog
        if not output_folder:
            print("No destination folder selected. Aborting.")
            self.root.after(0, self._on_conversion_aborted)
            return

        # 2. Instantiate the correct Converter class based on user selection
        converter = None
        if selected_type == "Video to Audio (MP3)":
            converter = VideoToAudioConverter()
        elif selected_type == "PDF to Image":
            # converter = PdfToImageConverter() # Uncomment when implemented
            pass
        elif selected_type == "Image to PDF":
            # converter = ImageToPdfConverter() # Uncomment when implemented
            pass
            
        # Safety check in case a strategy is not yet implemented
        if not converter:
            print(f"Converter for '{selected_type}' is not implemented yet.")
            self.root.after(0, self._on_conversion_aborted)
            return

        # 3. Instantiate the BatchProcessor and run the parallel conversion
        try:
            processor = BatchProcessor(converter=converter, output_folder=output_folder)
            
            # This is a blocking call, but since we are in a background thread, 
            # the UI remains fully responsive!
            results = processor.process_files(input_files)
            
            print(f"Successfully processed {len(results)} files.")
            
            # Safely schedule the success UI update back on the main thread
            self.root.after(0, self._on_conversion_finished)
            
        except Exception as e:
            print(f"A critical error occurred during batch processing: {e}")
            self.root.after(0, self._on_conversion_aborted)

    def _on_conversion_aborted(self):
        # Restore the UI elements if the user cancels or an error occurs
        self.status_label.configure(text="Conversion Cancelled or Failed", text_color="red")
        self.convert_btn.configure(state="normal")

    def run(self):
        # Start the main event loop of the CustomTkinter window
        self.root.mainloop()