# Calricula Deployment Guide

This guide covers deploying Calricula to a VPS with automatic SSL via Caddy.

## Prerequisites

- A VPS with Ubuntu 22.04+ (recommended: 2 vCPU, 2-4GB RAM)
- Domain `calricula.com` pointed to your VPS IP
- Firebase project configured
- Google AI API key

## 1. VPS Initial Setup

SSH into your VPS and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# Install Docker Compose plugin
sudo apt install docker-compose-plugin -y

# Log out and back in for group changes
exit
```

SSH back in and verify:

```bash
docker --version
docker compose version
```

## 2. Clone Repository

```bash
# Create app directory
sudo mkdir -p /opt/calricula
sudo chown $USER:$USER /opt/calricula
cd /opt/calricula

# Clone the repository
git clone https://github.com/johnnyphung-laccd/calricula.git .
# Or use scp/rsync to upload files
```

## 3. Configure Environment

```bash
# Copy example environment file
cp .env.production.example .env

# Edit with your values
nano .env
```

Fill in your `.env` file:

```env
# DATABASE
DB_USER=calricula
DB_PASSWORD=YOUR_SECURE_PASSWORD_HERE
DB_NAME=calricula

# GOOGLE AI
GOOGLE_API_KEY=your-google-api-key
GEMINI_FILE_SEARCH_STORE_NAME=calricula-knowledge-base

# FIREBASE
FIREBASE_PROJECT_ID=curricula-de841
NEXT_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=curricula-de841.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=curricula-de841

# LOGGING (optional)
LOG_LEVEL=info
```

## 4. Add Firebase Service Account

Upload your `serviceAccountKey.json` to the project root:

```bash
# From your local machine
scp serviceAccountKey.json user@your-vps-ip:/opt/calricula/
```

Or create it directly on the server:

```bash
nano serviceAccountKey.json
# Paste your service account JSON content
```

**Important:** Set proper permissions:

```bash
chmod 600 serviceAccountKey.json
```

## 5. Configure DNS

In your domain registrar (or Cloudflare/etc.), add these DNS records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_VPS_IP | 300 |
| A | www | YOUR_VPS_IP | 300 |

Wait for DNS propagation (usually 5-15 minutes):

```bash
# Verify DNS is working
dig calricula.com +short
dig www.calricula.com +short
```

## 6. Configure Firebase

In [Firebase Console](https://console.firebase.google.com/):

1. Go to **Authentication** → **Settings** → **Authorized domains**
2. Add `calricula.com`
3. Add `www.calricula.com`

## 7. Build and Deploy

```bash
cd /opt/calricula

# Build production images (takes 3-5 minutes first time)
docker compose -f docker-compose.prod.yml build

# Start all services
docker compose -f docker-compose.prod.yml up -d

# Watch the logs (Ctrl+C to exit)
docker compose -f docker-compose.prod.yml logs -f
```

Wait for all services to be healthy:

```bash
docker compose -f docker-compose.prod.yml ps
```

You should see all services as "healthy".

## 8. Initialize Database

```bash
# Run database migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

# (Optional) Seed with demo data
docker compose -f docker-compose.prod.yml exec backend python -m seeds.seed_all
```

## 9. Verify Deployment

1. Visit https://calricula.com - should show the app with HTTPS
2. Check Caddy obtained SSL certificate:
   ```bash
   docker compose -f docker-compose.prod.yml logs caddy | grep -i certificate
   ```
3. Test login with your Firebase account

## Common Commands

```bash
# View all logs
docker compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend
docker compose -f docker-compose.prod.yml logs -f caddy

# Restart a service
docker compose -f docker-compose.prod.yml restart backend

# Stop everything
docker compose -f docker-compose.prod.yml down

# Stop and remove volumes (DESTROYS DATA)
docker compose -f docker-compose.prod.yml down -v

# Rebuild and restart (after code changes)
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

# Check service health
docker compose -f docker-compose.prod.yml ps

# Access database directly
docker compose -f docker-compose.prod.yml exec db psql -U calricula -d calricula

# Run a backend command
docker compose -f docker-compose.prod.yml exec backend python -m seeds.seed_all
```

## Updating the Application

```bash
cd /opt/calricula

# Pull latest code
git pull origin main

# Rebuild images
docker compose -f docker-compose.prod.yml build

# Restart with new images
docker compose -f docker-compose.prod.yml up -d

# Run any new migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## Backup Database

```bash
# Create backup
docker compose -f docker-compose.prod.yml exec db pg_dump -U calricula calricula > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
cat backup_file.sql | docker compose -f docker-compose.prod.yml exec -T db psql -U calricula calricula
```

## Troubleshooting

### SSL Certificate Not Working

```bash
# Check Caddy logs for errors
docker compose -f docker-compose.prod.yml logs caddy

# Verify DNS is pointing to your server
dig calricula.com +short

# Make sure ports 80 and 443 are open
sudo ufw allow 80
sudo ufw allow 443
```

### Backend Won't Start

```bash
# Check backend logs
docker compose -f docker-compose.prod.yml logs backend

# Common issues:
# - Missing serviceAccountKey.json
# - Invalid .env values
# - Database not ready (wait and retry)
```

### Database Connection Issues

```bash
# Check if database is running
docker compose -f docker-compose.prod.yml ps db

# Check database logs
docker compose -f docker-compose.prod.yml logs db

# Test connection
docker compose -f docker-compose.prod.yml exec db pg_isready -U calricula
```

### Out of Memory

If services crash due to memory:

```bash
# Check memory usage
docker stats

# Add swap space (if needed)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## Security Checklist

- [ ] Strong `DB_PASSWORD` in `.env` (use `openssl rand -base64 32`)
- [ ] `serviceAccountKey.json` has restricted permissions (`chmod 600`)
- [ ] Firewall configured (only ports 80, 443, and SSH open)
- [ ] SSH key authentication enabled, password auth disabled
- [ ] Regular backups configured
- [ ] Firebase authorized domains configured

## Firewall Setup

```bash
# Enable UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status
```

## Resource Usage

Expected resource consumption for ~25 users:

| Service | Memory | CPU |
|---------|--------|-----|
| Caddy | ~50MB | <1% |
| Frontend | ~200MB | <5% |
| Backend | ~300MB | <10% |
| PostgreSQL | ~200MB | <5% |
| **Total** | ~750MB | <20% |

A 2GB RAM VPS should handle this comfortably with room for spikes.
