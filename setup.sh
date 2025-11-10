#!/bin/bash
# Bash Setup Script for AN/FSQ-7 Simulator
# Run this script on Linux/Mac to install and launch the simulator

echo "==============================================="
echo "  AN/FSQ-7 SAGE Computer Simulator Setup"
echo "==============================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✓ Found: $PYTHON_VERSION"
    
    # Check if version is 3.8 or higher
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        echo "✗ Python 3.8 or higher required. Please upgrade Python."
        exit 1
    fi
else
    echo "✗ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies."
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Initialize Reflex
echo "Initializing Reflex application..."
if [ ! -d ".web" ]; then
    reflex init --loglevel warning
    
    if [ $? -ne 0 ]; then
        echo "✗ Failed to initialize Reflex."
        exit 1
    fi
    
    echo "✓ Reflex initialized successfully"
else
    echo "✓ Reflex already initialized"
fi

echo ""
echo "==============================================="
echo "  Setup Complete!"
echo "==============================================="
echo ""
echo "Starting the simulator..."
echo "Once the server starts, open your browser to:"
echo "  http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Run the simulator
reflex run
