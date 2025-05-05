FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install diffusers transformers safetensors Pillow

# Copy files
COPY . .

# Make sure output dir exists
RUN mkdir -p output
RUN pip install accelerate

# Set environment so CPU is used
ENV DOCKER_ENV=1

# Default command: run the generator with sample prompt
CMD ["python", "generate.py"]
