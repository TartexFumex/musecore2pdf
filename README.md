# musecore2pdf

##Notes
A graphical interface has been added, you just have to run the gui.py file.

## Description
The `musecore2pdf` program is designed to convert MuseScore sheet music URLs into PDF files. It utilizes Selenium, ReportLab, and other Python libraries to automate the process of rendering each page of the MuseScore sheet music and saving them as a single PDF file. The script handles various scenarios, including the display of both SVG and PNG images on the MuseScore webpage.

## Prerequisites
- Python 3.x
- Chrome browser
- ChromeDriver (Ensure it's in your system PATH)
- Required Python libraries: `selenium`, `svglib`, `reportlab`, `PyPDF2`

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/TartexFumex/musecore2pdf
   cd musecore2pdf
   ```

2. **Install the required Python libraries:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `config.conf`:**
   - Set the `url` to the MuseScore sheet music URL.
   - Adjust other parameters like `render_path` and `file_name` as needed.

## Usage
Run the script using the following command:
```bash
python musecore2pdf.py
```

## Configuration
Modify the `config.conf` file to customize the script behavior:
```ini
[general]
url = https://musescore.com/sheetmusic/some-sheet-music
render_path = /path/to/render
file_name = output.pdf
```

Feel free to contribute or report issues!
