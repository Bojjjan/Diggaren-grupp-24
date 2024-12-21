#!/bin/bash

os_dir="$(dirname "$(realpath "$0")")"
script_dir="$os_dir/src/main/server"

python3 "$script_dir/start_server.py" "$os_dir"