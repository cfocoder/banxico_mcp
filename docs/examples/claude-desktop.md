# Example Configuration: Claude Desktop

This configuration works with the official Claude Desktop app.

## Method 1: Auto-Updates (Recommended)

Update your Claude Desktop config file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Location**: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "banxico": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/cfocoder/banxico_mcp",
        "banxico-mcp-server"
      ],
      "env": {
        "BANXICO_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Benefits:** Automatically gets latest updates when you restart Claude Desktop.

## Method 2: Local File

```json
{
  "mcpServers": {
    "banxico": {
      "command": "uvx",
      "args": [
        "--python", "3.12",
        "--from", "fastmcp",
        "--with", "httpx",
        "--",
        "python",
        "/absolute/path/to/banxico_mcp_server.py"
      ],
      "env": {
        "BANXICO_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Setup Instructions (Method 2 only)

1. **Download the server file**:
   ```bash
   curl -O https://raw.githubusercontent.com/cfocoder/banxico_mcp/main/banxico_mcp_server.py
   ```

2. **Update the config file** with the absolute path to the downloaded file.

## Environment Setup

Set your API token as an environment variable:

```bash
# Linux/macOS
export BANXICO_API_TOKEN="your_actual_token_here"

# Windows
set BANXICO_API_TOKEN=your_actual_token_here
```

## Restart Claude Desktop

After adding the configuration:
1. Completely quit Claude Desktop
2. Restart the application
3. Test with: "Can you check the current USD/MXN exchange rate from Banxico?"