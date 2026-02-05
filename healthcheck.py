#!/usr/bin/env python3
"""Health check script for Banxico MCP Server."""

import socket
import os
import sys

def check_health():
    """Check if server is listening on the configured port."""
    port = int(os.getenv("MCP_PORT", "8000"))
    
    try:
        # Try to connect to localhost on the configured port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex(("127.0.0.1", port))
            if result == 0:
                print(f"✓ Server is listening on port {port}")
                return 0
            else:
                print(f"✗ Server is NOT listening on port {port}")
                return 1
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())
