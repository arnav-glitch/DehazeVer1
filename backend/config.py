"""Configuration management for Dehaze backend."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Path configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# Helper function to find model path (check multiple locations)
def get_model_path(env_var, default_name):
    """Get model path from env var or check multiple standard locations."""
    if env_var in os.environ:
        return os.getenv(env_var)
    
    # Check multiple fallback locations
    possible_paths = [
        BASE_DIR / default_name,  # Local: Dehaze/maxim_savedmodel
        BASE_DIR / "backend" / default_name,  # In backend folder
        Path("/app/models") / default_name,  # HF Spaces download location
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
            
    # If in Hugging Face Space, models will be downloaded to /app/models momentarily
    if "SPACE_ID" in os.environ:
        return str(Path("/app/models") / default_name)
    
    # Return first choice (will fail later if not found)
    return str(possible_paths[0])

MODEL_PATH = get_model_path("MODEL_PATH", "maxim_savedmodel")
ADAPTER_PATH = get_model_path("ADAPTER_PATH", "adapter_best.weights.h5")
AOD_NET_PATH = get_model_path("AOD_NET_PATH", "adapter_aod.weights.h5")

# API configuration
API_PORT = int(os.getenv("API_PORT", 5001))
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# File handling
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "backend" / "uploads"))
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER", str(BASE_DIR / "backend" / "results"))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB

# CORS configuration
ENABLE_CORS = os.getenv("ENABLE_CORS", "True").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080,https://dehazetransformer.vercel.app,https://*.vercel.app").split(",")

# Model configuration
IMG_SIZE = 256
IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff")

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

print(f"✓ Configuration loaded")
print(f"  - Model path: {MODEL_PATH}")
print(f"  - Adapter path: {ADAPTER_PATH}")
print(f"  - AOD-Net path: {AOD_NET_PATH}")
print(f"  - API running on {API_HOST}:{API_PORT}")
