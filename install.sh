#!/bin/bash

# ANSI Color codes
BLUE='\033[94m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Ensure we are in the script's directory
cd "$(dirname "$0")"

echo -e "${BLUE}${BOLD}-------------------------------------------------------${NC}"
echo -e "${BLUE}${BOLD}   ____ ___   ____        ______                      ${NC}"
echo -e "${BLUE}${BOLD}  / __ \\__ \\ / __ \\      / ____/___  ____  __  __ ${NC}"
echo -e "${BLUE}${BOLD} / /_/ /_/ // /_/ /_____/ /   / __ \\/ __ \\/ / / / ${NC}"
echo -e "${BLUE}${BOLD}/ ____/ __// ____/_____/ /___/ /_/ / /_/ / /_/ /  ${NC}"
echo -e "${BLUE}${BOLD}/_/   /____/_/          \\____/\\____/ .___/\\__, /   ${NC}"
echo -e "${BLUE}${BOLD}                                  /_/    /____/    ${NC}"
echo -e "${YELLOW}   Secure P2P-style file transfer setup script${NC}"
echo -e "${BLUE}${BOLD}-------------------------------------------------------${NC}"

echo -e "\n${YELLOW}Step 1: Checking system requirements...${NC}"

# 1. Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    echo "Please install it with: sudo apt update && sudo apt install python3"
    exit 1
fi

# 2. Check for venv module
if ! python3 -m venv --help &>/dev/null; then
    echo -e "${RED}Error: the 'venv' module is missing.${NC}"
    echo "On Debian/Ubuntu, please install it with: sudo apt update && sudo apt install python3-venv"
    exit 1
fi

# 3. Create virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}Creating virtual environment in .venv/...${NC}"
    python3 -m venv .venv || {
        echo -e "${RED}Error: Failed to create virtual environment.${NC}"
        exit 1
    }
fi

# 4. Check for pip
if [ ! -f ".venv/bin/pip" ]; then
    echo -e "${RED}Error: 'pip' was not found in the virtual environment.${NC}"
    echo "Try: sudo apt update && sudo apt install python3-pip"
    exit 1
fi

# 5. Install/Update
echo -e "${YELLOW}Step 2: Installing dependencies and p2p-copy...${NC}"
.venv/bin/pip install --upgrade pip &>/dev/null
.venv/bin/pip install -e . &>/dev/null

echo -e "\n${GREEN}${BOLD}✔ Installation completed successfully!${NC}"
echo "-------------------------------------------------------"
echo -e "To use the program, you can:"
echo -e "  1. Activate: ${BOLD}source .venv/bin/activate${NC}"
echo -e "  2. Direct:   ${BOLD}/tmp/fc/.venv/bin/p2p-copy${NC}"
echo "-------------------------------------------------------"
