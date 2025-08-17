# Example Configuration: Continue.dev

This configuration works with the Continue VS Code extension.

Update your Continue config file (`~/.continue/config.json`):

```json
{
  "models": [
    {
      "title": "GPT-4",
      "provider": "openai",
      "model": "gpt-4",
      "apiKey": "your_openai_key"
    }
  ],
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

## Restart Continue

After adding the configuration:
1. Reload your VS Code window
2. Restart the Continue extension
3. Test with: "Get me the latest USD/MXN exchange rate"