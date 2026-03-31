# Railway Deployment — Environment Variables Setup

After the HuggingFace model download integration has been pushed, follow these steps in your Railway dashboard:

## 📋 Step 1: Log into Railway Dashboard

1. Go to **https://dashboard.railway.app**
2. Select your Dehaze project
3. Click on the service (backend API)

## 🔧 Step 2: Open Variables in Raw Editor

1. Click the **"Variables"** tab
2. Click **"Raw Editor"** button (top-right)
3. Clear any existing content if present

## 📝 Step 3: Paste Environment Variables

Copy and paste this entire block:

```
API_HOST=0.0.0.0
API_PORT=$PORT
FLASK_ENV=production
FLASK_DEBUG=False
ENABLE_CORS=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-vercel-frontend.vercel.app
UPLOAD_FOLDER=/app/uploads
RESULTS_FOLDER=/app/results
MAX_FILE_SIZE=10485760
IMG_SIZE=256
MODEL_PATH=/app/models/maxim_savedmodel
ADAPTER_PATH=/app/models/adapter_best.weights.h5
AOD_NET_PATH=/app/models/adapter_aod.weights.h5
```

**Important:** Replace `your-vercel-frontend.vercel.app` with your actual Vercel domain after deployment.

## 🚀 Step 4: Deploy

1. Click **"Save Variables"**
2. Railway will automatically redeploy with new env vars
3. On first boot, the download script will:
   - Create `/app/models` directory
   - Download `maxim_savedmodel` from HuggingFace
   - Download `adapter_best.weights.h5` from HuggingFace
   - Print `✓ All models downloaded and ready`

## 📊 What Happens on Startup

When your Railway service starts:

```
✓ Configuration loaded
  - Model path: /app/models/maxim_savedmodel
  - Adapter path: /app/models/adapter_best.weights.h5
  - AOD-Net path: /app/models/adapter_aod.weights.h5

Downloading maxim_savedmodel from HuggingFace...
✓ All models downloaded and ready

Loading models...
  ✓ MAXIM-S2 loaded via TFSMLayer
  ✓ Adapter weights injected successfully
  ✓ MiDaS depth model loaded (CPU)
✓ All models loaded successfully

INFO: Uvicorn running on http://0.0.0.0:$PORT
```

## ✅ Verification Checklist

- [ ] Variables pasted in Railway Raw Editor
- [ ] `$PORT` is set (Railway auto-provides this)
- [ ] `CORS_ORIGINS` includes your Vercel URL
- [ ] "Deploy" button is ready to click
- [ ] Models will download on first boot (~30-60 seconds)
- [ ] Check Railway logs to confirm successful download

## 🆘 Troubleshooting

### "Model download failed"
- Verify your HuggingFace token has repository access
- Check that `Arnoobie/dehaze-models` repo is public
- Wait 1-2 minutes for download to complete

### "Connection timeout"
- Railway needs internet access to download from HF
- This is normal on first deployment (one-time)
- Subsequent deployments use cached downloads

### Still seeing old error?
- Clear Railway cache: "Settings" → "Deploy" → "Clear cache and redeploy"
- Or push a new commit to trigger fresh deployment

## 📚 Reference

- **HF Model Repo:** https://huggingface.co/Arnoobie/dehaze-models
- **Download Script:** `backend/download_models.py`
- **App Entry Point:** `backend/app.py` (calls download_models on startup)
- **Dependencies:** Added to `backend/requirements.txt`

---

**Once these variables are set and deployed, your backend will be production-ready on Railway!** 🚀

