# 🚀 QUICK DEPLOYMENT CHECKLIST

Your project is now ready to deploy! Follow these 3 steps to get your app live.

---

## ✅ STEP 1: VERIFY GITHUB PUSH

Your repository: **https://github.com/arnav-glitch/DehazeVer1**

```bash
# Verify push was successful
git log --oneline -n 3
# You should see the deployment commit
```

**Status: ✅ COMPLETE**

---

## 🚂 STEP 2: DEPLOY BACKEND ON RAILWAY (15-20 minutes)

### A. Create Railway Account
1. Go to **https://railway.app**
2. Sign up with GitHub (recommended)
3. Click "New Project"

### B. Connect Your Repository
1. Select **"Deploy from GitHub repo"**
2. Authorize Railway to access your GitHub
3. Search & select **`DehazeVer1`**
4. Click "Deploy"

### C. Configure Service
Once the repo is imported:

1. **Root Directory:** Leave empty (Railway will auto-detect)
2. **Build Command:**
   ```
   cd Dehaze && pip install -r backend/requirements.txt
   ```
3. **Start Command:**
   ```
   cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

### D. Add Environment Variables
In Railway dashboard **→ Variables tab**, add:
```
API_HOST=0.0.0.0
FLASK_ENV=production
ENABLE_CORS=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-vercel-app.vercel.app
```

*(Update the last one later with your Vercel URL)*

### E. Deploy
- Click **"Deploy"** button
- Wait for build (~3-5 minutes)
- Once complete, note your Railway URL: **https://your-service-name.railway.app**

**Status: ⏳ MANUAL (You do this)**

---

## 🎨 STEP 3: DEPLOY FRONTEND ON VERCEL (10-15 minutes)

### A. Create Vercel Account
1. Go to **https://vercel.com**
2. Sign up with GitHub (recommended)
3. Click "Add New Project"

### B. Import Repository
1. Select **"Import Git Repository"**
2. Paste: **https://github.com/arnav-glitch/DehazeVer1**
3. Click "Import"

### C. Configure Project
1. **Framework Preset:** React
2. **Root Directory:** `Dehaze/frontend`
3. **Build Command:** `npm run build`
4. **Output Directory:** `build`
5. Click **"Continue"**

### D. Add Environment Variables
1. Set **REACT_APP_API_URL** to your Railway backend URL
   - Example: `https://dehaze-backend-prod.railway.app`
2. Click **"Deploy"**

### E. Wait & Verify
- Build starts automatically (~3-5 minutes)
- Once complete, your frontend is at: **https://your-app.vercel.app**
- Check header shows "API ONLINE" ✅

**Status: ⏳ MANUAL (You do this)**

---

## 🔗 STEP 4: CONNECT SERVICES

### A. Update Backend CORS
Back in Railway dashboard Variables, update:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-vercel-frontend.vercel.app
```

### B. Redeploy Backend
Push a small commit to trigger Railway redeploy:
```bash
git commit --allow-empty -m "chore: update CORS for production"
git push
```

### C. Test Full Stack
1. Open your Vercel app
2. Upload an image to test dehazing
3. Verify metrics compute correctly

**Status: ⏳ MANUAL (You do this)**

---

## 📋 BEFORE YOU START

Make sure you have:
- [ ] GitHub account created
- [ ] Railway account created
- [ ] Vercel account created
- [ ] All accounts connected to GitHub

---

## 🆘 TROUBLESHOOTING

### Issue: "API OFFLINE" in frontend
**Solution:**
1. Check Railway is running (dashboard shows green "deployed")
2. Check Vercel env var is correct
3. Wait 2-3 minutes after Railway deployment

### Issue: Railway build fails
**Solution:**
1. Check Railway build logs
2. Verify TensorFlow/PyTorch dependencies are installing
3. Consider Railway Pro if CPU insufficient

### Issue: Vercel build fails
**Solution:**
1. Check Vercel build logs
2. Run `npm run build` locally to test
3. Ensure Node 16+ is used

---

## 📊 DEPLOYMENT SUMMARY

| Component | Platform | Time | Status |
|-----------|----------|------|--------|
| GitHub Repo | GitHub | ✅ Done | Ready |
| Backend API | Railway | ⏳ Next | Manual |
| Frontend App | Vercel | ⏳ Then | Manual |
| DNS/Custom | Optional | Later | Optional |

---

## 🎯 FINAL CHECKS

Once deployed, verify:
- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend loads and shows "API ONLINE"
- [ ] Image upload works
- [ ] Dehazing completes successfully
- [ ] Metrics compute (if ground truth provided)
- [ ] Results can be downloaded

---

**Ready to deploy? Start with Step 2 above!** 🚀

