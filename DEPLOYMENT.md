# DEHAZE.AI — Full Stack Deployment Guide

Complete walkthrough for deploying to GitHub, Railway (Backend), and Vercel (Frontend).

## 📋 Prerequisites

- GitHub account & git installed
- Railway account (railway.app)
- Vercel account (vercel.com)
- Node.js 16+ & npm installed
- Python 3.9+ with pip

---

## 🚀 Step 1: Push to GitHub

### 1.1 Initialize / Check Git Status

```bash
cd Dehaze
git status  # Verify repository is initialized
```

### 1.2 Configure Git (if needed)

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.3 Stage, Commit & Push

```bash
git add .
git commit -m "feat: set up full stack deployment configuration"
git push origin main
```

**Expected:** All files committed to GitHub on `main` branch.

---

## 🚂 Step 2: Deploy Backend on Railway

### 2.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your Dehaze repository
4. Connect & authorize GitHub

### 2.2 Configure Backend Service

1. In Railway dashboard, create a new service:
   - Click "Add Service" → "GitHub repo"
   - Select your repo → sync

2. **Service Settings:**
   - Root Directory: `Dehaze` (or leave empty if at repo root)
   - Deployment Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables** (Railway dashboard → Variables):
   ```
   API_HOST=0.0.0.0
   API_PORT=$PORT
   FLASK_ENV=production
   ENABLE_CORS=True
   CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-vercel-app.vercel.app
   ```

### 2.3 Deploy

- Railway auto-deploys on push to main
- Check deployment status in dashboard
- Once deployed, note your Railway backend URL (e.g., `https://dehaze-backend-prod-railway.app`)

---

## 🎨 Step 3: Deploy Frontend on Vercel

### 3.1 Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project" → "Import Git Repository"
3. Select your Dehaze repository

### 3.2 Configure Build

**Project Settings:**
- **Framework Preset:** React
- **Root Directory:** `Dehaze/frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `build`
- **Install Command:** `npm install`

### 3.3 Environment Variables

In Vercel dashboard → Project Settings → Environment Variables:

```
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

Replace `your-railway-backend.railway.app` with actual Railway URL from Step 2.3

### 3.4 Deploy

- Click "Deploy"
- Vercel auto-deploys on push to main
- Wait for build to complete (~3-5 min)
- Your app is now live at `https://your-app.vercel.app`

---

## 🔗 Step 4: Connect Services

### 4.1 Update Backend CORS

In Railway dashboard → Variables, update:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-app.vercel.app
```

(Replace with actual Vercel URL)

### 4.2 Redeploy Backend

Push an empty commit to trigger Railway redeploy:
```bash
git commit --allow-empty -m "chore: update CORS for production"
git push
```

### 4.3 Test Full Stack

1. Open your Vercel app: `https://your-app.vercel.app`
2. Check header for "API ONLINE" status
3. Upload an image to test dehazing
4. Metrics should compute from backend

---

## 📝 Local Development Setup

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5001
```

### Frontend
```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:5001 npm start  # Runs on http://localhost:3000
```

---

## 🔍 Troubleshooting

### Frontend shows "API OFFLINE"
- Check Vercel env var `REACT_APP_API_URL` is set correctly
- Verify Railway backend is running (check Railway dashboard)
- Check CORS origins include Vercel domain

### Railway deployment fails
- Check build logs in Railway dashboard
- Ensure `backend/requirements.txt` exists and is valid
- Verify Python 3.9+ is available

### Vercel build fails
- Check build logs in Vercel dashboard
- Run `npm run build` locally to debug
- Ensure `frontend/package.json` exists

### Models not loading on Railway
- Railroad has limitations. For intensive models (MAXIM-S2, MiDaS):
  - Consider Railway Pro tier for more CPU/memory
  - Or use a faster dehazing model for initial deploy
  - Or deploy on Railway with GPU support (Advanced)

---

## 🎯 Production Checklist

- [ ] GitHub repo initialized & pushed
- [ ] Railway backend deployed & running
- [ ] Vercel frontend deployed & running
- [X] CORS configured in backend
- [ ] Environment variables set in both services
- [ ] API health check shows "ONLINE"
- [ ] Image dehazing works end-to-end
- [ ] Metrics compute correctly (if ground truth provided)

---

## 📞 Quick References

| Service | URL | Dashboard |
|---------|-----|-----------|
| Backend | `https://your-railway-backend.railway.app/api/health` | railway.app |
| Frontend | `https://your-app.vercel.app` | vercel.com |
| Repo | `https://github.com/you/Dehaze` | github.com |

---

## 🚀 Next Steps

After successful deployment:
1. Monitor logs in Railway & Vercel dashboards
2. Set up GitHub Actions for CI/CD (optional)
3. Add custom domain to Vercel (optional)
4. Enable analytics on Vercel (optional)

