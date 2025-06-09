# UBC Science Advising Queue Sniper

UBC Science Advising Queue Sniper is a Python script for Windows that automates the process of joining the UBC Science Advising virtual (Zoom) queue. It allows users to specify a target (opening) time and automatically clicks the buttons + fills out the form with millisecond precision.

## Demo



## Installation

1. Install Python 3.12.
2. Initialize a virtual environment and install the required dependencies by running:
```bash
pip install -r requirements.txt
```
3. **Find your version of Google Chrome and download the corresponding ChromeDriver version [here](https://googlechromelabs.github.io/chrome-for-testing/)**. 
4. Move `chromedriver.exe` into the project folder (at the same level as `main.py`).

## Usage

1. Open `main.py` and modify the `hour` and `minute` variables to match the Science Advising opening time in PST (24-hour time). These variables are marked with the comment: `### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME IN PST (24-hour time) ###`.
2. In `main.py`, fill in the `preferred_name`, `last_initial`, `phone_number`, `inquiry_type`, `student_number`, and `sent_message` variables to match your information. These variables are marked with the comment: `### ENTER REQUIRED INFORMATION BELOW AS STRINGS ###`.
3. Run the `main.py`. **You will be prompted to run the program as Administrator so that your computer time can be automatically synced.**
4. Press `Enter` in the terminal to start the script.
5. The script will wait until the specified opening time to refresh the page and automatically join the queue.