# Example Configuration: VS Code Cline

This configuration works with the Cline extension in VS Code.

Create or update your VS Code settings file (`.vscode/settings.json`):

```json
{
  "mcp.servers": {
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

## Setup Instructions

1. **Download the server file**:
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/banxico-mcp-server/main/banxico_mcp_server.py
   ```

2. **Update the settings file** with the absolute path to the downloaded file.

## Environment Setup

Set your API token as an environment variable:

```bash
# Linux/macOS
export BANXICO_API_TOKEN="your_actual_token_here"

# Windows
set BANXICO_API_TOKEN=your_actual_token_here
```

## Restart Cline

After adding the configuration:
1. Reload your VS Code window
2. Restart the Cline extension
3. Test with: "What's the current USD to MXN exchange rate?"