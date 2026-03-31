FROM python:3.11-slim

WORKDIR /app

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (no PyTorch, CPU-only TF)
RUN pip install --no-cache-dir \
    tensorflow-cpu==2.15.0 \
    fastapi \
    "uvicorn[standard]" \
    pillow \
    numpy \
    opencv-contrib-python-headless \
    huggingface_hub \
    h5py \
    python-multipart \
    scipy

COPY . .

# Download models at build time (cached in image)
RUN python download_models.py

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
