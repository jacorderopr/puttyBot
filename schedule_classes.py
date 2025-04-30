#!/usr/bin/env python3
import time
import sys
import os
import re
from dotenv import load_dotenv # <-- Import load_dotenv

try:
    import keyboard
except ImportError:
    print("Error: The 'keyboard' library is not installed.")
    print("Please install it: pip install keyboard")
    sys.exit(1)

# --- Load Environment Variables ---
load_dotenv() # <-- Load variables from .env file into environment

# --- Get Credentials from Environment ---
STUDENT_ID_FROM_ENV = os.getenv("STUDENT_ID")
STUDENT_PIN_FROM_ENV = os.getenv("STUDENT_PIN")
STUDENT_PIN_2 = os.getenv("STUDENT_PIN_2")
STUDENT_BIRTHDAY = os.getenv("STUDENT_BIRTHDAY")

# --- Validate Credentials ---
if not STUDENT_ID_FROM_ENV:
    print("Error: STUDENT_ID not found in environment or .env file.")
    print("Please ensure it's defined in the .env file.")
    sys.exit(1)
if not STUDENT_PIN_FROM_ENV:
    print("Error: STUDENT_PIN not found in environment or .env file.")
    print("Please ensure it's defined in the .env file.")
    sys.exit(1)


# --- Configuration ---
CLASSES_FILE = 'classes_with_sections.txt'
CLASS_SECTION_REGEX = r'^([A-Z]{4}\d{4})-([A-Za-z0-9]+)$'

# Base sequence using fetched credentials
BASE_INPUT_SEQUENCE = [
    "ENTER_KEY",
    "2",
    STUDENT_ID_FROM_ENV, # <-- Use variable
    STUDENT_PIN_FROM_ENV, # <-- Use variable
    STUDENT_PIN_2, # <-- Use variable
    STUDENT_BIRTHDAY, # <-- Use variable
    "1",
    "A",
    # Class codes inserted here
    "FIN",
    "ENTER_KEY",
    "S",
    "WAIT_5_SECONDS",
    "S",
    "ENTER_KEY",
]

# Delay settings
INITIAL_WAIT = 5
DELAY_AFTER_TYPE = 0.1
DELAY_AFTER_ENTER = 0.6

# --- Platform Specific Notes ---
# (Keep existing platform checks)
if os.name == 'posix' and os.geteuid() != 0 and sys.platform != 'darwin':
     print("\nWARNING: On Linux, the 'keyboard' library usually needs root privileges.")
     print("You might need to run this script using 'sudo python your_script.py'\n")
elif sys.platform == 'darwin':
     print("\nNOTE: On macOS, you may need to grant Accessibility permissions")
     print("to your Terminal or IDE in System Settings > Privacy & Security > Accessibility.\n")

# --- File Reading and Parsing ---
print(f"Attempting to read class schedule from: {CLASSES_FILE}")
# (Keep existing file reading logic)
if not os.path.exists(CLASSES_FILE):
    print(f"Error: File '{CLASSES_FILE}' not found. Please create it.")
    sys.exit(1)

parsed_classes_commands = []
try:
    with open(CLASSES_FILE, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(CLASS_SECTION_REGEX, line)
            if match:
                class_code = match.group(1)
                section = match.group(2)
                parsed_classes_commands.append(class_code)
                parsed_classes_commands.append("ENTER_KEY")
                parsed_classes_commands.append(section)
                parsed_classes_commands.append("ENTER_KEY")
                print(f"  Successfully parsed: {class_code} - {section}")
            else:
                print(f"\nError: Invalid format on line {line_num} in '{CLASSES_FILE}'.")
                print(f"  Line content: '{line}'")
                print(f"  Expected format: 'LLLLNNNN-Section' (e.g., CIIC5140-036)")
                sys.exit(1)
except Exception as e:
    print(f"\nError reading or parsing file '{CLASSES_FILE}': {e}")
    sys.exit(1)

if not parsed_classes_commands:
    print(f"Warning: No valid class/section entries found in '{CLASSES_FILE}'.")

# --- Construct Final Input Sequence ---
try:
    insert_index = BASE_INPUT_SEQUENCE.index('A') + 1
except ValueError:
    print("Error: Could not find insertion point 'A' in BASE_INPUT_SEQUENCE.")
    sys.exit(1)

FINAL_INPUT_SEQUENCE = BASE_INPUT_SEQUENCE[:insert_index] + \
                       parsed_classes_commands + \
                       BASE_INPUT_SEQUENCE[insert_index:]

print("\nFinal sequence of commands constructed.")
# import pprint
# pprint.pprint(FINAL_INPUT_SEQUENCE)


# --- Main Execution ---
print("="*40)
print("!!! IMPORTANT !!!")
print("1. MANUALLY start your 'putty' session in a terminal NOW.")
print("2. Ensure the terminal window running 'putty' HAS FOCUS.")
print(f"3. The script will start typing in {INITIAL_WAIT} seconds...")
print("="*40)

for i in range(INITIAL_WAIT, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)
print("Starting keyboard input simulation!")

try:
    time.sleep(0.5)
    for item in FINAL_INPUT_SEQUENCE:
        if item == "WAIT_5_SECONDS":
            print("--> Waiting 5 seconds...")
            time.sleep(5)
        elif item == "ENTER_KEY":
            print("--> Sending: [ENTER]")
            keyboard.press_and_release('enter')
            time.sleep(DELAY_AFTER_ENTER)
        else:
            print(f"--> Typing: {item if item not in (STUDENT_ID_FROM_ENV, STUDENT_BIRTHDAY, STUDENT_PIN_FROM_ENV, STUDENT_PIN_2) else '*****'}")
            keyboard.write(item)
            time.sleep(DELAY_AFTER_TYPE)
            time.sleep(DELAY_AFTER_ENTER * 0.5) # Still need some delay

    print("\n" + "="*40)
    print("Finished sending all keyboard inputs.")
    print("Check your terminal session to see the result.")
    print("Remember, this script cannot verify success.")
    print("="*40)

except Exception as e:
    print("\n" + "="*40)
    print(f"An error occurred during keyboard simulation: {e}")
    print("The sequence may not have completed.")
    print("Check keyboard library permissions (Linux: sudo? macOS: Accessibility?).")
    print("="*40)
except KeyboardInterrupt:
    print("\n" + "="*40)
    print("Script interrupted by user (Ctrl+C).")
    print("="*40)