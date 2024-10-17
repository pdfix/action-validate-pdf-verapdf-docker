# Use the official Debian slim image as a base
FROM debian:stable-slim

# Install Tesseract OCR and necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    openjdk-17-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/validation/

ENV VIRTUAL_ENV=venv


# Create a virtual environment and install dependencies
RUN python3 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Copy the source code and requirements.txt into the container
COPY src/ /usr/validation/src/
# res contains the VeraPDF CLI build
COPY res/ /usr/validation/res/


ENTRYPOINT ["/usr/validation/venv/bin/python3", "/usr/validation/src/main.py"]
