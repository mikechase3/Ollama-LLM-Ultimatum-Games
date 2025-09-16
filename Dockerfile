# Dockerfile for an OFFLINE machine
#################### UNCOMMENT BELOW ####################################
#FROM python:3.12-bullseye
#WORKDIR /app
#COPY requirements.txt .
#COPY packages/ ./packages/
## RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --no-index --find-links=./packages -r requirements.txt
#COPY . .
##COPY app .
#EXPOSE 8501

# Dockerfile for an ONLINE machine with SSH Server (DEBUG MODE)

# This will pull the official Python image from the internet
FROM python:3.12-bullseye

# --- Installation Steps (separated for better debugging) ---

# Step 1: Update the package lists.
RUN apt-get update -y

# Step 2: Install the SSH server. The DEBIAN_FRONTEND flag prevents it from hanging.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server

# Step 3: Configure the SSH server to allow root login.
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Step 4: Set the root password.
RUN echo 'root:password' | chpasswd

# Step 5: Clean up the apt cache to keep the image smaller.
RUN rm -rf /var/lib/apt/lists/*

# --- Application Setup ---

WORKDIR /app

# Copy ONLY the requirements list
COPY requirements.txt .

# Install all packages directly from the internet (PyPI)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code.
COPY . .

# Expose ports for Streamlit and SSH
EXPOSE 8501
EXPOSE 22
