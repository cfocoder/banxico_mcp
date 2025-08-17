# Example Configuration: Claude Desktop

This configuration works with the official Claude Desktop app.

Update your Claude Desktop config file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Location**: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "banxico": {
      "command": "uvx",
      "args": [
        "run",
        "--from",
        "git+https://github.com/yourusername/banxico-mcp-server",
        "banxico_mcp_server"
      ],
      "env": {
        "BANXICO_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

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