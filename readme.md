# unMark - Process Manager

A lightweight Windows app solely designed to kill and start MarkAny services (Document SAFER 5.0 and IMG SAFER 5.0)

![unMark Icon](unmark-ico.ico)

I am not responsible for any damages done to your system due to this program. By using this, you agree to use this program in a safe and legal method.

## Features
- **Manage MarkAny Processes**: Monitor, kill, and start MarkAny processes
- **Sortable Interface**: Sort processes by any column (Name, PID, Username, Memory)
- **Word/Excel Add In Control**: Disable / Enable the MarkAny Document SAFER DRM add in

## Requirements

- Windows
- Administrative privileges
- Python 3

## Installation

### Option 1: Download Executable
1. Download the latest release from the Releases page
2. Run `unmark.exe`

### Option 2: Run from Source
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage
1. Start the application (requires admin privileges)
2. Scan for processes by clicking "Check"
3. Terminate processes by clicking "Terminate" (Does not need to click "Check" first)
4. Start services by selecting them and clicking "Start" (Does not need to click "Check" first)
5. For the Word/Excel add in control, go to the other tabs and enter the appropriate Word/Excel versions & Document SAFER directory


