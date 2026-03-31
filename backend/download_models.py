"""Download models from HuggingFace Hub at startup."""
from huggingface_hub import snapshot_download, hf_hub_download
import os

REPO_ID = "Arnoobie/dehaze-models"  # HuggingFace model repository
MODEL_DIR = "/app/models"

def download_models():
    """Download MAXIM and adapter models from HF Hub."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    if not os.path.exists(f"{MODEL_DIR}/maxim_savedmodel"):
        print("Downloading maxim_savedmodel from HuggingFace...")
        snapshot_download(
            repo_id=REPO_ID,
            local_dir=MODEL_DIR,
            ignore_patterns=["*.h5"]
        )
    
    if not os.path.exists(f"{MODEL_DIR}/adapter_best.weights.h5"):
        print("Downloading adapter weights from HuggingFace...")
        hf_hub_download(
            repo_id=REPO_ID,
            filename="adapter_best.weights.h5",
            local_dir=MODEL_DIR
        )
    
    print("✓ All models downloaded and ready")

if __name__ == "__main__":
    download_models()
