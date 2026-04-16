# Smart OCR Pro

Smart OCR Pro is a professional desktop application designed to extract text from images and PDF files with high precision. Built using Python and PyQt6, the tool specializes in organizing extracted data into structured Word and Excel formats. It is specifically optimized for Arabic, English, and German languages.

## Key Features
- Multi-language Support: High-accuracy OCR for Arabic, English, and German via the Tesseract engine.
- Data Export: Direct conversion of extracted text into organized .docx and .xlsx files.
- Modern Interface: A streamlined Dark Mode UI developed for professional workflows.
- PDF Processing: Integrated capability to convert and analyze PDF documents.

## System Requirements
This project was developed and tested on CachyOS (Arch Linux). The following system-level dependencies are required:

```bash
sudo pacman -S tesseract tesseract-data-ara tesseract-data-deu poppler
Installation and Usage
Clone the repository:git clone [https://github.com/Mahm0udhazem/Smart-OCR-Pro.git](https://github.com/Mahm0udhazem/Smart-OCR-Pro.git)
cd Smart-OCR-Pro
Set up the virtual environment:python -m venv venv
source venv/bin/activate.fish  # For Fish shell users
Install Python dependencies:pip install -r requirements.txt
Run the application:python "print(1).py"
Project Structure
print(1).py: The main application script containing the UI and OCR logic.

requirements.txt: List of necessary Python libraries for the environment.

.gitignore: Configuration to exclude virtual environments and temporary files from version control.

LICENSE: MIT License for open-source distribution.

Security Overview
As a tool developed with a focus on data privacy, all OCR processing is performed locally on the user's machine. No data is transmitted to external servers, ensuring the confidentiality of processed documents.

Developed by: Mahmoud Hazem
