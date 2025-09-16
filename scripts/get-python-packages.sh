#!/bin/bash

# ==============================================================================
# Download Python Packages for Offline Docker Build
# ==============================================================================
#
# Description:
# This script uses a temporary Docker container to download all Python packages
# listed in requirements.txt. It downloads the Linux-compatible versions,
# making them suitable for building the Docker image in an air-gapped environment.
#
# Usage:
# Run this script from the root of the project directory on an
# internet-connected machine before transferring the project.
#
# ./scripts/download_python_packages.sh
#

# --- Configuration ---
# The base Python image. This MUST match the FROM line in your Dockerfile.
PYTHON_IMAGE="python:3.12-bullseye"

# The local folder where package files (.whl) will be stored.
PACKAGES_DIR="./packages"

# The requirements file listing all dependencies.
REQUIREMENTS_FILE="./requirements.txt"


# --- Script Logic ---

# Announce the start of the process
echo "--- Preparing to download Python packages for offline build ---"
echo "Using base image: $PYTHON_IMAGE"

# 1. Ensure the packages directory exists.
# The '-p' flag means 'create parent directories if needed, no error if it exists'.
echo "Ensuring packages directory exists at: $PACKAGES_DIR"
mkdir -p "$PACKAGES_DIR"

# 2. Check if requirements.txt exists before proceeding.
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "ERROR: requirements.txt not found at '$REQUIREMENTS_FILE'. Aborting."
    exit 1
fi

# 3. Run the docker command to download the packages.
# This command starts a temporary, clean Linux container to ensure we get
# the correct, platform-independent packages for our final Docker image.
echo "Starting temporary Docker container to download packages..."

docker run --rm \
  -v "$(pwd)/packages:/app/packages" \
  -v "$(pwd)/requirements.txt:/app/requirements.txt" \
  "$PYTHON_IMAGE" \
  pip download -r /app/requirements.txt -d /app/packages

# Check the exit code of the docker command.
# '$?' is a special variable in bash that holds the exit code of the last command.
# A '0' means success.
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Success! All packages have been downloaded to the '$PACKAGES_DIR' folder."
else
  echo ""
  echo "❌ Error: The docker run command failed. Please check the output above for details."
  exit 1
fi
```

### How to Use It

1.  **Place the file:** Save the code above into a new file at `scripts/download_python_packages.sh`.
2.  **Make it executable (Mac/Linux only):** You may need to give the script permission to run. In your terminal, type:
    ```bash
    chmod +x scripts/download_python_packages.sh

````