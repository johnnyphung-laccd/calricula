# Calricula VPS Deployment Guide

This guide covers deploying Calricula on a VPS (Virtual Private Server), specifically optimized for Hetzner but applicable to any VPS provider.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [VPS Requirements](#vps-requirements)
3. [Initial Server Setup](#initial-server-setup)
4. [Deployment Modes](#deployment-modes)
5. [Demo Mode Deployment](#demo-mode-deployment)
6. [Production Mode Deployment](#production-mode-deployment)
7. [Firebase Setup](#firebase-setup)
8. [Google AI Setup](#google-ai-setup)
9. [Domain Configuration](#domain-configuration)
10. [Maintenance](#maintenance)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, you'll need:

- A VPS account (Hetzner, DigitalOcean, AWS, etc.)
- A domain name (e.g., `calricula.com`)
- Basic knowledge of SSH and command line
- A GitHub account (to clone the repository)

---

## VPS Requirements

### Minimum Specifications (Demo Mode)
- **CPU:** 1-2 vCPUs
- **RAM:** 2GB
- **Storage:** 20GB SSD
- **OS:** Ubuntu 22.04 LTS or 24.04 LTS

### Recommended Specifications (Production)
- **CPU:** 2-4 vCPUs
- **RAM:** 4GB
- **Storage:** 40GB SSD
- **OS:** Ubuntu 22.04 LTS or 24.04 LTS

### Hetzner Server Recommendations

**For Demo Mode:**
- Server: **CX21** (2 vCPU, 4GB RAM, 40GB SSD)
- Cost: ~€4.26/month
- Location: Choose closest to your users (e.g., `hil` for US West)

**For Production:**
- Server: **CPX21** (3 vCPU, 4GB RAM, 160GB SSD)
- Cost: ~€9.56/month
- Or **CPX31** (4 vCPU, 8GB RAM, 240GB SSD) for higher traffic
- Location: Choose closest to your users

---

## Initial Server Setup

### 1. Create the VPS

1. Log in to your Hetzner Cloud Console
2. Click "Create Server"
3. Choose location (recommended: `hil` - Hillsboro, Oregon for US users)
4. Choose OS: **Ubuntu 24.04** (or 22.04 LTS)
5. Choose server type (see recommendations above)
6. Add SSH key (recommended) or use root password
7. Click "Create Server"

### 2. Connect to the Server

```bash
# Replace with your server IP
ssh root@your.server.ip

# If using SSH key:
ssh -i ~/.ssh/your_key root@your.server.ip
```

### 3. Update the System

```bash
apt update && apt upgrade -y
```

### 4. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Enable Docker to start on boot
systemctl enable docker

# Verify installation
docker --version
docker compose version
```

### 5. Install Additional Tools

```bash
# Install useful tools
apt install -y git curl wget vim htop fail2ban ufw
```

### 6. Configure Firewall

```bash
# Allow SSH
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw --force enable

# Check status
ufw status
```

---

## Deployment Modes

Calricula supports three deployment modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Development** | Local development with hot reload | Local development |
| **Demo** | Public demo with daily resets | Public demonstrations |
| **Production** | Full production with persistence | Live production use |

Choose your deployment mode below:

- [Demo Mode Deployment](#demo-mode-deployment) - For public demos
- [Production Mode Deployment](#production-mode-deployment) - For live use

---

## Demo Mode Deployment

Demo mode is ideal for public demonstrations. It:
- Allows anyone with "demo" in their email to sign up/login
- Resets all data every day at midnight
- Uses a separate isolated database

### 1. Clone the Repository

```bash
# Install git if not already installed
apt install git -y

# Clone the repository
cd /opt
git clone https://github.com/johnnyphung-laccd/calricula.git
cd calricula
```

### 2. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit the .env file
vim .env
```

**Required environment variables for Demo Mode:**

```bash
# ===========================================
# Application Mode
# ===========================================
DEMO_MODE=true
NEXT_PUBLIC_DEMO_MODE=true
AUTH_DEV_MODE=false
NEXT_PUBLIC_AUTH_DEV_MODE=false

# ===========================================
# Demo Database
# ===========================================
DEMO_DB_NAME=calricula_demo
DEMO_DB_USER=calricula_demo
DEMO_DB_PASSWORD=CHANGE_THIS_TO_A_SECURE_PASSWORD

# ===========================================
# Demo Domain
# ===========================================
DEMO_DOMAIN=demo.calricula.com

# ===========================================
# Google AI (Required)
# ===========================================
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_FILE_SEARCH_STORE_NAME=calricula-knowledge-base

# ===========================================
# Firebase (Required)
# ===========================================
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_firebase_project_id

# ===========================================
# Other Settings
# ===========================================
LOG_LEVEL=info
```

### 3. Add Firebase Service Account Key

```bash
# Download your Firebase service account key from Firebase Console
# Then upload it to the server (from your local machine):
scp serviceAccountKey.json root@your.server.ip:/opt/calricula/

# Or create it directly on the server (paste the content):
vim /opt/calricula/serviceAccountKey.json
```

**IMPORTANT:** The service account key should be a JSON file that looks like:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-...@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

### 4. Create Caddyfile for Demo Mode

```bash
# Create the demo Caddyfile
vim Caddyfile.demo
```

**Content for `Caddyfile.demo`:**

```caddy
{$DEMO_DOMAIN:demo.calricula.com} {
    # Health check endpoint
    handle /caddy-health {
        respond "OK" 200
    }

    # Backend API proxy
    handle /api/* {
        reverse_proxy backend:8000
    }

    # Frontend proxy
    handle /* {
        reverse_proxy frontend:3000
    }

    # Log all requests
    log {
        output file /var/log/caddy/demo_access.log
    }
}
```

### 5. Start the Demo Mode Services

```bash
# Build and start the services
docker compose -f docker-compose.demo.yml up -d --build

# Check the status
docker compose -f docker-compose.demo.yml ps

# View logs
docker compose -f docker-compose.demo.yml logs -f
```

### 6. Run Database Migrations and Seeds

```bash
# Wait for the database to be ready (about 10 seconds)
sleep 10

# Run migrations
docker compose -f docker-compose.demo.yml exec backend alembic upgrade head

# Seed the demo database
docker compose -f docker-compose.demo.yml exec backend python -m seeds.seed_all

# Create the golden master backup
docker compose -f docker-compose.demo.yml exec db pg_dump -U calricula_demo calricula_demo > demo_db_backup.sql
```

### 7. Configure DNS

1. Go to your domain registrar (e.g., Namecheap, GoDaddy, Cloudflare)
2. Add an **A Record**:
   - **Name:** `demo` (or `@` for root domain)
   - **Type:** `A`
   - **Value:** Your server IP address
   - **TTL:** 3600 (or default)

Example:
```
Type: A
Name: demo
Value: 123.45.67.89
TTL: 3600
```

### 8. Verify Deployment

1. Wait for DNS to propagate (can take 5-30 minutes)
2. Visit `https://demo.calricula.com` (replace with your domain)
3. You should see the Calricula login page with a demo banner

### 9. Create Demo User in Firebase

To allow demo users to sign up:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Authentication** → **Users** tab
4. Click **Add user**
5. Create a user with "demo" in the email (e.g., `demo@example.com`)
6. Set a password
7. The user can now log in to the demo site

---

## Production Mode Deployment

Production mode is for live usage with real data persistence.

### 1. Clone the Repository

```bash
cd /opt
git clone https://github.com/johnnyphung-laccd/calricula.git
cd calricula
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
vim .env
```

**Required environment variables for Production:**

```bash
# ===========================================
# Application Mode
# ===========================================
DEMO_MODE=false
NEXT_PUBLIC_DEMO_MODE=false
AUTH_DEV_MODE=false
NEXT_PUBLIC_AUTH_DEV_MODE=false

# ===========================================
# Production Database
# ===========================================
DB_NAME=calricula
DB_USER=calricula
DB_PASSWORD=CHANGE_THIS_TO_A_SECURE_PASSWORD

# ===========================================
# Domain
# ===========================================
DOMAIN=calricula.com

# ===========================================
# Google AI (Required)
# ===========================================
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_FILE_SEARCH_STORE_NAME=calricula-knowledge-base

# ===========================================
# Firebase (Required)
# ===========================================
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_firebase_project_id

# ===========================================
# Other Settings
# ===========================================
ENVIRONMENT=production
LOG_LEVEL=info
```

### 3. Add Firebase Service Account Key

```bash
# Upload your service account key
scp serviceAccountKey.json root@your.server.ip:/opt/calricula/
```

### 4. Review and Update Caddyfile

```bash
vim Caddyfile
```

**Content for `Caddyfile`:**

```caddy
{$DOMAIN:calricula.com} {
    # Health check endpoint
    handle /caddy-health {
        respond "OK" 200
    }

    # Backend API proxy
    handle /api/* {
        reverse_proxy backend:8000
    }

    # Frontend proxy
    handle /* {
        reverse_proxy frontend:3000
    }

    # Log all requests
    log {
        output file /var/log/caddy/production_access.log
    }
}
```

### 5. Start Production Services

```bash
# Build and start
docker compose -f docker-compose.prod.yml up -d --build

# Check status
docker compose -f docker-compose.prod.yml ps
```

### 6. Run Database Migrations and Seeds

```bash
# Wait for database
sleep 10

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

# For production, you may want to seed reference data only
docker compose -f docker-compose.prod.yml exec backend python -m seeds.seed_reference_data
```

### 7. Configure DNS

Add an **A Record** for your domain:
```
Type: A
Name: @
Value: your.server.ip
TTL: 3600
```

---

## Firebase Setup

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **Add project**
3. Enter project name (e.g., `calricula-production`)
4. Disable Google Analytics (optional)
5. Click **Create project**

### 2. Enable Authentication

1. In Firebase Console, go to **Build** → **Authentication**
2. Click **Get Started**
3. Enable **Email/Password** provider
4. Click **Save**

### 3. Get Web Configuration

1. Click the **Web icon** (</>) to add a web app
2. App nickname: `Calricula Web`
3. Copy the configuration (you'll need it for `.env`):
   - `apiKey`
   - `authDomain`
   - `projectId`

### 4. Generate Service Account Key

1. Go to **Project Settings** (gear icon)
2. Go to **Service Accounts** tab
3. Click **Generate new private key**
4. Save as `serviceAccountKey.json`
5. **IMPORTANT:** Keep this file secure and never commit it to Git

### 5. Configure Email Verification (Optional but Recommended)

1. In Firebase Console, go to **Authentication** → **Templates**
2. Edit **Email verification** template
3. Customize for your institution

---

## Google AI Setup

### 1. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the API key
5. Add to `.env` as `GOOGLE_API_KEY`

### 2. Configure RAG Knowledge Base (Optional)

The app will automatically create the knowledge base store on first run.

---

## Domain Configuration

### Subdomain Structure

You can use different subdomains for different modes:

| Subdomain | Mode | Purpose |
|-----------|------|---------|
| `calricula.com` | Production | Live production site |
| `demo.calricula.com` | Demo | Public demo |
| `staging.calricula.com` | Staging | Testing before production |

### SSL Certificates

Caddy automatically obtains and renews SSL certificates from Let's Encrypt. No manual configuration needed!

---

## Maintenance

### View Logs

```bash
# Demo mode
docker compose -f docker-compose.demo.yml logs -f

# Production
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.demo.yml logs -f backend
```

### Restart Services

```bash
# Demo mode
docker compose -f docker-compose.demo.yml restart

# Production
docker compose -f docker-compose.prod.yml restart
```

### Update the Application

```bash
cd /opt/calricula

# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose -f docker-compose.demo.yml up -d --build
```

### Database Backups (Production Only)

```bash
# Create backup
docker compose -f docker-compose.prod.yml exec db pg_dump -U calricula calricula > backup_$(date +%Y%m%d).sql

# Restore from backup
cat backup_20241201.sql | docker compose -f docker-compose.prod.yml exec -T db psql -U calricula calricula
```

### Manual Demo Database Reset

```bash
# Trigger immediate reset
docker compose -f docker-compose.demo.yml exec demo-reset /demo-reset.sh
```

### Monitor Resources

```bash
# Check resource usage
htop

# Check Docker stats
docker stats

# Check disk usage
df -h
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose -f docker-compose.demo.yml logs

# Check for port conflicts
netstat -tulpn

# Restart Docker
systemctl restart docker
```

### Database Connection Issues

```bash
# Check if database is running
docker compose -f docker-compose.demo.yml ps db

# Check database logs
docker compose -f docker-compose.demo.yml logs db

# Test database connection
docker compose -f docker-compose.demo.yml exec backend python -c "from app.core.database import engine; print(engine.connect())"
```

### SSL Certificate Issues

```bash
# Check Caddy logs
docker compose -f docker-compose.demo.yml logs caddy

# Restart Caddy
docker compose -f docker-compose.demo.yml restart caddy
```

### Firebase Authentication Issues

1. Verify `FIREBASE_SERVICE_ACCOUNT_PATH` is correct
2. Check that `serviceAccountKey.json` exists and is valid JSON
3. Verify Firebase project ID matches
4. Check backend logs for authentication errors

### Demo Reset Not Working

```bash
# Check demo-reset service logs
docker compose -f docker-compose.demo.yml logs demo-reset

# Manually trigger reset
docker compose -f docker-compose.demo.yml exec demo-reset /demo-reset.sh

# Check reset state
docker compose -f docker-compose.demo.yml exec demo-reset cat /state/demo_last_reset.txt
```

---

## Security Best Practices

1. **Never commit `.env` or `serviceAccountKey.json` to Git**
2. Use strong, unique passwords for database
3. Keep the server updated: `apt update && apt upgrade -y`
4. Enable automatic security updates:
   ```bash
   apt install unattended-upgrades -y
   dpkg-reconfigure -plow unattended-upgrades
   ```
5. Use SSH keys instead of password authentication
6. Regularly check logs for suspicious activity
7. Set up monitoring/alerting (recommended: UptimeRobot, StatusCake)

---

## Cost Summary

### Hetzner Monthly Costs

| Server Type | RAM | CPU | Storage | Monthly |
|-------------|-----|-----|---------|---------|
| CX21 | 4GB | 2 vCPU | 40GB SSD | ~€4.26 |
| CPX21 | 4GB | 3 vCPU | 160GB SSD | ~€9.56 |
| CPX31 | 8GB | 4 vCPU | 240GB SSD | ~€19.44 |

### Additional Services

- **Domain:** ~$10-15/year
- **Firebase:** Free tier available
- **Google AI:** Free tier available

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/johnnyphung-laccd/calricula/issues
- Documentation: See `calricula_docs/` directory

---

**Last Updated:** 2025-01-04
