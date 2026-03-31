FROM python:3.11-slim

WORKDIR /app

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Use tensorflow-cpu for CPU-only deployment (no GPU)
# Filter out PyTorch/TIMM (not needed for inference)
RUN pip install --no-cache-dir \
    --upgrade pip && \
    pip install --no-cache-dir \
    tensorflow-cpu==2.18.0 \
    fastapi==0.115.6 \
    uvicorn[standard]==0.34.0 \
    python-multipart==0.0.20 \
    pillow \
    numpy \
    scikit-image \
    python-dotenv==1.0.1 \
    pydantic \
    opencv-contrib-python-headless \
    huggingface_hub \
    h5py \
    scipy

COPY . .

# Models are downloaded at runtime by app.py startup
# (No need to pre-download during build)

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
