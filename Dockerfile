FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

# Install dependencies
COPY pyproject.toml README.md .
RUN pip install --no-cache-dir -e .

# Copy application and healthcheck script
COPY --chown=mcp:mcp banxico_mcp_server.py .
COPY --chown=mcp:mcp healthcheck.py .

USER mcp

# Health check - verify server is listening on configured port
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python healthcheck.py

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_PORT=8000

# Expose port (default, will be overridden by env var at runtime)
EXPOSE 8000

# Run server with HTTP transport
CMD ["python", "banxico_mcp_server.py"]
