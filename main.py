import time as time_obj
from datetime import datetime, time
from zoneinfo import ZoneInfo
import subprocess
import sys
import ctypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def set_chrome_settings():
    chrome_options = Options()
    args = [
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-client-side-phishing-detection",
        "--disable-default-apps",
        "--disable-hang-monitor",
        "--disable-popup-blocking",
        "--disable-prompt-on-repost",
        "--disable-translate",
        "--disable-infobars",
        "--metrics-recording-only",
        "--no-first-run",
        "--safebrowsing-disable-auto-update",
        "--mute-audio",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
    ]

    for arg in args:
        chrome_options.add_argument(arg)

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_service = Service("./chromedriver.exe")
    chrome_service.creation_flags = 0x8000000  # Suppress logs

    return chrome_service, chrome_options

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This script needs to be run as Administrator. Re-launching with elevated privileges...")
        # Relaunch the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()  # Exit the original script

def sync_windows_time():
    try:
        # Start the Windows Time service if it's not running
        subprocess.run(["net", "start", "w32time"], shell = True, check = False)

        # Resync time
        subprocess.run(["w32tm", "/resync"], shell = True, check = True)
        print("Time successfully synchronized with Windows Time Server.")

    except subprocess.CalledProcessError:
        print("Error syncing time. Please run this program as Administrator.")

if __name__ == "__main__":
    # Running the script as Administrator is required for syncing the time
    run_as_admin()

    # Get screen dimensions
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Initialize ChromeDriver with optimizations
    chrome_service, chrome_options = set_chrome_settings()
    driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
    driver.set_window_size(screen_width / 2, screen_height)
    driver.get("https://vue.comm100.com/joinqueue/80000180/location?locationId=90864154a3fb4566884b2e1833d3951d")

    # Wait until exactly the opening time in PST (24-hour time)
    pst_tz = ZoneInfo("America/Los_Angeles")
    year = datetime.now(pst_tz).year
    month = datetime.now(pst_tz).month
    day = datetime.now(pst_tz).day
    second = 0
    microsecond = 0
    ### MODIFY TO MATCH THE OPENING TIME IN PST (24-hour time) ###
    hour = #
    minute = #

    ### ENTER REQUIRED INFORMATION BELOW AS STRINGS ###
    ### PREFERRED NAME ###
    preferred_name = ""

    ### LAST INITIAL ###
    last_initial = ""

    ### CELL PHONE NUMBER (only CAN numbers will receive text message updates) ###
    phone_number = ""

    ### SELECT INQUIRY TYPE FOR THE "select.value" FIELD BELOW ###
    ### Copy-paste one of: 
    ### "Degree Requirements"
    ### "Course Registration"
    ### "Transfer credit"
    ### "Academic Concessions"
    ### "Graduation check (Year 4 students)"
    ### "Other"
    inquiry_type = ""

    ### STUDENT NUMBER ###
    student_number = ""

    ### SELECT WHETHER YOU HAVE SENT A MESSAGE FOR THE "select.value" FIELD BELOW ###
    ### Copy-paste one of: 
    ### "Yes"
    ### "No"
    sent_message = ""

    reg_time = time(hour, minute)
    form_reg_time = reg_time.strftime("%I:%M %p").lstrip("0").lower()  # Formatted as 12-hour time
    input(f"Welcome to UBC Science Advising Queue Sniper!\nInstructions:\n 1. ⭐ENSURE THE SCIENCE ADVISING OPENING TIME IS SET CORRECTLY!⭐\n    You have set the Science Advising opening time to {form_reg_time} PST.\n 2. Ensure all inputted information is correct.\n    Preferred name: {preferred_name}\n    Last initial: {last_initial}\n    Cell phone number: {phone_number}\n    Type of inquiry: {inquiry_type}\n    Student number: {student_number}\n    Have you sent us (Science Advising) a message about this? {sent_message}\n 3. Press `Enter` in the terminal to start the script.")

    sync_windows_time()

    target_time = datetime(year, month, day, hour, minute, second, microsecond, pst_tz)
    now = datetime.now(pst_tz)
    if now > target_time:
        print(f"\nIt is past {form_reg_time}.")
    else:
        wait_seconds = (target_time - now).total_seconds() - 0.200  # Decreased wait time to ensure scripts starts as close to the opening time as possible
        print(f"\nWaiting {wait_seconds:.3f} seconds until {form_reg_time}.\nDO NOT TOUCH YOUR COMPUTER except to ensure that it does not fall asleep.")
        time_obj.sleep(wait_seconds)

    # Refresh the page at the target time
    print("\nRefreshing the page...")
    driver.refresh()

    try:
        virtual_advising_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Virtual Advising (Zoom) - Science Advising')]"))
        )
        virtual_advising_button.click()
        print("\nClicked 'Virtual Advising (Zoom) - Science Advising'")

        next_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
        )
        next_button.click()
        print("\nClicked 'Next'")

        preferred_name_field = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Preferred Name')]/following::input[1]"))
        )
        preferred_name_field.send_keys(preferred_name)
        print("\nFilled 'Preferred Name'")

        last_initial_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Last Initial')]/following::input[1]"))
        )
        last_initial_field.send_keys(last_initial)
        print("\nFilled 'Last Initial'")

        phone_number_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Cell Phone Number (only CAN numbers will receive text message updates)')]/following::input[1]"))
        )
        phone_number_field.send_keys(phone_number)
        print("\nFilled 'Cell Phone Number'")

        # Use Field ID ONLY if broken
        # type_of_inquiry = WebDriverWait(driver, 1).until(
        #     EC.presence_of_element_located((By.XPATH, "//select[@id='field-3837ca01-2f7d-4bbb-b26d-33051b63b8cd']"))  # Dropdown field id
        # )
        type_of_inquiry_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(@class, 'field__label') and contains(., 'Type of Inquiry')]/ancestor::div[contains(@class, 'field')]//select"))
        )
        driver.execute_script("""
            const select = arguments[0];
            select.value = arguments[1];
            select.dispatchEvent(new Event('change', { bubbles: true }));
        """, type_of_inquiry_field, inquiry_type)
        print("\nFilled 'Type of Inquiry'")

        student_number_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(., 'UBC Student Number')]/following::input[1]"))
        )
        student_number_field.send_keys(student_number)
        print("\nFilled 'UBC Student Number'")

        # Use Field ID if broken
        # sent_message = WebDriverWait(driver, 1).until(
        #     EC.presence_of_element_located((By.XPATH, "//select[@id='field-fb888639-03e6-477b-bfed-0fedb1184b69']"))  # Dropdown field id
        # )
        sent_message_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(@class, 'field__label') and contains(., 'Have you sent us (Science Advising) a message about this?')]/ancestor::div[contains(@class, 'field')]//select"))
        )
        driver.execute_script("""
            const select = arguments[0];
            select.value = arguments[1];
            select.dispatchEvent(new Event('change', { bubbles: true }));
        """, sent_message_field, sent_message)
        print("\nFilled 'Have you sent us (Science Advising) a message about this?'")

        join_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Join')]"))
        )
        join_button.click()
        print("\nClicked 'Join'")

    except Exception as e:
        print("\nERROR JOINING QUEUE.", e)

    time_obj.sleep(999999) # Keep Chrome open (for ~11 days)

    # Cleanup (optional)
    # driver.quit()