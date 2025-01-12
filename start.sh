#!/bin/bash

# Set the current directory to the script's location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define the Python script path relative to the current directory
PYTHON_SCRIPT="$SCRIPT_DIR/src/main/server/start_server.py"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed or not in your system's PATH environment variable."
    exit 1
fi

# Run the Python script with the current directory as an argument
python "$PYTHON_SCRIPT" "$SCRIPT_DIR"