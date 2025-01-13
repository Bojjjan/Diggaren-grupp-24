#!/bin/bash

# Set the current directory to the script's location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define the Python script path relative to the current directory
PYTHON_SCRIPT="$SCRIPT_DIR/src/main/server/start_server.py"


# Run the Python script with the current directory as an argument
python3 "$PYTHON_SCRIPT" "$SCRIPT_DIR"