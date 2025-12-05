#!/bin/bash
################################################################################
# LOGOS ENGINE - Quick Setup Script for Linux/Mac/Raspberry Pi
# 
# This script will:
# 1. Check if Python 3 is installed
# 2. Install networkx (required)
# 3. Build the graph database
# 4. Test the installation
#
# Usage: 
#   chmod +x setup.sh
#   ./setup.sh
#
# Or in one line:
#   bash setup.sh
################################################################################

set -e  # Exit on any error

echo "================================================================================"
echo "                    LOGOS ENGINE - Quick Setup"
echo "================================================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo "Step 1: Checking for Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    if [[ $PYTHON_VERSION == *"Python 3"* ]]; then
        echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗ Error: Python 3 is required but only found $PYTHON_VERSION${NC}"
        echo ""
        echo "Please install Python 3:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        echo "  Mac: brew install python3"
        exit 1
    fi
else
    echo -e "${RED}✗ Error: Python is not installed${NC}"
    echo ""
    echo "Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Mac: brew install python3"
    exit 1
fi
echo ""

# Step 2: Check pip
echo "Step 2: Checking for pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ Found: pip3${NC}"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}✓ Found: pip${NC}"
    PIP_CMD="pip"
else
    echo -e "${YELLOW}⚠ pip not found, attempting to install...${NC}"
    $PYTHON_CMD -m ensurepip --default-pip || {
        echo -e "${RED}✗ Could not install pip${NC}"
        echo "Please install pip manually:"
        echo "  Ubuntu/Debian: sudo apt install python3-pip"
        exit 1
    }
    PIP_CMD="pip3"
fi
echo ""

# Step 3: Install networkx
echo "Step 3: Installing required dependencies..."
echo "Installing networkx (this may take a moment)..."
$PIP_CMD install --user networkx || {
    echo -e "${YELLOW}⚠ Failed with --user flag, trying without...${NC}"
    $PIP_CMD install networkx || {
        echo -e "${RED}✗ Failed to install networkx${NC}"
        echo "Please try manually: $PIP_CMD install networkx"
        exit 1
    }
}
echo -e "${GREEN}✓ networkx installed successfully${NC}"
echo ""

# Step 4: Build the graph
echo "Step 4: Building LOGOS graph database..."
echo "This will create the network graph from Bible data..."
$PYTHON_CMD logos.py build || {
    echo -e "${YELLOW}⚠ Graph build returned non-zero, but this may be okay if graph already exists${NC}"
}
echo ""

# Step 5: Test the installation
echo "Step 5: Testing LOGOS ENGINE..."
echo "Looking up John 3:16..."
echo ""
$PYTHON_CMD logos.py verse "John 3:16" || {
    echo -e "${RED}✗ Test failed${NC}"
    exit 1
}
echo ""

# Success!
echo "================================================================================"
echo -e "${GREEN}✓ LOGOS ENGINE is ready!${NC}"
echo "================================================================================"
echo ""
echo "Try these commands:"
echo "  $PYTHON_CMD logos.py help              # Show all commands"
echo "  $PYTHON_CMD logos.py verse \"Genesis 1:1\" # Look up a verse"
echo "  $PYTHON_CMD logos.py search \"grace\"     # Search for a word"
echo "  $PYTHON_CMD logos.py strongs H430      # Hebrew/Greek study"
echo "  $PYTHON_CMD logos.py stats             # Network statistics"
echo ""
echo "Read START_HERE.txt for introduction"
echo "Read WHY.txt to understand the Gospel"
echo "Read docs/INSTALL.md for complete documentation"
echo ""
echo "================================================================================"
echo "\"In the beginning was the Word, and the Word was with God,"
echo " and the Word was God.\" - John 1:1"
echo "================================================================================"
