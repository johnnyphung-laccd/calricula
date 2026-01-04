# Calricula Demo Mode - Quick Start Guide

This guide helps you quickly set up and run Calricula in **Demo Mode**.

## What is Demo Mode?

Demo mode allows users with "demo" in their email address to:
- Access the full application
- Make changes and explore features
- Test all functionality

The demo database **resets every day at midnight** back to its original state.

---

## Quick Start (Local Development)

### 1. Set Environment Variables

Create or edit your `.env` file:

```bash
# Enable Demo Mode
DEMO_MODE=true
NEXT_PUBLIC_DEMO_MODE=true

# Disable Dev Mode (demo mode uses real Firebase)
AUTH_DEV_MODE=false
NEXT_PUBLIC_AUTH_DEV_MODE=false
```

### 2. Start the Services

```bash
# Use the demo docker-compose configuration
docker compose -f docker-compose.demo.yml up -d --build
```

### 3. Run Database Setup

```bash
# Wait for database to be ready (~10 seconds)
sleep 10

# Run migrations
docker compose -f docker-compose.demo.yml exec backend alembic upgrade head

# Seed the demo database
docker compose -f docker-compose.demo.yml exec backend python -m seeds.seed_all
```

### 4. Access the Application

- **URL:** http://localhost:3001
- **Demo User:** Create a Firebase user with "demo" in the email
  - Example: `demo@example.com`
  - The backend will verify the email contains "demo"

### 5. Test the Demo Reset

```bash
# Manually trigger a database reset
docker compose -f docker-compose.demo.yml exec demo-reset /demo-reset.sh
```

---

## Demo Mode vs Dev Mode vs Production

| Feature | Dev Mode | Demo Mode | Production |
|---------|----------|-----------|------------|
| **Purpose** | Local development | Public demo | Live production |
| **Auth** | Mock users (no Firebase) | Firebase (demo emails only) | Firebase (all users) |
| **Database** | Resets manually | Resets daily at midnight | Persistent |
| **URL** | localhost | demo.calricula.com | calricula.com |
| **SSL** | No | Yes (Caddy) | Yes (Caddy) |

---

## Demo Mode Authentication

Demo mode requires **Firebase Authentication**. Users must:

1. Have "demo" in their email address (e.g., `demo@example.com`, `mydemo@company.com`)
2. Sign up through Firebase Authentication
3. The backend will verify the email contains "demo" before granting access

### Creating Demo Users

**Option 1: Self-Service (Recommended)**
- Enable email/password sign-up in Firebase
- Users can create their own accounts with "demo" in their email

**Option 2: Admin-Created**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Authentication → Users
3. Click "Add user"
4. Create user with "demo" in email

---

## Daily Reset Behavior

Every day at midnight (server time), the demo database will:

1. **Drop all data** - All courses, programs, users, etc. are deleted
2. **Restore from backup** - The "golden master" backup is restored
3. **Continue running** - The application restarts with fresh data

Users will see:
- All their changes gone
- The original demo data restored
- A fresh demo environment

---

## Running Demo Mode on a VPS

For public demo deployment (e.g., on Hetzner), see:
- **[VPS_DEPLOYMENT.md](./VPS_DEPLOYMENT.md)** - Complete VPS deployment guide

**Quick VPS commands:**

```bash
# On your VPS
cd /opt/calricula

# Edit .env and set:
# DEMO_MODE=true
# NEXT_PUBLIC_DEMO_MODE=true
# DEMO_DOMAIN=demo.yourdomain.com

# Start demo mode
docker compose -f docker-compose.demo.yml up -d --build

# Run migrations
docker compose -f docker-compose.demo.yml exec backend alembic upgrade head

# Seed database
docker compose -f docker-compose.demo.yml exec backend python -m seeds.seed_all

# Create golden master backup
docker compose -f docker-compose.demo.yml exec db pg_dump -U calricula_demo calricula_demo > demo_db_backup.sql
```

---

## Monitoring Demo Mode

### Check Reset Status

```bash
docker compose -f docker-compose.demo.yml exec demo-reset cat /state/demo_last_reset.txt
```

### View Reset Logs

```bash
docker compose -f docker-compose.demo.yml logs demo-reset
```

### View All Logs

```bash
docker compose -f docker-compose.demo.yml logs -f
```

---

## Stopping Demo Mode

```bash
# Stop all services
docker compose -f docker-compose.demo.yml down

# Stop and remove volumes (deletes all data)
docker compose -f docker-compose.demo.yml down -v
```

---

## Troubleshooting

### Demo users can't log in

1. Check that Firebase is configured in `.env`:
   ```bash
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
   ```

2. Verify the email contains "demo" (case-insensitive)

3. Check backend logs:
   ```bash
   docker compose -f docker-compose.demo.yml logs backend
   ```

### Database reset not working

1. Check demo-reset service is running:
   ```bash
   docker compose -f docker-compose.demo.yml ps demo-reset
   ```

2. Manually trigger reset:
   ```bash
   docker compose -f docker-compose.demo.yml exec demo-reset /demo-reset.sh
   ```

3. Check reset service logs:
   ```bash
   docker compose -f docker-compose.demo.yml logs demo-reset
   ```

### Can't access the application

1. Check all services are running:
   ```bash
   docker compose -f docker-compose.demo.yml ps
   ```

2. Check for errors in logs:
   ```bash
   docker compose -f docker-compose.demo.yml logs
   ```

3. Verify ports are not in use:
   ```bash
   netstat -tulpn | grep -E ':(3000|8000|80|443)'
   ```

---

## Security Notes

- **Demo mode is NOT for production data** - All data is reset daily
- **Anyone with "demo" in their email can access** - Only use for public demos
- **Firebase is still required** - Demo mode uses real Firebase authentication
- **Keep service account key secure** - Never commit to Git

---

## Next Steps

- For full VPS deployment: **[VPS_DEPLOYMENT.md](./VPS_DEPLOYMENT.md)**
- For production deployment: Use `docker-compose.prod.yml`
- For development: Use `docker-compose.yml`

---

**Last Updated:** 2025-01-04
