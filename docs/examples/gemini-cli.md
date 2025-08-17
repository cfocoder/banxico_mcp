# Example Configuration: Gemini CLI

This configuration works with the official Gemini CLI tool.

Update your Gemini CLI settings file (`~/.gemini/settings.json`):

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

## Setup Instructions

1. **Download the server file**:
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/banxico-mcp-server/main/banxico_mcp_server.py
   ```

2. **Update your Gemini CLI settings file** (`~/.gemini/settings.json`) with the absolute path to the downloaded file.

## Environment Setup

Set your API token as an environment variable:

```bash
# Linux/macOS
export BANXICO_API_TOKEN="your_actual_token_here"

# Windows
set BANXICO_API_TOKEN=your_actual_token_here
```

## Test the Setup

```bash
# Test that Gemini CLI can connect to the server
gemini --help

# Ask about exchange rates
gemini "What's the current USD to MXN exchange rate?"
```

## Troubleshooting

- Make sure `uvx` is installed: `pip install uv`
- Verify your Banxico API token is valid
- Check that the settings.json file has valid JSON syntax