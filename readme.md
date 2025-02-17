# unMark - Process Manager

A lightweight Windows app solely designed to kill and start MarkAny services (Document SAFER 5.0 and IMG SAFER 5.0)

![unMark Icon](unmark-ico.ico)

## Features
- **Process Monitoring**: 
- **Sortable Interface**: Sort processes by any column (Name, PID, Username, Memory)
- **Tooltips**: Helpful tooltips on all controls for better usability

## Requirements

- Windows OS
- Administrative privileges (required for service management)
- Python 3.9+ (if running from source)

## Installation

### Option 1: Download Executable
1. Download the latest release from the Releases page
2. Run `unmark.exe` (requires admin privileges)

### Option 2: Run from Source
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage
1. Start the application (requires admin privileges)
2. Scan for processes by clicking "Check"
3. Terminate processes by clicking "Terminate" (Does not need to click "Check" first)
4. Start services by selecting them and clicking "Start" (Does not need to click "Check" first)


