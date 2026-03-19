#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

echo "--- Preparing environment for p2p-copy ---"

# 1. Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed. Please install it with:"
    echo "  sudo apt update && sudo apt install python3"
    exit 1
fi

# 2. Check for venv module
if ! python3 -m venv --help &>/dev/null; then
    echo "Error: the 'venv' module is missing."
    echo "On Debian/Ubuntu, please install it with:"
    echo "  sudo apt update && sudo apt install python3-venv"
    exit 1
fi

# 3. Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv/..."
    python3 -m venv .venv || {
        echo "Error: Failed to create virtual environment."
        echo "Try installing: sudo apt install python3-venv"
        exit 1
    }
fi

# 4. Check if pip exists in the virtual environment
if [ ! -f ".venv/bin/pip" ]; then
    echo "Error: 'pip' was not found in the virtual environment."
    echo "This usually happens if 'python3-pip' is missing on the host."
    echo "Try: sudo apt update && sudo apt install python3-pip"
    exit 1
fi

# 5. Install/Update the package
echo "Installing dependencies and configuring p2p-copy command..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .

echo "-------------------------------------------------------"
echo "Installation completed successfully!"
echo ""
echo "To use the program, you can:"
echo "  1. Activate the environment: source .venv/bin/activate"
echo "  2. Or use the direct path: $(pwd)/.venv/bin/p2p-copy"
echo "-------------------------------------------------------"
