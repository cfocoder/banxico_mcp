FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

# Install dependencies
COPY pyproject.toml README.md .
RUN pip install --no-cache-dir -e .

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
