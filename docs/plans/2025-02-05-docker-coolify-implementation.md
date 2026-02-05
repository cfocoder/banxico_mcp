# Docker Coolify Deployment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create production-ready Docker deployment configuration with health checks, graceful shutdown, and configurable ports for Coolify deployment on Oracle Cloud.

**Architecture:** Multi-stage Dockerfile with non-root user, health checks, and configurable HTTP port; docker-compose.yml for local testing; cleaned-up documentation; updated README with deployment instructions.

**Tech Stack:** Python 3.12, FastMCP, Docker, docker-compose, httpx

---

## Task 1: Create Dockerfile

**Files:**
- Create: `Dockerfile`

**Step 1: Create Dockerfile**

Create `/home/hectorsa/Dropbox/DELL_VOSTRO_DOCUMENTS/MCP_SERVERS/banxico_mcp/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir gunicorn

# Copy application
COPY --chown=mcp:mcp banxico_mcp_server.py .

USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:${MCP_PORT:-8000}/health', timeout=5)" || exit 1

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_PORT=8000

# Expose port
EXPOSE ${MCP_PORT}

# Run server
CMD ["python", "banxico_mcp_server.py"]
```

**Step 2: Verify Dockerfile syntax**

Run: `docker build --help | head -5`

Expected: Docker CLI works

**Step 3: Commit**

```bash
git add Dockerfile
git commit -m "feat: add Dockerfile for production deployment"
```

---

## Task 2: Create docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

**Step 1: Create docker-compose.yml**

Create `/home/hectorsa/Dropbox/DELL_VOSTRO_DOCUMENTS/MCP_SERVERS/banxico_mcp/docker-compose.yml`:

```yaml
version: '3.8'

services:
  banxico-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: banxico-mcp-server
    ports:
      - "${MCP_PORT:-8000}:${MCP_PORT:-8000}"
    environment:
      - BANXICO_API_TOKEN=${BANXICO_API_TOKEN}
      - MCP_PORT=${MCP_PORT:-8000}
      - PYTHONUNBUFFERED=1
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:${MCP_PORT:-8000}/health', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    networks:
      - banxico-network

networks:
  banxico-network:
    driver: bridge
```

**Step 2: Verify file is valid YAML**

Run: `python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))" && echo "Valid YAML"`

Expected: "Valid YAML" printed

**Step 3: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: add docker-compose for local testing"
```

---

## Task 3: Create .dockerignore

**Files:**
- Create: `.dockerignore`

**Step 1: Create .dockerignore**

Create `/home/hectorsa/Dropbox/DELL_VOSTRO_DOCUMENTS/MCP_SERVERS/banxico_mcp/.dockerignore`:

```
.git
.gitignore
.github
.claude
.venv
venv
__pycache__
*.pyc
*.pyo
*.egg-info
dist
build
.pytest_cache
.coverage
.DS_Store
*.md
!README.md
docs/examples
.env
.env.local
```

**Step 2: Verify file exists**

Run: `test -f .dockerignore && echo "File exists"`

Expected: "File exists"

**Step 3: Commit**

```bash
git add .dockerignore
git commit -m "feat: add .dockerignore for optimized builds"
```

---

## Task 4: Create .env.example

**Files:**
- Create: `.env.example`

**Step 1: Create .env.example**

Create `/home/hectorsa/Dropbox/DELL_VOSTRO_DOCUMENTS/MCP_SERVERS/banxico_mcp/.env.example`:

```
BANXICO_API_TOKEN=your_token_here
MCP_PORT=8000
```

**Step 2: Verify file exists**

Run: `test -f .env.example && echo "File exists"`

Expected: "File exists"

**Step 3: Commit**

```bash
git add .env.example
git commit -m "feat: add .env.example template for local development"
```

---

## Task 5: Delete docs/examples directory

**Files:**
- Delete: `docs/examples/` (entire directory)

**Step 1: Verify docs/examples exists**

Run: `ls -la docs/examples/`

Expected: Lists files like claude-desktop.md, continue.md, etc.

**Step 2: Delete directory**

Run: `rm -rf docs/examples/`

**Step 3: Verify deletion**

Run: `test ! -d docs/examples && echo "Directory deleted"`

Expected: "Directory deleted"

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: remove docs/examples (not relevant for server deployment)"
```

---

## Task 6: Update banxico_mcp_server.py - Add imports and health endpoint

**Files:**
- Modify: `banxico_mcp_server.py` (after line 40, before first tool definition)

**Step 1: Read current file structure**

Run: `head -50 banxico_mcp_server.py`

Expected: See imports and logger setup

**Step 2: Add signal import after existing imports**

After line 16 (`import os`), add:

```python
import signal
```

**Step 3: Add health endpoint tool after logger setup**

After line 40 (after logger definition), add:

```python
# Health check endpoint for container orchestration
@mcp.tool()
async def health_check():
    """Health check endpoint for container monitoring.

    Returns:
        dict: Status information
    """
    return {"status": "healthy"}
```

**Step 4: Add environment variable for port after BANXICO_TOKEN line**

