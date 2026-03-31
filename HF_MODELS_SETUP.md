# 🎯 HuggingFace Space Model Setup Guide

## Problem
The Docker build failed because the model repository `Arnoobie/dehaze-models` doesn't exist yet. We need to either:
1. **Option A**: Create the model repository and upload models (recommended for production)
2. **Option B**: Upload model files directly to the Space via web interface (quick test)

---

## Option A: Create HuggingFace Model Repository ⭐ Recommended

### Step 1: Create Model Repository
1. Go to [huggingface.co/new](https://huggingface.co/new)
2. Fill in:
   - **Model name**: `dehaze-models`
   - **Owner**: Select your profile (Arnoobie)
   - **License**: MIT (or your choice)
   - **Model card metadata**: Optional
3. Click **Create repository**

### Step 2: Upload Model Files

You can upload files via the web interface or command line:

#### Via Web Interface (Easy)
1. Go to [huggingface.co/Arnoobie/dehaze-models](https://huggingface.co/Arnoobie/dehaze-models)
2. Click **Files and versions** tab
3. Click **Upload file(s)**
4. Upload these files:
   - `maxim_savedmodel/` folder (entire directory with saved_model.pb and variables/)
   - `adapter_best.weights.h5`
5. Commit

#### Via Command Line (Fast batch upload)
```bash
cd C:\Users\KIIT0001\OneDrive\Documents\Dehaze\Dehaze\backend

# Upload maxim_savedmodel folder
hf.exe upload-large-folder Arnoobie/dehaze-models maxim_savedmodel/

# Upload adapter weights
hf.exe upload Arnoobie/dehaze-models adapter_best.weights.h5
```

**Note**: Replace `hf.exe` with `hf` if on macOS/Linux

### Step 3: Verify Upload
1. Visit [huggingface.co/Arnoobie/dehaze-models/tree/main](https://huggingface.co/Arnoobie/dehaze-models/tree/main)
2. You should see both files uploaded
3. If private, add HF token to .env or Space secrets

### Step 4: Update Space Configuration
If you made the repo **private**, set environment variable in HF Space:
1. Go to [huggingface.co/spaces/Arnoobie/dehaze-ai/settings](https://huggingface.co/spaces/Arnoobie/dehaze-ai/settings)
2. Scroll to **Repository secrets**
3. Click **Add secret**
4. Name: `HF_TOKEN`
5. Value: Your HuggingFace write token (from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
6. Click **Add secret**

### Step 5: Trigger Space Rebuild
1. Go to Space: [huggingface.co/spaces/Arnoobie/dehaze-ai](https://huggingface.co/spaces/Arnoobie/dehaze-ai)
2. Click **Settings** → **Restart Space** 
3. Wait 5-10 minutes for rebuild

**Result**: On startup, `download_models.py` will fetch models from your repo!

---

## Option B: Manual Upload to Space Files

### Quick Method (For Testing)
1. Go to [huggingface.co/spaces/Arnoobie/dehaze-ai](https://huggingface.co/spaces/Arnoobie/dehaze-ai)
2. Click **Files and versions** tab
3. Create folder `maxim_savedmodel/` and upload:
   - `saved_model.pb`
   - `variables/` folder (with its contents)
4. Upload `adapter_best.weights.h5`
5. Commit
6. **Settings** → **Restart Space**

**Pros**: Quick test  
**Cons**: Models stored in Space (uses 100MB+ quota)

---

## After Setup Complete

Once models are uploaded, check your Space status:

✅ **Expected behavior**:
1. Docker builds successfully
2. Models are downloaded at startup
3. API endpoints become available

🔍 **Monitor logs**:
- Go to Space → **Logs** tab
- Should see: `✓ maxim_savedmodel downloaded` or `✓ maxim_savedmodel already exists`

📡 **Test the API**:
```bash
curl https://Arnoobie-dehaze-ai.hf.space/api/health
# Should return: {"status": "ok", "models_loaded": true, ...}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build still fails | Check Space logs for exact error |
| "Repository Not Found" | Verify repo exists at huggingface.co/Arnoobie/dehaze-models |
| 401 Unauthorized | Set HF_TOKEN in Space secrets (for private repos) |
| Slow startup | First inference takes ~30-60s to download/load models |
| Models not found | Ensure files are in correct paths (see config.py for fallback locations) |

---

## Model Files Location

The backend looks for models in this order:
1. Environment variables: `MODEL_PATH`, `ADAPTER_PATH`
2. Local paths: `Dehaze/maxim_savedmodel`, `Dehaze/adapter_best.weights.h5`
3. Downloaded paths: `/app/models/maxim_savedmodel`, `/app/models/adapter_best.weights.h5`

This gives flexibility for local testing, git tracking, and cloud deployment!

