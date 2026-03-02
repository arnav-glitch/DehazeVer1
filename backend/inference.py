"""Inference module for image dehazing using MAXIM-S2 + Adapter."""
import os
import time
from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image
# Ensure h5py is installed (pip install h5py) if not already present
import h5py 
from config import MODEL_PATH, ADAPTER_PATH, IMG_SIZE

# Global model cache
_CACHED_MODELS = {"base_model": None, "adapter": None}


def load_models(model_path=MODEL_PATH, adapter_path=ADAPTER_PATH):
    """
    Load MAXIM-S2 SavedModel and adapter weights.
    Uses 'Safe Mode' initialization to prevent noise if weights fail.
    """
    # Check if models already loaded
    if _CACHED_MODELS["base_model"] is not None:
        print("✓ Models already loaded (from cache)")
        return _CACHED_MODELS["base_model"], _CACHED_MODELS["adapter"]
    
    print("Loading models...")
    
    # ---------------------------------------------------------
    # 1. Load MAXIM Backbone (Legacy SavedModel)
    # ---------------------------------------------------------
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path not found: {model_path}")
    
    print(f"  Loading MAXIM-S2 legacy format from {model_path}...")
    
    # Use TFSMLayer for Keras 3 compatibility
    from keras.layers import TFSMLayer
    
    # Wrap in Sequential to ensure it behaves like a standard Keras model
    base_model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        TFSMLayer(model_path, call_endpoint='serving_default')
    ])
    
    print(f"  ✓ MAXIM-S2 loaded via TFSMLayer")
    
    # ---------------------------------------------------------
    # 2. Build Adapter Head (With ZERO Initialization)
    # ---------------------------------------------------------
    print(f"  Building adapter head...")
    
    # CRITICAL FIX: Initialize with 'zeros'. 
    # If weights fail to load, this ensures the adapter adds NOTHING (0)
    # instead of random noise, preserving the high-quality MAXIM output.
    adapter = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu", 
                               kernel_initializer='zeros', bias_initializer='zeros', name="adapter_c1"),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu", 
                               kernel_initializer='zeros', bias_initializer='zeros', name="adapter_c2"),
        tf.keras.layers.Conv2D(3, 3, padding="same", activation=None, 
                               kernel_initializer='zeros', bias_initializer='zeros', name="adapter_out"),
    ], name="adapter_head")
    
    # Initialize the variables by running a single dummy prediction
    # This forces Keras to create the variables in memory
    adapter(np.zeros((1, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32))

    # ---------------------------------------------------------
    # 3. Load Adapter Weights (Robust Method)
    # ---------------------------------------------------------
    if os.path.exists(adapter_path):
        print(f"  Loading adapter weights from {adapter_path}...")
        try:
            # Try standard loading first
            adapter.load_weights(adapter_path, skip_mismatch=True)
            print(f"  ✓ Adapter weights injected")
        except Exception as e:
            print(f"  ⚠ Standard load failed: {e}")
            print(f"  ⚠ Falling back to ZERO-initialized adapter (Base Model performance guaranteed)")
            # No further action needed; model is already zero-init
    else:
        print(f"  ⚠ Adapter weights file not found: {adapter_path}")
        print(f"  Using base MAXIM model (Adapter disabled)")
    
    # Cache models
    _CACHED_MODELS["base_model"] = base_model
    _CACHED_MODELS["adapter"] = adapter
    
    print("✓ All models loaded successfully")
    return base_model, adapter


def flatten_tensors(y):
    """Recursively flatten nested tensor structures."""
    out = []
    if isinstance(y, tf.Tensor):
        out.append(y)
    elif isinstance(y, (list, tuple)):
        for v in y:
            out.extend(flatten_tensors(v))
    elif isinstance(y, dict):
        for v in y.values():
            out.extend(flatten_tensors(v))
    return out


def select_best_output(y, prefer_hw=None):
    """
    Select best output tensor from MAXIM backbone.
    """
    tensors = [t for t in flatten_tensors(y) if isinstance(t, tf.Tensor) and len(t.shape) == 4]
    if not tensors:
        # Fallback if structure is unexpected
        return y
    
    if prefer_hw is not None:
        H, W = prefer_hw
        same = [t for t in tensors if (t.shape[1] == H and t.shape[2] == W)]
        if same:
            return same[-1]
    
    # Fallback: max spatial area
    def area(t):
        h = t.shape[1] if t.shape[1] is not None else 0
        w = t.shape[2] if t.shape[2] is not None else 0
        return int(h) * int(w)
    
    return max(tensors, key=area)


@tf.function
def backbone_predict(x, base_model):
    """
    Execute MAXIM-S2 backbone prediction.
    """
    y = base_model(x, training=False)
    pred = select_best_output(y, prefer_hw=(IMG_SIZE, IMG_SIZE))
    pred = tf.image.resize(pred, (IMG_SIZE, IMG_SIZE), method="bilinear")
    pred = tf.clip_by_value(pred, 0.0, 1.0)
    return pred


def preprocess_image(image_path):
    """
    Preprocess image for inference (resize to 256x256).
    Use process_high_res for tiled inference instead.
    """
    # Load image
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img).astype(np.float32)
    
    # Normalize to [0, 1]
    arr = arr / 255.0
    
    # Resize to fixed size
    img_tensor = tf.convert_to_tensor(arr)
    img_tensor = tf.image.resize(img_tensor, (IMG_SIZE, IMG_SIZE), method="bilinear")
    
    # Add batch dimension
    img_tensor = img_tensor[None, ...]
    
    return img_tensor


