# Deployment Guide

This guide covers various deployment options for the FinVision AI Insights Service.

## Quick Deploy Options

### 1. Railway (Recommended for Quick Start)

Railway provides the easiest deployment experience.

1. **Sign up at [railway.app](https://railway.app)**

2. **Install Railway CLI** (optional)
```powershell
npm install -g @railway/cli
```

3. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Dockerfile

4. **Set Environment Variables**
   - Go to project settings
   - Add variables:
     - `PORT=8000`
     - `ALLOWED_ORIGINS=https://your-frontend-url.com`
     - `ENVIRONMENT=production`

5. **Deploy**
   - Railway will automatically build and deploy
   - You'll get a public URL: `https://your-service.railway.app`

**Cost:** Free tier available, then $5/month

---

### 2. Render

1. **Sign up at [render.com](https://render.com)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `ai-insights-service` directory

3. **Configure**
   - **Name:** finvision-ai-insights
   - **Environment:** Docker
   - **Region:** Choose closest to your users
   - **Instance Type:** Free (or Starter for production)

4. **Environment Variables**
   ```
   PORT=8000
   ALLOWED_ORIGINS=https://your-frontend.com
   ENVIRONMENT=production
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

**Cost:** Free tier available, $7/month for starter

---

### 3. DigitalOcean App Platform

1. **Sign up at [digitalocean.com](https://www.digitalocean.com/)**

2. **Create New App**
   - Go to Apps → Create App
   - Connect GitHub repository
   - Select branch and `ai-insights-service` directory

3. **Configure**
   - **Resource Type:** Web Service
   - **HTTP Port:** 8000
   - **Build Command:** (Auto-detected from Dockerfile)
   - **Run Command:** (Auto-detected from Dockerfile)

4. **Environment Variables**
   ```
   ALLOWED_ORIGINS=${YOUR_FRONTEND_URL}
   ENVIRONMENT=production
   ```

5. **Choose Plan**
   - Basic: $5/month
   - Professional: $12/month

**Cost:** Starting at $5/month

---

### 4. Google Cloud Run

Cloud Run is serverless and scales to zero when not in use.

1. **Install Google Cloud SDK**
```powershell
# Install from: https://cloud.google.com/sdk/docs/install
```

2. **Authenticate**
```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

3. **Build Container**
```powershell
cd ai-insights-service
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/finvision-ai-insights
```

4. **Deploy**
```powershell
gcloud run deploy finvision-ai-insights `
  --image gcr.io/YOUR_PROJECT_ID/finvision-ai-insights `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "ENVIRONMENT=production,ALLOWED_ORIGINS=https://your-frontend.com"
```

5. **Get URL**
```powershell
gcloud run services describe finvision-ai-insights --region us-central1
```

**Cost:** Pay per request, free tier includes 2M requests/month

---

### 5. AWS ECS with Fargate

1. **Install AWS CLI**
```powershell
# Install from: https://aws.amazon.com/cli/
```

2. **Create ECR Repository**
```powershell
aws ecr create-repository --repository-name finvision-ai-insights
```

3. **Build and Push Image**
```powershell
# Get login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t finvision-ai-insights .

# Tag
docker tag finvision-ai-insights:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finvision-ai-insights:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finvision-ai-insights:latest
```

4. **Create ECS Cluster** (via AWS Console or CLI)
   - Go to ECS → Clusters → Create Cluster
   - Choose "Networking only" (Fargate)

5. **Create Task Definition**
   - Container image: Your ECR image URL
   - Port: 8000
   - Environment variables: Add from .env

6. **Create Service**
   - Launch type: Fargate
   - Configure load balancer (optional)

**Cost:** ~$15-30/month depending on usage

---

### 6. Azure Container Instances

1. **Install Azure CLI**
```powershell
# Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

2. **Login**
```powershell
az login
```

3. **Create Resource Group**
```powershell
az group create --name finvision-rg --location eastus
```

4. **Create Container Registry**
```powershell
az acr create --resource-group finvision-rg --name finvisionacr --sku Basic
```

5. **Build and Push**
```powershell
az acr build --registry finvisionacr --image finvision-ai-insights:latest .
```

6. **Deploy Container**
```powershell
az container create `
  --resource-group finvision-rg `
  --name finvision-ai-insights `
  --image finvisionacr.azurecr.io/finvision-ai-insights:latest `
  --dns-name-label finvision-ai `
  --ports 8000 `
  --environment-variables ENVIRONMENT=production ALLOWED_ORIGINS=https://your-frontend.com
```

**Cost:** ~$10-20/month

---

## Docker Deployment (Self-Hosted)

### Using Your Own Server

1. **Setup Server** (Ubuntu/Debian example)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

2. **Clone Repository**
```bash
git clone https://github.com/yourusername/finvision.git
cd finvision/ai-insights-service
```

3. **Configure Environment**
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

4. **Deploy**
```bash
docker-compose up -d
```

5. **Setup Nginx Reverse Proxy** (optional)
```nginx
server {
    listen 80;
    server_name ai-insights.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ai-insights.yourdomain.com
```

---

## Environment Configuration

### Production Environment Variables

Create a `.env` file with:

```env
# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# CORS - IMPORTANT: Set your actual frontend URL
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com

# Logging
LOG_LEVEL=INFO

# Model Cache
MODEL_CACHE_DIR=/app/models
```

---

## Monitoring and Logging

### Add Health Check Monitoring

Use services like:
- **UptimeRobot**: Free uptime monitoring
- **Better Uptime**: More features, free tier available
- **Pingdom**: Professional monitoring

Monitor endpoint: `https://your-service.com/api/v1/health`

### Logging

Most platforms provide built-in logging:
- **Railway**: View logs in dashboard
- **Render**: Logs tab in service settings
- **Cloud Run**: Google Cloud Logging
- **AWS**: CloudWatch Logs

---

## Scaling Considerations

### Horizontal Scaling
The service is stateless, so you can run multiple instances:
- Railway/Render: Adjust instance count in settings
- Cloud Run: Auto-scales based on traffic
- AWS ECS: Set desired task count

### Performance Tips
1. Use Redis for caching (add to docker-compose.yml)
2. Enable request compression
3. Implement rate limiting
4. Use CDN for static assets
5. Monitor response times

---

## CI/CD Setup

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]
    paths:
      - 'ai-insights-service/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          # Railway auto-deploys on push
          echo "Deployed to Railway"
```

---

## Database Integration (Optional)

If you want to store transaction history:

1. **Add PostgreSQL to docker-compose.yml**
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: finvision_ai
      POSTGRES_USER: finvision
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

2. **Update requirements.txt**
```
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
```

3. **Add DATABASE_URL to .env**
```
DATABASE_URL=postgresql://finvision:password@postgres:5432/finvision_ai
```

---

## Security Checklist

- [ ] Set strong random values for any secrets
- [ ] Restrict CORS to only your frontend domains
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add API authentication if needed
- [ ] Keep dependencies updated
- [ ] Monitor for security vulnerabilities
- [ ] Use environment variables for all secrets
- [ ] Enable firewall rules
- [ ] Regular security audits

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Scaling |
|----------|-----------|-----------|---------|
| Railway | 500 hours/month | $5+/month | Auto |
| Render | 750 hours/month | $7+/month | Auto |
| DigitalOcean | None | $5+/month | Manual |
| Google Cloud Run | 2M requests/month | Pay per use | Auto |
| AWS Fargate | 1 year free | $15+/month | Auto |
| Azure | $200 credit | Variable | Auto |

---

## Troubleshooting

### Common Issues

**Port already in use:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process
taskkill /PID <PID> /F
```

**Docker build fails:**
```powershell
# Clear Docker cache
docker system prune -a
# Rebuild
docker-compose build --no-cache
```

**CORS errors:**
- Check ALLOWED_ORIGINS in .env
- Ensure frontend URL matches exactly
- Include protocol (http:// or https://)

---

## Support

For deployment help, check:
- Platform-specific documentation
- GitHub Issues
- Community forums

## Next Steps

After deployment:
1. Test all endpoints
2. Set up monitoring
3. Configure CI/CD
4. Update frontend to use production URL
5. Monitor logs for errors
6. Set up backups (if using database)
