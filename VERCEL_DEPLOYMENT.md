# 🚀 Vercel Frontend Deployment Guide

## Setup Instructions

### 1. Connect GitHub to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New" → "Project"
3. Import Git Repository: Select `arnav-glitch/DehazeVer1`
4. Select `frontend` as the root directory

### 2. Configure Environment Variables
In Vercel Project Settings → Environment Variables, add:

```
REACT_APP_API_URL=https://Arnoobie-dehaze-ai.hf.space
```

**Note:** Update `https://Arnoobie-dehaze-ai.hf.space` to match your actual HF Space URL once deployed.

### 3. Build Settings
- **Framework Preset**: Create React App
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Root Directory**: `frontend`

### 4. Deploy
1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Your frontend will be available at a URL like: `dehazetransformer.vercel.app`

## Testing After Deployment

1. Visit your Vercel domain
2. Upload a hazy image
3. Should show dehazed result (or error if HF Space backend is still building)

## Troubleshooting

**Frontend not connecting to backend:**
- Check that `REACT_APP_API_URL` is set correctly in Vercel
- Verify HF Space has finished building and is running
- Check browser console for CORS errors

**"API Offline" message:**
- HF Space might still be building (can take 5-10 minutes)
- Check [HF Space status](https://huggingface.co/spaces/Arnoobie/dehaze-ai)

## Update API URL Later

If you change the backend URL:
1. Go to Vercel Project Settings → Environment Variables
2. Update `REACT_APP_API_URL`
3. Vercel will auto-redeploy

