# 🚀 Project NEER Deployment Guide

## 📋 Prerequisites
- GitHub account (✅ You already have this)
- Google Earth Engine account
- Vercel account (free)
- Railway account (free)

## 🌐 Deployment Steps

### Step 1: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** with your GitHub account
3. **Create New Project** → **Deploy from GitHub repo**
4. **Select**: `ANONYMOUSZED-beep/project-neer-dashboard`
5. **IMPORTANT - Configure Service Settings**:
   - Click on the service that was created
   - Go to **Settings** tab
   - Under **Source**, set **Root Directory**: `backend`
   - Under **Build**, set **Build Command**: `pip install -r requirements.txt`
   - Under **Deploy**, set **Start Command**: `python app.py`
6. **Environment Variables** (if needed):
   - `PORT`: (Railway sets this automatically)
   - `GOOGLE_APPLICATION_CREDENTIALS`: (Add your Earth Engine credentials if needed)
7. **Redeploy** and note your Railway URL (e.g., `https://your-app.railway.app`)

### Step 1 Alternative: Fix Current Deployment

If you want to fix the current deployment:
1. Go to your Railway project settings
2. Click on **Settings**
3. Under **Source** section, set **Root Directory** to: `backend`
4. Under **Build** section, set **Build Command** to: `pip install -r requirements.txt`
5. Under **Deploy** section, set **Start Command** to: `python app.py`
6. Click **Redeploy**

### Step 2: Deploy Frontend to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Sign up/Login** with your GitHub account
3. **Import Project** → **Import Git Repository**
4. **Select**: `ANONYMOUSZED-beep/project-neer-dashboard`
5. **Configure**:
   - Framework Preset: **React**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
6. **Environment Variables**:
   - `REACT_APP_API_URL`: `https://your-railway-url.railway.app/api`
7. **Deploy**

### Step 3: Update Environment Variables

After Railway deployment, update the frontend environment:
1. Go to your Vercel project settings
2. Add environment variable:
   - Name: `REACT_APP_API_URL`
   - Value: `https://[your-railway-url].railway.app/api`
3. Redeploy

## 🔗 Alternative Deployment Options

### Option 2: Netlify + Heroku
- **Frontend**: Netlify (free tier)
- **Backend**: Heroku (limited free tier)

### Option 3: AWS Amplify + AWS Lambda
- **Frontend**: AWS Amplify
- **Backend**: AWS Lambda + API Gateway

### Option 4: Digital Ocean App Platform
- **Full-stack**: Single platform deployment

## 🛠️ Post-Deployment Configuration

1. **Update CORS settings** in Flask if needed
2. **Configure Google Earth Engine** credentials for production
3. **Set up custom domain** (optional)
4. **Enable HTTPS** (usually automatic)

## 📊 Expected Results

After successful deployment:
- **Frontend URL**: `https://your-project.vercel.app`
- **Backend API**: `https://your-project.railway.app/api`
- **Features**: All lake monitoring, charts, and maps working online

## 🔍 Troubleshooting

- **CORS errors**: Check backend CORS configuration
- **API not found**: Verify environment variables
- **Build failures**: Check Node.js/Python versions
- **Maps not loading**: Verify Leaflet/MapBox configuration

## 💡 Pro Tips

1. **Use environment variables** for all API URLs
2. **Enable monitoring** on Railway/Vercel
3. **Set up CI/CD** for automatic deployments
4. **Configure error tracking** (e.g., Sentry)
5. **Add analytics** (e.g., Google Analytics)
