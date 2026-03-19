#!/bin/bash

# Configuration
INSTALL_DIR="$HOME/.p2pc-secure"
BIN_DIR="$HOME/.local/bin"
BLUE='\033[94m'; GREEN='\033[92m'; YELLOW='\033[93m'; RED='\033[91m'; BOLD='\033[1m'; NC='\033[0m'

echo -e "${BLUE}${BOLD}--- p2pc-secure: Installer ---${NC}"

# 1. Prepare target directory
echo -e "${YELLOW}Step 1: Preparing permanent home in $INSTALL_DIR...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# 2. Sync files (excluding .git and .venv)
echo -e "${YELLOW}Step 2: Copying source files...${NC}"
if command -v rsync &>/dev/null; then
    rsync -aq --exclude='.git' --exclude='.venv' . "$INSTALL_DIR/"
else
    cp -r . "$INSTALL_DIR/"
    rm -rf "$INSTALL_DIR/.git" "$INSTALL_DIR/.venv"
fi

# 3. Setup Virtual Env
echo -e "${YELLOW}Step 3: Setting up internal environment in $INSTALL_DIR...${NC}"
cd "$INSTALL_DIR"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip &>/dev/null
.venv/bin/pip install -e . &>/dev/null

# 4. Create the global shim/access in $BIN_DIR
echo -e "${YELLOW}Step 4: Creating global command...${NC}"
cat > "$BIN_DIR/p2pc-secure" <<EOF
#!/bin/bash
"$INSTALL_DIR/.venv/bin/p2pc-secure" "\$@"
EOF
chmod +x "$BIN_DIR/p2pc-secure"

# 5. Clear bash hash cache
hash -r 2>/dev/null

echo -e "\n${GREEN}${BOLD}✔ Installation complete!${NC}"
echo "-------------------------------------------------------"
echo -e "The command ${BOLD}p2p-copy${NC} is now ready."
echo -e "Note: Make sure ${BOLD}$BIN_DIR${NC} is in your PATH."
echo "To ensure it works now, run: export PATH=\$PATH:$BIN_DIR"
echo "-------------------------------------------------------"
