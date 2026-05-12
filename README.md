# 📬 ContactForm App

A production-ready **Flask + PostgreSQL** contact-form application fully containerised with **Docker Compose**, with automatic local deployment via **GitHub Actions self-hosted runner**.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Tech Stack](#tech-stack)
3. [Local Setup (without Docker)](#local-setup-without-docker)
4. [Docker Setup](#docker-setup)
5. [GitHub Setup](#github-setup)
6. [Self-Hosted Runner Setup](#self-hosted-runner-setup)
7. [How Auto-Deployment Works](#how-auto-deployment-works)
8. [Database Migrations](#database-migrations)
9. [Environment Variables](#environment-variables)
10. [Troubleshooting](#troubleshooting)

---

## Project Structure

```
contact-form-app/
│
├── app/
│   ├── templates/
│   │   ├── base.html          # Navbar, flash messages, footer
│   │   ├── index.html         # Contact form page
│   │   └── submissions.html   # Admin list of all submissions
│   ├── static/
│   │   ├── css/style.css      # Custom styling (Bootstrap override)
│   │   └── js/main.js         # Char counter + loading spinner
│   ├── app.py                 # Flask application factory
│   ├── models.py              # SQLAlchemy ContactSubmission model
│   ├── forms.py               # WTForms ContactForm + validation
│   └── routes.py              # URL routes / views
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD workflow
│
├── Dockerfile                 # Multi-stage production image
├── docker-compose.yml         # Orchestrates web + db services
├── requirements.txt           # Python dependencies
├── init.sql                   # First-run SQL executed by Postgres
├── .env.example               # Environment variable template
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Backend        | Python 3.12 · Flask 3             |
| Frontend       | HTML5 · Bootstrap 5 · Vanilla JS  |
| Database       | PostgreSQL 16                     |
| ORM            | SQLAlchemy 2 (via Flask-SQLAlchemy)|
| Migrations     | Flask-Migrate (Alembic)           |
| Forms          | Flask-WTF · WTForms               |
| Containerization | Docker · Docker Compose          |
| CI/CD          | GitHub Actions (self-hosted runner)|
| Web Server     | Gunicorn (2 workers)              |

---

## Local Setup (without Docker)

> Useful for development. Requires **Python 3.12+** and a running PostgreSQL instance.

```bash
# 1. Clone the repository
git clone https://github.com/<your-user>/<your-repo>.git
cd contact-form-app

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env
# Edit .env with your local PostgreSQL credentials

# 5. Set FLASK_APP and run migrations
export FLASK_APP=app/app.py
flask --app app/app.py db init      # only the very first time
flask --app app/app.py db migrate -m "initial"
flask --app app/app.py db upgrade

# 6. Run the development server
cd app
flask run --host=0.0.0.0 --port=5000
```

Open **http://localhost:5000** in your browser.

---

## Docker Setup

> The recommended way to run the application. Requires **Docker Desktop** (or Docker Engine + Compose plugin).

### First run

```bash
# 1. Clone the repo
git clone https://github.com/<your-user>/<your-repo>.git
cd contact-form-app

# 2. Create your .env file from the example
cp .env.example .env

# 3. (Optional) edit .env with a strong SECRET_KEY and DB password
nano .env        # or: code .env  / vim .env

# 4. Build images and start all services in the background
docker compose up -d --build
```

The first `docker compose up --build`:
- Builds the Flask image (multi-stage, ~200 MB)
- Starts the `db` (PostgreSQL) container
- Waits for the DB health check to pass
- Runs `flask db upgrade` (creates tables via Alembic)
- Starts **Gunicorn** on port 5000

### Useful commands

```bash
# View live logs
docker compose logs -f

# View logs for just one service
docker compose logs -f web
docker compose logs -f db

# Restart only the web service (e.g. after a code change without CI)
docker compose up -d --build web

# Stop everything (keeps the DB volume)
docker compose down

# Stop everything AND delete the database volume (clean slate)
docker compose down -v

# Shell into the web container
docker compose exec web sh

# Shell into the PostgreSQL container
docker compose exec db psql -U contactuser -d contactdb

# Check health status
docker compose ps
```

### Accessing the app

| URL                          | Description                   |
|------------------------------|-------------------------------|
| http://localhost:5000        | Contact form                  |
| http://localhost:5000/submissions | List of all submissions  |
| http://localhost:5000/health | Docker health-check endpoint  |

---

## GitHub Setup

```bash
# 1. Create a new repository on github.com (or use an existing one)

# 2. Initialise git in the project (if not done already)
cd contact-form-app
git init
git add .
git commit -m "Initial commit"

# 3. Add your remote and push
git remote add origin https://github.com/<your-user>/<your-repo>.git
git branch -M main
git push -u origin main
```

### Add the ENV_FILE secret

The deploy workflow writes your `.env` file from a GitHub Actions secret so
credentials are never stored in the repository.

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ENV_FILE`
4. Value: paste the entire contents of your `.env` file
5. Click **Add secret**

---

## Self-Hosted Runner Setup

> **Why is this needed?**  
> GitHub-hosted runners run on GitHub's cloud servers. They have no way to reach
> your local machine. A **self-hosted runner** is a small background agent you
> install on your own computer. GitHub sends jobs to it, and it executes them
> locally — giving the workflow full access to your Docker environment.

### Install the runner on your local machine

```bash
# 1. Go to your GitHub repo
#    Settings → Actions → Runners → "New self-hosted runner"
#    Select your OS (Linux / macOS / Windows) and follow the on-screen commands.
#    The steps below are the typical Linux/macOS flow:

# 2. Create a directory for the runner
mkdir ~/actions-runner && cd ~/actions-runner

# 3. Download the runner package (GitHub shows the exact URL for your OS)
#    Example for Linux x64:
curl -o actions-runner-linux-x64-2.317.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.317.0/actions-runner-linux-x64-2.317.0.tar.gz

# 4. Extract
tar xzf ./actions-runner-linux-x64-2.317.0.tar.gz

# 5. Configure — GitHub generates a unique TOKEN for you on the Runners page
./config.sh --url https://github.com/<your-user>/<your-repo> --token <YOUR_TOKEN>
#   When prompted:
#     Runner group   → press Enter (default)
#     Runner name    → e.g. "my-local-machine"
#     Labels         → press Enter (keeps "self-hosted")
#     Work folder    → press Enter (default _work)

# 6. Start the runner as a background service (recommended)

# macOS:
./svc.sh install
./svc.sh start

# Linux (systemd):
sudo ./svc.sh install
sudo ./svc.sh start

# To check status:
./svc.sh status

# To stop:
./svc.sh stop
```

Once installed, the runner appears as **Online** in
*GitHub → Settings → Actions → Runners*.

### Ensure Docker is accessible to the runner

The runner process must be able to run `docker` and `docker compose`
without `sudo`.

```bash
# Add your user to the docker group (Linux only — restart session after)
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker ps
```

---

## How Auto-Deployment Works

```
Developer pushes code to GitHub (main branch)
          │
          ▼
GitHub detects push → triggers Actions workflow
          │
          ▼
GitHub sends job to your LOCAL self-hosted runner
          │
          ▼
Runner checks out latest code on your machine
          │
          ▼
Runner writes .env from GitHub secret
          │
          ▼
docker compose build --no-cache   ← builds updated image
          │
          ▼
docker compose down               ← stops old containers
          │
          ▼
docker compose up -d              ← starts updated containers
          │                         (includes: flask db upgrade)
          ▼
Health check passes → workflow succeeds
          │
          ▼
Updated app running at http://localhost:5000 ✅
```

Total time from `git push` to live update: **~2–4 minutes** (mostly image build).

---

## Database Migrations

Flask-Migrate (Alembic) handles schema changes without data loss.

```bash
# Generate a new migration after changing models.py
docker compose exec web flask db migrate -m "describe your change"

# Apply pending migrations
docker compose exec web flask db upgrade

# Roll back one migration
docker compose exec web flask db downgrade

# View migration history
docker compose exec web flask db history
```

The `docker-compose.yml` `command:` already runs `flask db upgrade` on every
container start, so new migrations are applied automatically on deploy.

---

## Environment Variables

| Variable            | Description                                  | Default (example)              |
|---------------------|----------------------------------------------|--------------------------------|
| `SECRET_KEY`        | Flask secret key for CSRF / sessions         | `change-me-in-production`      |
| `FLASK_ENV`         | `production` or `development`                | `production`                   |
| `FLASK_DEBUG`       | `true` / `false`                             | `false`                        |
| `FLASK_PORT`        | Port exposed by Docker                       | `5000`                         |
| `POSTGRES_DB`       | Database name                                | `contactdb`                    |
| `POSTGRES_USER`     | Database user                                | `contactuser`                  |
| `POSTGRES_PASSWORD` | Database password                            | `supersecretpassword`          |
| `DATABASE_URL`      | Full SQLAlchemy URI (auto-built by compose)  | `postgresql://user:pw@db/db`   |

---

## Troubleshooting

### App won't start — "could not connect to server"

The web container started before PostgreSQL was ready.

```bash
docker compose down
docker compose up -d
# The healthcheck on db ensures web waits — allow ~30 s
docker compose logs -f web
```

### Port 5000 already in use

```bash
# Find what's using it
lsof -i :5000          # macOS/Linux
netstat -ano | findstr 5000   # Windows

# Change the port in .env:
FLASK_PORT=8080
docker compose up -d
```

### Migrations fail on startup

```bash
# Run interactively to see the error
docker compose exec web flask db upgrade

# If the migrations folder doesn't exist yet:
docker compose exec web flask db init
docker compose exec web flask db migrate -m "initial"
docker compose exec web flask db upgrade
```

### GitHub Actions workflow never runs

- Check the runner is **Online**: GitHub repo → Settings → Actions → Runners
- Make sure the push is to the `main` branch (or update the `on.push.branches` in `deploy.yml`)
- Check runner logs: `~/actions-runner/_diag/`

### "Permission denied" running Docker in the workflow

```bash
sudo usermod -aG docker $USER
# Log out and log back in (or run: newgrp docker)
```

### Reset everything (nuclear option)

```bash
docker compose down -v          # removes containers + DB volume
docker system prune -af         # removes all unused images/caches
cp .env.example .env            # reset env
docker compose up -d --build    # fresh start
```
