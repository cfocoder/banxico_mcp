# Docker Coolify Deployment Design

**Date:** 2025-02-05
**Project:** Banxico MCP Server
**Author:** Claude Code
**Status:** Approved

## Overview

Design for production-ready Docker deployment of the Banxico MCP Server on Oracle Cloud via Coolify.

## Architecture & Components

**Production-Ready Stack:**
- Python 3.12 slim base image
- Non-root user (mcp:1000) for security
- Health checks (HTTP /health endpoint)
- Graceful SIGTERM shutdown handling
- Configurable port via `MCP_PORT` environment variable
- Dual-mode: STDIO (for MCP clients) + HTTP (for Coolify)

**Files to Create:**
1. `Dockerfile` - Multi-stage, optimized, production-ready
2. `docker-compose.yml` - Local testing with env vars
3. `.dockerignore` - Optimize build context
4. `.env.example` - Template for local development

**Files to Modify:**
- `banxico_mcp_server.py` - Add health endpoint, port configuration, graceful shutdown
- `README.md` - Add Docker/Coolify deployment section

**Files to Delete:**
- `docs/examples/` - All IDE configuration examples (not relevant for server deployment)

## Dockerfile Specification

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

**Key Features:**
- Slim base for smaller image size
- Non-root user for security
- Health check every 30s with 5s startup period
- Environment variables for flexibility
- Dynamic port exposure

## docker-compose.yml Specification

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

**Key Features:**
- Reads from `.env` for local development
- Configurable port (default 8000)
- Restart policy for resilience
- Health check redundancy
- Dedicated network for future expansion

## .dockerignore Specification

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

Excludes unnecessary files to reduce image size and build context.

## Code Changes to banxico_mcp_server.py

**New additions:**

1. **Health check endpoint:**
```python
@mcp.tool()
async def health_check():
    """Health check endpoint for container orchestration"""
    return {"status": "healthy"}
```

2. **Environment variables:**
```python
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
BANXICO_API_TOKEN = os.getenv("BANXICO_API_TOKEN")
```

3. **Graceful shutdown:**
```python
import signal

def signal_handler(sig, frame):
    logger.info("Shutdown signal received")
    exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

## README Updates

Add new section "Deployment with Docker/Coolify" after "Installation Methods" with:
- Local testing with docker-compose quick start
- Step-by-step Coolify deployment guide
- Environment variable configuration
- Health check verification

## Cleanup Plan

**Documentation:**
- Delete `docs/examples/` folder entirely (claude-desktop.md, continue.md, gemini-cli.md, vscode-cline.md, env-template.md)
- Keep `docs/EXTENDING.md` and `docs/MCP_SERVER_DEVELOPMENT_GUIDE.md`

**Repository:**
- Clean commit history (squash or rebase if desired)

## Local Development Workflow

1. `cp .env.example .env`
2. Edit `.env` with `BANXICO_API_TOKEN` and desired `MCP_PORT`
3. `docker-compose up`
4. Test: `curl http://localhost:8000/health`

## Coolify Deployment Workflow

1. Push to GitHub
2. Create new Docker service in Coolify
3. Set environment variables (BANXICO_API_TOKEN, MCP_PORT)
4. Configure port mapping
5. Health checks automatic via `/health` endpoint

## Success Criteria

- ✅ Docker image builds successfully
- ✅ Health check endpoint responds 200 OK
- ✅ Server runs on configurable port
- ✅ docker-compose works locally
- ✅ Graceful shutdown on SIGTERM
- ✅ Non-root user executing container
- ✅ Documentation updated
- ✅ Unused docs deleted
