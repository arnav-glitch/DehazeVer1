# Deploy Backend to HuggingFace Spaces

This guide walks you through deploying the Dehaze backend API to HuggingFace Spaces.

## 📋 Prerequisites

- HuggingFace account (https://huggingface.co)
- Your models uploaded to HuggingFace (Arnoobie/dehaze-models)
- Git configured with HuggingFace credentials

## 🚀 Step 1: Create HuggingFace Space

1. Go to **https://huggingface.co/new-space**
2. Fill in:
   - **Space name:** `dehaze-ai` (or any name)
   - **License:** Openrail-M (or MIT)
   - **SDK:** Docker
   - **Visibility:** Public

3. Click **"Create Space"**

Your Space is now at: `https://huggingface.co/spaces/Arnoobie/dehaze-ai`

## 🔗 Step 2: Add HF Space as Git Remote

From your local `Dehaze` directory:

```bash
cd backend
git remote add space https://huggingface.co/spaces/Arnoobie/dehaze-ai
```

Replace `Arnoobie` with your actual HuggingFace username.

## 📤 Step 3: Push Backend to HF Spaces

From the `backend` folder:

```bash
git subtree push --prefix backend space main
```

This pushes only the `backend` folder to the Space's `main` branch.

## ⏳ Step 4: Wait for Build

HuggingFace will:
1. Pull your backend code
2. Build the Docker image
3. Download models from your HF repo
4. Start the API server

Go to your Space URL to monitor the build:
`https://huggingface.co/spaces/Arnoobie/dehaze-ai`

Look for:
- **Build status** indicator (should turn green)
- **Logs** tab to see build progress
- **App** tab once deployed

## ✅ Step 5: Verify Deployment

Once built, your API will be at:
`https://Arnoobie-dehaze-ai.hf.space`

Test the health endpoint:
```bash
curl https://Arnoobie-dehaze-ai.hf.space/api/health
```

Expected response:
```json
{"status": "ok"}
```

## 🔗 Step 6: Update Frontend with New URL

Update your Vercel environment variable:
```
REACT_APP_API_URL=https://Arnoobie-dehaze-ai.hf.space
```

## 📝 Step 7: Push Updates

Whenever you update the backend code:

```bash
git add backend/*
git commit -m "update backend code"
git push origin main
git subtree push --prefix backend space main
```

HuggingFace will auto-rebuild.

## 🆘 Troubleshooting

### Build fails with "Model download error"
- Verify `Arnoobie/dehaze-models` repo is public
- Check download_models.py has correct REPO_ID
- Ensure models are uploaded to HF

### Build times out
- Increase Space hardware: Space Settings → Runtime → Select GPU (costs credits)
- Or use CPU - should work but slower

### API returns 503
- Space might still be initializing (first boot can take 2-3 min)
- Check Logs tab in Space dashboard

### CORS errors in frontend
- Update config.py CORS_ORIGINS to include your Vercel domain
- Redeploy to Space

## 📊 What Happens on Deploy

When you push to HF Spaces:

1. **Docker builds** (2-3 min)
   ```
   FROM python:3.11-slim
   RUN apt-get install libglib2.0-0 libsm6 libxext6...
   RUN pip install tensorflow-cpu fastapi...
   ```

2. **Models download** (~20-30 sec)
   ```
   Downloading maxim_savedmodel from HuggingFace...
   ✓ All models downloaded and ready
   ```

3. **API starts** (10-20 sec)
   ```
   Loading models...
   ✓ MAXIM-S2 loaded via TFSMLayer
   ✓ Adapter weights injected successfully
   ✓ MiDaS depth model loaded (CPU)
   
   INFO: Uvicorn running on http://0.0.0.0:7860
   ```

4. **Space goes live** ✅

## 🎯 Key Files

- `backend/Dockerfile` - Container definition
- `backend/README.md` - HF Spaces metadata (must include YAML header)
- `backend/app.py` - FastAPI entry point
- `backend/download_models.py` - Model download logic
- `backend/requirements.txt` - Dependencies

## 💡 Pro Tips

- HF Spaces runs on **port 7860** (not 5001)
- Models are cached in the Docker image (no re-download)
- Use Space Secrets for sensitive env vars (tokens, etc.)
- Monitor build time and resource usage in Settings tab

## 📚 Reference

- HF Spaces docs: https://huggingface.co/docs/hub/spaces
- Docker SDK docs: https://huggingface.co/docs/hub/spaces-sdks-docker
- Your Space: https://huggingface.co/spaces/Arnoobie/dehaze-ai
- Your Models: https://huggingface.co/Arnoobie/dehaze-models

---

**Once deployed, your backend is live and accessible globally!** 🎉

Update `REACT_APP_API_URL` in Vercel and your full stack is complete.

