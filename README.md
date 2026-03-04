# Concurrent File Converter Pro

A modern, high-performance desktop application built with Python and CustomTkinter for bulk file conversions. 

Unlike standard, single-threaded scripts, this application leverages Python's `ProcessPoolExecutor` to process multiple files concurrently, utilizing all available CPU cores. The codebase is strictly organized using the **Strategy Design Pattern**, ensuring that adding new conversion types is seamless and decoupled from the core engine.

## Key Features
* **Concurrent Processing:** Bypasses the Global Interpreter Lock (GIL) using multiprocessing for heavy CPU-bound tasks (like rendering PDFs or extracting audio).
* **Strategy Design Pattern:** Converters implement a strict `BaseConverter` interface, making the architecture highly modular and maintainable.
* **Modern GUI:** A clean, responsive, dark-mode-enabled interface built with `CustomTkinter`.
* **Asynchronous UI:** Background threading ensures the GUI remains fully responsive during heavy batch processing.
* **Supported Conversions:**
  * Video to Audio (MP3) extraction
  * PDF to Image (JPEG) rendering
  * Image to PDF compilation

## Architecture
* `ui/` - Handles the user interface and main event loop.
* `core/` - Contains the `BatchProcessor` which manages the multiprocessing pool.
* `converters/` - Contains isolated conversion strategies inheriting from a unified base class.

## Prerequisites & Installation

### 1. Python Dependencies
Ensure you have Python 3 installed, then run:
```bash
pip install moviepy pdf2image Pillow customtkinter
```
### 2. System Dependencies (Poppler for PDF Conversion)
To convert PDFs to images, the pdf2image library requires Poppler.

- Windows: Download the latest Poppler for Windows, extract it, and ensure the bin path is correctly referenced in converters/pdf_to_image.py.

-  Linux (Ubuntu/Debian): 
```bash
sudo apt-get install poppler-utils
```
## How to Run
Start the application by running the main entry point:
```bash
python main.py
```
