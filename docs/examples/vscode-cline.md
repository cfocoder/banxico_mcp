# Example Configuration: VS Code Cline

This configuration works with the Cline extension in VS Code.

Create or update your VS Code settings file (`.vscode/settings.json`):

```json
{
  "mcp.servers": {
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

## Restart Cline

After adding the configuration:
1. Reload your VS Code window
2. Restart the Cline extension
3. Test with: "What's the current USD to MXN exchange rate?"