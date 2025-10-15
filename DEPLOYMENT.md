# EmpathZ Demo - Serverless Deployment Guide

## Quick Deploy to Vercel (Recommended)

### Prerequisites
1. Install Vercel CLI: `npm i -g vercel`
2. Have a GitHub account
3. Push your code to GitHub

### Deployment Steps

#### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

#### 2. Deploy to Vercel
```bash
# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: empathz-demo
# - Framework: Other
# - Root directory: ./
# - Override settings? Yes
```

#### 3. Configure Production Domain
```bash
# Set custom domain (optional)
vercel domains add empathz-demo.com

# Deploy to production
vercel --prod
```

### Alternative: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/crisisline_demo)

## Other Serverless Options

### Option 2: Netlify + Railway

#### Frontend (Netlify)
1. Connect GitHub repo to Netlify
2. Build command: `echo "Static HTML"`
3. Publish directory: `frontend/`

#### Backend (Railway)
1. Connect GitHub repo to Railway
2. Select `backend/` as root directory
3. Railway auto-detects Python/FastAPI
4. Deploy automatically

### Option 3: AWS Serverless

#### Frontend (S3 + CloudFront)
```bash
# Build and upload to S3
aws s3 sync frontend/ s3://your-bucket-name
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

#### Backend (Lambda)
```bash
# Package for Lambda
pip install -r backend/requirements.txt -t backend/
cd backend && zip -r lambda-deployment.zip .
```

## Environment Variables

### Production Settings
```bash
# Vercel Environment Variables
vercel env add NODE_ENV production
vercel env add API_URL https://your-domain.vercel.app/api
```

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend  
cd frontend
python3 -m http.server 3000
```

## Monitoring & Analytics

### Vercel Analytics
- Automatic performance monitoring
- Real user metrics
- Error tracking

### Custom Monitoring
```javascript
// Add to frontend/index.html
<script>
  // Custom analytics
  window.addEventListener('error', (e) => {
    console.error('App Error:', e.error);
  });
</script>
```

## Performance Optimization

### Frontend
- ✅ Single HTML file (minimal bundle)
- ✅ CDN delivery via Vercel
- ✅ Gzip compression
- ✅ Browser caching

### Backend
- ✅ Serverless functions (auto-scaling)
- ✅ Edge computing via Vercel
- ✅ Optimized Python runtime

## Cost Estimation

### Vercel (Recommended)
- **Free Tier**: 100GB bandwidth, 100GB-hours functions
- **Pro**: $20/month for unlimited bandwidth
- **Perfect for**: Demo, small production apps

### Netlify + Railway
- **Netlify**: Free tier (100GB bandwidth)
- **Railway**: $5/month hobby plan
- **Total**: ~$5/month

### AWS
- **S3**: ~$0.50/month for static hosting
- **Lambda**: Pay per request (~$1-10/month)
- **CloudFront**: ~$1/month
- **Total**: ~$2-15/month

## Troubleshooting

### Common Issues

#### CORS Errors
```python
# Update backend/main.py
allow_origins=["https://your-domain.vercel.app"]
```

#### API Not Found
```bash
# Check Vercel routing in vercel.json
{
  "routes": [
    {"src": "/api/(.*)", "dest": "backend/main.py"}
  ]
}
```

#### Build Failures
```bash
# Check Python version compatibility
python --version  # Should be 3.8+
```

### Debug Commands
```bash
# Check deployment logs
vercel logs

# Test API locally
curl http://localhost:8000/api/calls

# Test production API
curl https://your-domain.vercel.app/api/calls
```

## Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **CORS**: Restrict to known domains
3. **Rate Limiting**: Add API rate limits
4. **HTTPS**: Always use SSL in production
5. **Input Validation**: Validate all API inputs

## Scaling Considerations

- **Vercel**: Auto-scales to 1000+ concurrent requests
- **Database**: Consider PlanetScale/Neon for data persistence
- **CDN**: Vercel Edge Network provides global distribution
- **Monitoring**: Add Sentry for error tracking

