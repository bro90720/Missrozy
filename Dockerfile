# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variable to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Update package lists
RUN apt-get update

# Install locales and build-essential packages
RUN echo y | apt-get install locales && \
    echo y | apt install build-essential

# Install necessary dependencies
RUN apt -qq install -y --no-install-recommends \
    curl \
    git \
    gnupg2 \
    wget

# Install Python and other necessary dependencies
RUN set -ex; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        busybox \
        git \
        python3 \
        python3-dev \
        python3-pip \
        python3-lxml \
        pv && \
    apt-get autoclean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install setuptools and other necessary Python libraries
RUN pip3 install setuptools wheel yarl multidict

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Reconfigure locales (if necessary)
RUN dpkg-reconfigure locales

# Copy all other application files to the working directory
COPY . /app

# Set the command to run your Python bot
CMD ["python3", "bot.py"]
