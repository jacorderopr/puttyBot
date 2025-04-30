#!/bin/bash

# --- Configuration ---
PYTHON_SCRIPT_DIR="$HOME/Documents/schedule_classes" # Use $HOME for portability
PYTHON_SCRIPT_NAME="schedule_classes.py"
VENV_DIR="venv"
PUTTY_COMMAND="putty" # Using the alias name
# OR use the full command if the alias doesn't work in the new terminal:
# PUTTY_COMMAND="ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa estudiante@rumad.uprm.edu"

# Delay to allow the new terminal and SSH connection to establish (adjust if needed)
SSH_STARTUP_DELAY=4

# --- Script Logic ---

echo "Navigating to script directory..."
cd "$PYTHON_SCRIPT_DIR" || { echo "Error: Could not navigate to $PYTHON_SCRIPT_DIR"; exit 1; }
echo "Current directory: $(pwd)"

echo "Activating Python virtual environment..."
source "$VENV_DIR/bin/activate" || { echo "Error: Could not activate virtual environment in $VENV_DIR"; exit 1; }
echo "Virtual environment activated."

echo "Opening new terminal and starting '$PUTTY_COMMAND'..."

# Platform detection for opening a new terminal
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  osascript <<EOF
tell application "Terminal"
    activate
    do script "$PUTTY_COMMAND"
end tell
EOF
  if [ $? -ne 0 ]; then
    echo "Error: Failed to open new Terminal window via osascript."
    exit 1
  fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux - Try common terminal emulators
  # The '; exec $SHELL' part attempts to keep the terminal open after putty exits
  if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "$PUTTY_COMMAND; echo 'SSH session ended. Press Enter to close.'; read" &
  elif command -v konsole &> /dev/null; then
    konsole -e bash -c "$PUTTY_COMMAND; echo 'SSH session ended. Press Enter to close.'; read" &
  elif command -v xterm &> /dev/null; then
    xterm -e bash -c "$PUTTY_COMMAND; echo 'SSH session ended. Press Enter to close.'; read" &
  else
    echo "Error: Could not find gnome-terminal, konsole, or xterm."
    echo "Please modify the script to use your installed terminal emulator."
    exit 1
  fi
  # Check if the command launched successfully in the background
  if [ $? -ne 0 ]; then
    echo "Error: Failed to open new terminal window."
    exit 1
  fi
else
  echo "Error: Unsupported operating system '$OSTYPE'. Cannot automatically open a new terminal."
  exit 1
fi

echo "'$PUTTY_COMMAND' should be starting in a new terminal window."
echo "Waiting ${SSH_STARTUP_DELAY} seconds for it to initialize..."
sleep $SSH_STARTUP_DELAY

echo "--- IMPORTANT ---"
echo "Ensure the new terminal window with '$PUTTY_COMMAND' has keyboard FOCUS."
echo "Running Python script now..."
echo "-----------------"

python3 "$PYTHON_SCRIPT_NAME"

# Deactivate might not be strictly necessary as the script ends, but good practice
# echo "Deactivating virtual environment..."
# deactivate

echo "Shell script finished."