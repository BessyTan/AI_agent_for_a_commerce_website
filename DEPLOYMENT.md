# Deployment Guide

This guide explains how to deploy the AI Commerce Agent to production.

## Quick Deploy to Render/Vercel

### Backend (Render.com)

1. **Sign up** at [render.com](https://render.com)

2. **Create New Web Service**
   - Connect your GitHub repository
   - Select the `backend` folder
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
   - Environment: Python 3

3. **Environment Variables** (if needed)
   - No environment variables required for basic setup

4. **Deploy** - Click "Save & Deploy"

### Frontend (Vercel.com)

1. **Sign up** at [vercel.com](https://vercel.com)

2. **Import Project**
   - Import your GitHub repository
   - Root directory: `frontend`
   - Framework: Vite

3. **Environment Variables**
   ```
   VITE_API_URL=https://your-render-app.onrender.com
   ```

4. **Deploy** - Click "Deploy"

## Manual Deployment

### Option 1: Docker (Recommended)

#### Backend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

#### Frontend Dockerfile

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### Option 2: Traditional VPS

#### Backend Setup

```bash
# SSH into your server
ssh user@your-server

# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend Setup

```bash
# Build frontend
cd ../frontend
npm install
npm run build

# Copy to nginx
sudo cp -r dist/* /var/www/html/
```

## Environment Configuration

### Backend

No special configuration needed for basic deployment. For production, consider:

- Add CORS restrictions
- Set up HTTPS
- Add rate limiting
- Use PostgreSQL instead of SQLite

### Frontend

Update `.env` or environment variables:

```env
VITE_API_URL=https://your-backend-url.com
```

## Monitoring & Logs

### Render

- View logs: Render dashboard → Your service → Logs
- Monitor metrics: Render dashboard → Your service → Metrics

### Railway

- View logs: Railway dashboard → Your project → Logs
- Set up alerts: Railway dashboard → Project settings

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
pip install -r requirements.txt
```

**Database issues:**
```bash
# Delete and recreate database
rm commerce.db
python main.py
```

### Frontend Issues

**Build errors:**
```bash
rm -rf node_modules
npm install
npm run build
```

**API connection errors:**
- Check `VITE_API_URL` is set correctly
- Verify CORS is enabled on backend
- Check network tab in browser dev tools

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] API calls working from frontend
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Error handling in place
- [ ] Logging configured
- [ ] Database backed up
- [ ] Environment variables set

## Scaling

For high traffic:

1. **Database**: Migrate from SQLite to PostgreSQL
2. **Caching**: Add Redis for caching
3. **CDN**: Use CloudFlare for static assets
4. **Load Balancing**: Multiple backend instances
5. **Queue**: Celery for async tasks

## Support

For issues, check:
- Backend logs
- Frontend console errors
- Network tab in browser
- Render/Vercel status pages

