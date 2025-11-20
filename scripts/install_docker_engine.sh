#!/bin/bash

# ==============================================================================
# Docker Engine Installation Script for Ubuntu
# ==============================================================================
#
# Purpose: Installs Docker Engine (CLI) using the official Apt repository.
#          This method is preferred over Snap or Docker Desktop for Linux
#          development to avoid permission and volume mounting issues.
#
# Usage:
# 1. Make executable: chmod +x install_docker_engine.sh
# 2. Run: ./install_docker_engine.sh
# ==============================================================================

echo "--- Step 1: Removing conflicting packages ---"
# We remove old versions or unofficial Ubuntu repo versions to avoid conflicts.
# The 'for' loop iterates through the list of package names.
# If a package isn't installed, apt will just warn you and move on.
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove -y $pkg
done

echo "--- Step 2: Setting up Docker's apt repository ---"
# Update the local package index so we know what's currently available
sudo apt-get update

# Install prerequisites:
# ca-certificates: Allows apt to check HTTPS certificates
# curl: Tool to download the GPG key from the internet
sudo apt-get install -y ca-certificates curl

# Create the directory for the security keys with specific permissions
# -m 0755: Owner gets Read/Write/Exec (7), everyone else gets Read/Exec (5)
sudo install -m 0755 -d /etc/apt/keyrings

# Download Docker's official GPG key (used to verify the software hasn't been tampered with)
# -f: Fail silently on server errors
# -s: Silent mode (no progress bar)
# -S: Show error if it fails
# -L: Follow redirects
# -o: Output the file to the specific path
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

# Make the key readable by everyone (All users + Read permission)
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources
# This command constructs the download URL dynamically based on your Ubuntu version (VERSION_CODENAME)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "--- Step 3: Installing Docker Engine ---"
# Update apt again so it sees the NEW packages in the Docker repo we just added
sudo apt-get update

# Install the core Docker packages
# docker-ce: Docker Community Edition (the engine)
# docker-ce-cli: The command line tool (the 'docker' command)
# containerd.io: The container runtime
# docker-compose-plugin: The 'docker compose' command
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "--- Step 4: Post-Installation Setup ---"
# Add your current user ($USER) to the 'docker' group.
# -aG: Append to Group.
# This allows you to run docker commands without typing 'sudo' every time.
sudo usermod -aG docker $USER

echo ""
echo "✅ Installation Complete!"
echo "⚠️  IMPORTANT: You must Log Out and Log Back In (or reboot) for the group changes to take effect."
echo "   After logging back in, test it by running: docker run hello-world"