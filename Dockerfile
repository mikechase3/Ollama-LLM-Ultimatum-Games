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

# Dockerfile for an ONLINE machine
# This will pull the official Python image from the internet
FROM python:3.12-bullseye

WORKDIR /app

# Copy ONLY the requirements list
COPY requirements.txt .

# Install all packages directly from the internet (PyPI)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code. The .dockerignore file will
# prevent the large data folders from being included.
COPY . .

EXPOSE 8501