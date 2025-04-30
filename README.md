# University Class Scheduler Automation

This set of scripts attempts to automate the process of logging into a university student portal via an SSH connection (using a pre-configured `putty` alias) and entering class registration details based on local configuration files.

** **CRITICAL WARNINGS** **

*   **Fragile Automation:** This script uses the `keyboard` Python module to simulate keyboard input. This method is **highly dependent on timing and window focus**. If the university portal's response time changes, or if focus is lost from the target terminal window during execution, the script **will likely fail** without proper error reporting regarding the remote system's state.
*   **No Success Verification:** The script *cannot* verify if the class registration was actually successful. You **MUST** manually log in afterward to confirm your schedule.
*   **Security:** While credentials are read from a `.env` file to avoid hardcoding in the script, they are still stored in plain text on your local machine. Ensure the `.env` file has restrictive permissions.
*   **Permissions:** The `keyboard` library often requires elevated permissions (root/sudo on Linux, Accessibility settings on macOS).

**Use this script at your own risk. The author is not responsible for any issues arising from its use, including incorrect class registration or security vulnerabilities.**

## Prerequisites

Before you begin, ensure you have the following:

1.  **Operating System:** Linux or macOS.
2.  **Python:** Python 3 installed.
3.  **pip:** Python package installer (usually comes with Python 3).
4.  **`putty` Alias:** You must have a shell alias named `putty` configured (e.g., in your `~/.bashrc`, `~/.zshrc`, etc.) that successfully executes the `ssh` command to connect to the university portal. Example:
    ```bash
    # Example alias in ~/.zshrc or ~/.bashrc
    alias putty='ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa your_username@university.portal.edu'
    ```
    *(Verify this alias works correctly by simply typing `putty` in your terminal)*

## Setup Instructions

1.  **Directory:** Ensure both `schedule_classes.py` and `run_script.sh` are in the same directory. The scripts assume this directory is `~/Documents/schedule_classes`. If not, you'll need to adjust the `PYTHON_SCRIPT_DIR` variable in `run_script.sh`.

2.  **Navigate to Directory:**
    ```bash
    cd ~/Documents/schedule_classes
    ```

3.  **Create Virtual Environment:** (Recommended)
    ```bash
    python3 -m venv venv
    ```

4.  **Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    # Your terminal prompt should now indicate the 'venv' is active
    ```

5.  **Install Dependencies:**
    ```bash
    pip install keyboard python-dotenv
    ```

6.  **Create `classes_with_sections.txt`:**
    *   Create a text file named `classes_with_sections.txt` in the same directory.
    *   List the classes you want to register, one per line, in the format `CLASSCODE-SECTION`.
    *   The class code must be 4 uppercase letters followed by 4 digits.
    *   The section can contain letters and numbers.
    *   Lines starting with `#` or empty lines will be ignored.
    *   **Example `classes_with_sections.txt`:**
        ```
        # Fall Semester Classes
        CIIC5140-036
        ININ4010-010
        MATE3135-051H
        ESPA4225-016
        ```

7.  **Create `.env` File:**
    *   Create a file named `.env` (starting with a dot) in the same directory.
    *   This file will store your sensitive login credentials.
    *   Add the following keys, replacing the placeholder values with your actual information:
        ```dotenv
        # .env file - Stores sensitive credentials
        STUDENT_ID=YOUR_STUDENT_ID_HERE
        STUDENT_PIN=YOUR_FIRST_PIN_HERE
        STUDENT_PIN_2=YOUR_SECOND_PIN_HERE
        STUDENT_BIRTHDAY=YOUR_BIRTHDAY_MMDDYYYY_HERE
        ```
    *   **Example `.env`:**
        ```dotenv
        STUDENT_ID=802123456
        STUDENT_PIN=9876
        STUDENT_PIN_2=1234
        STUDENT_BIRTHDAY=01152003
        ```

8.  **Set `.env` Permissions (Security):**
    *   Restrict permissions so only you can read/write this file.
    ```bash
    chmod 600 .env
    ```

9.  **Configure `.gitignore` (If using Git):**
    *   If you are using Git version control in this directory, create or edit a `.gitignore` file and add the following lines to prevent committing sensitive information and the virtual environment:
    ```gitignore
    venv/
    __pycache__/
    *.pyc
    .env
    ```

## Usage

1.  **Make Shell Script Executable:**
    ```bash
    chmod +x run_script.sh
    ```

2.  **Run the Script:**
    *   Ensure your virtual environment is activated (`source venv/bin/activate`).
    *   Execute the shell script:
        ```bash
        ./run_script.sh
        ```

3.  ** **!!! CRITICAL STEP !!!** **
    *   The `run_script.sh` will open a **new terminal window** and attempt to start the `putty` SSH session inside it.
    *   **IMMEDIATELY** after the new terminal window appears, **CLICK ON IT** to give it keyboard focus.
    *   The original terminal window (where you ran `./run_script.sh`) will show a countdown (`Starting in X...`). The Python script will start simulating keyboard input once the countdown finishes.
    *   **The `putty` terminal window MUST have focus when the Python script starts typing.**

4.  **Monitor:**
    *   Observe the `putty` terminal window. You should see the commands being typed automatically.
    *   The original terminal window will print logs indicating which command is being typed (sensitive info like ID/PINs will be masked with `*****`).

5.  **Verify:**
    *   Once the script finishes, **manually log in** to the student portal to **verify that your classes were registered correctly**. Do not rely solely on the script's output.

## Configuration

*   **SSH Command:** If the `putty` alias doesn't work correctly when launched by the script (sometimes aliases aren't available in non-interactive shells), edit `run_script.sh` and replace `PUTTY_COMMAND="putty"` with the full SSH command string.
*   **Delays:**
    *   `SSH_STARTUP_DELAY` in `run_script.sh`: Time (in seconds) the script waits after opening the new terminal before starting the Python script. Increase if your SSH connection is slow.
    *   `INITIAL_WAIT`, `DELAY_AFTER_TYPE`, `DELAY_AFTER_ENTER` in `schedule_classes.py`: Timings (in seconds) for the keyboard simulation. Adjust if commands are being missed or entered too quickly/slowly.

## Troubleshooting

*   **Permissions Error (keyboard):**
    *   **Linux:** You likely need to run the shell script with `sudo`: `sudo ./run_script.sh`.
    *   **macOS:** Grant Accessibility permissions to your Terminal application (e.g., Terminal.app, iTerm.app) in System Settings > Privacy & Security > Accessibility.
*   **`putty: command not found` (in new terminal):** The alias isn't working in the context the new terminal is launched. Edit `run_script.sh` and set `PUTTY_COMMAND` to the full `ssh ...` command.
*   **Script Types in Wrong Window:** You didn't give focus to the new `putty` terminal window quickly enough. Run the script again and ensure focus is correct.
*   **Commands Fail / Incorrect Input:** The timing delays might be wrong for your connection speed or the portal's responsiveness. Adjust the `DELAY_` variables in `schedule_classes.py`. The portal's interface might have also changed.
*   **File Not Found (`.env`, `classes_with_sections.txt`):** Ensure these files exist in the same directory as the scripts and are named correctly.
*   **Invalid Format Error (`classes_with_sections.txt`):** Check the specified line in the file; ensure it matches the `ABCD1234-S3CT10N` format.
*   **Credentials Not Found:** Ensure the `.env` file contains the required keys (`STUDENT_ID`, `STUDENT_PIN`, etc.) and is saved correctly.