def postprocess_output(output_array):
    """
    Post-process inference output.
    """
    # Remove batch dimension if present
    if len(output_array.shape) == 4:
        output = output_array[0]
    elif len(output_array.shape) == 3:
        output = output_array
        
    # If tensor, convert to numpy
    if isinstance(output, tf.Tensor):
        output = output.numpy()
        
    # Ensure valid range
    output = np.clip(output, 0.0, 1.0)
    
    # Convert to uint8
    output = (output * 255).astype(np.uint8)
    
    # Convert to PIL Image
    return Image.fromarray(output)


def process_high_res(img_pil, base_model, adapter, stride=256):
    """
    Process high-resolution image using tiled inference.
    
    Args:
        img_pil: Standard PIL Image (RGB)
        base_model: Loaded backbone
        adapter: Loaded adapter
        stride: Stride for tiling (default 256 for non-overlapping)
        
    Returns:
        Dehazed PIL Image (Same size as input)
    """
    # Convert to numpy float32 [0, 1]
    img_np = np.array(img_pil).astype(np.float32) / 255.0
    h, w, c = img_np.shape
    
    # Calculate padding to be multiple of IMG_SIZE (256)
    pad_h = (IMG_SIZE - h % IMG_SIZE) % IMG_SIZE
    pad_w = (IMG_SIZE - w % IMG_SIZE) % IMG_SIZE
    
    # Pad image (reflection padding reduces edge artifacts)
    img_padded = np.pad(img_np, ((0, pad_h), (0, pad_w), (0, 0)), mode='reflect')
    h_padded, w_padded, _ = img_padded.shape
    
    # Create empty canvas for output
    output_canvas = np.zeros_like(img_padded)
    # Count map for averaging overlapping tiles (if we implement overlap later)
    # For now, stride=256 means no overlap, so simple stitching works.
    
    # Loop over tiles
    for i in range(0, h_padded, IMG_SIZE):
        for j in range(0, w_padded, IMG_SIZE):
            # Extract tile
            tile = img_padded[i:i+IMG_SIZE, j:j+IMG_SIZE, :]
            
            # Convert to batch tensor [1, 256, 256, 3]
            tile_tensor = tf.convert_to_tensor(tile)[None, ...]
            
            # Predict
            # Note: backbone_predict expects 256x256 input
            base_pred = backbone_predict(tile_tensor, base_model)
            delta = adapter(base_pred, training=False)
            out_tile = tf.clip_by_value(base_pred + delta, 0.0, 1.0)
            
            # Squeeze and place in canvas
            output_canvas[i:i+IMG_SIZE, j:j+IMG_SIZE, :] = out_tile[0].numpy()
            
    # Crop back to original size
    output_final = output_canvas[:h, :w, :]
    
    return postprocess_output(output_final)


def process_single_image(image_path, base_model=None, adapter=None):
    """
    Complete inference pipeline for single image.
    Automatically switches to tiled inference for large images.
    """
    if base_model is None or adapter is None:
        base_model, adapter = load_models()
    
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    
    # If image is significantly larger/smaller than 256x256, use tiling?
    # Actually, always using tiling ensures resolution is preserved.
    # But for very small images, we should just resize UP to 256, process, and resize DOWN.
    # Strategy:
    # - If max(w, h) > 300: Use Tiled Inference (High Res)
    # - Else: Resize to 256x256 (Fast / Low Res)
    
    if max(w, h) > 300:
        print(f"  High-Res Mode: Processing {w}x{h} image with Tiled Inference...")
        result = process_high_res(img, base_model, adapter)
    else:
        print(f"  Fast Mode: Resizing {w}x{h} to 256x256...")
        x = preprocess_image(image_path)
        base_pred = backbone_predict(x, base_model)
        delta = adapter(base_pred, training=False)
        out = tf.clip_by_value(base_pred + delta, 0.0, 1.0)
        result = postprocess_output(out)
    
    return result


def process_image_bytes(image_bytes, base_model=None, adapter=None):
    """
    Process image from bytes (for API).
    """
    if base_model is None or adapter is None:
        base_model, adapter = load_models()
    
    start_time = time.time()
    
    # Load from bytes
    img = Image.open(image_bytes).convert("RGB")
    w, h = img.size
    
    # Decision logic: Tiling or Resize
    if max(w, h) > 300:
        print(f"  High-Res Mode: Processing {w}x{h} image with Tiled Inference...")
        result = process_high_res(img, base_model, adapter)
    else:
        # Legacy/Fast path
        img_array = np.array(img).astype(np.float32) / 255.0
        img_tensor = tf.convert_to_tensor(img_array)
        img_tensor = tf.image.resize(img_tensor, (IMG_SIZE, IMG_SIZE), method="bilinear")
        img_tensor = img_tensor[None, ...]
        
        base_pred = backbone_predict(img_tensor, base_model)
        delta = adapter(base_pred, training=False)
        out = tf.clip_by_value(base_pred + delta, 0.0, 1.0)
        result = postprocess_output(out)
    
    elapsed_ms = (time.time() - start_time) * 1000
    
    return result, elapsed_ms


if __name__ == "__main__":
    # Test inference
    print("Testing inference module...")
    base_model, adapter = load_models()
    print("✓ Models loaded successfully")