After line 36 (`BANXICO_TOKEN = os.getenv("BANXICO_API_TOKEN")`), add:

```python
# Get port from environment
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
```

**Step 5: Add graceful shutdown handler before main() function**

Before the `if __name__ == "__main__":` line, add:

```python
# Graceful shutdown handler
def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received, exiting...")
    exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

**Step 6: Verify syntax**

Run: `python3 -m py_compile banxico_mcp_server.py && echo "Syntax OK"`

Expected: "Syntax OK"

**Step 7: Commit**

```bash
git add banxico_mcp_server.py
git commit -m "feat: add health endpoint, port configuration, and graceful shutdown"
```

---

## Task 7: Update README.md - Add Docker/Coolify section

**Files:**
- Modify: `README.md` (after Installation Methods section, around line 96)

**Step 1: Find insertion point**

Run: `grep -n "## Configuration" README.md`

Expected: Shows line number of Configuration section

**Step 2: Add Docker/Coolify section before Configuration section**

Insert this section between "## Installation Methods" and "## Configuration":

```markdown
## Deployment with Docker/Coolify

### Quick Start with Docker Compose (Local Testing)

1. **Clone and setup:**
   ```bash
   git clone https://github.com/cfocoder/banxico_mcp.git
   cd banxico_mcp
   cp .env.example .env
   # Edit .env with your BANXICO_API_TOKEN and desired MCP_PORT
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up
   ```

3. **Test the server:**
   ```bash
   curl http://localhost:8000/health
   ```

### Deployment in Coolify (Oracle Cloud)

1. **Push to GitHub** - Coolify will pull from your repository
2. **Create new Docker service in Coolify** - Select "Docker" type
3. **Configure environment variables:**
   - `BANXICO_API_TOKEN`: Your Banxico API token
   - `MCP_PORT`: Port number (default: 8000, change to avoid conflicts)
4. **Expose port** - Configure port mapping in Coolify dashboard
5. **Health checks** - Coolify will automatically use the `/health` endpoint

The Docker image will build automatically with production-ready features including health checks, non-root user, and graceful shutdown handling.

```

**Step 3: Verify syntax**

Run: `python3 -c "import markdown; markdown.markdown(open('README.md').read())" && echo "Valid markdown"`

Expected: "Valid markdown"

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add Docker and Coolify deployment section to README"
```

---

## Task 8: Build and test Docker image locally

**Files:**
- No new files (testing existing setup)

**Step 1: Create local .env for testing**

Run:
```bash
cp .env.example .env
echo "BANXICO_API_TOKEN=test_token_12345" > .env
echo "MCP_PORT=8000" >> .env
```

**Step 2: Build Docker image**

Run: `docker build -t banxico-mcp:latest .`

Expected: Build succeeds with "Successfully tagged banxico-mcp:latest"

**Step 3: Verify image exists**

Run: `docker images | grep banxico-mcp`

Expected: Shows image with tag "latest"

**Step 4: Test with docker-compose (dry run)**

Run: `docker-compose config`

Expected: Shows valid composed configuration without errors

**Step 5: No commit needed**

This is testing only; all code already committed.

---

## Task 9: Final verification and summary

**Files:**
- Review all changes

**Step 1: Verify all new files exist**

Run:
```bash
test -f Dockerfile && \
test -f docker-compose.yml && \
test -f .dockerignore && \
test -f .env.example && \
echo "All files created"
```

Expected: "All files created"

**Step 2: Verify docs/examples deleted**

Run: `test ! -d docs/examples && echo "docs/examples deleted"`

Expected: "docs/examples deleted"

**Step 3: View git log of changes**

Run: `git log --oneline -10`

Expected: Shows 8 commits starting with "feat: add Dockerfile..." and ending with "docs: add Docker..."

**Step 4: Final status**

Run: `git status`

Expected: "On branch main" and "nothing to commit, working tree clean"

---

## Checklist

- [x] Dockerfile created with Python 3.12, non-root user, health checks
- [x] docker-compose.yml created for local testing
- [x] .dockerignore created for optimized builds
- [x] .env.example created as template
- [x] docs/examples directory deleted
- [x] banxico_mcp_server.py updated with health endpoint, port config, graceful shutdown
- [x] README.md updated with Docker/Coolify deployment section
- [x] Docker image builds successfully
- [x] All changes committed to git

---

## Testing the Implementation

After completing all tasks, test locally:

```bash
# Copy template
cp .env.example .env

# Edit .env if needed (default settings are fine for local testing)

# Build and run
docker-compose up

# In another terminal, test health check
curl http://localhost:8000/health

# Should return: {"status": "healthy"}

# Stop with Ctrl+C, which sends SIGTERM for graceful shutdown
```

## Deployment Notes for Coolify

Once deployed to Coolify on Oracle Cloud:

1. Set `BANXICO_API_TOKEN` in Coolify environment variables
2. Set `MCP_PORT` to desired port (e.g., 8001 to avoid conflicts)
3. Coolify will automatically:
   - Pull latest code from GitHub
   - Build Docker image
   - Run health checks every 30 seconds
   - Restart on failure (unless-stopped)
   - Handle graceful shutdown
