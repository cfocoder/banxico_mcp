# Environment Variables Template

Copy this file to `.env` and fill in your actual values.

```bash
# Banxico API Token
# Get your token from: https://www.banxico.org.mx/SieAPIRest/service/v1/token
BANXICO_API_TOKEN=your_banxico_api_token_here

# Optional: Set logging level
# Uncomment to enable debug logging
# LOG_LEVEL=DEBUG
```

## Setting Environment Variables

### Linux/macOS

```bash
# Option 1: Export directly
export BANXICO_API_TOKEN="your_actual_token"

# Option 2: Add to your shell profile
echo 'export BANXICO_API_TOKEN="your_actual_token"' >> ~/.bashrc
source ~/.bashrc

# Option 3: Use a .env file with direnv
# Install direnv, then create .envrc:
echo 'source .env' > .envrc
direnv allow
```

### Windows

```cmd
# Option 1: Set for current session
set BANXICO_API_TOKEN=your_actual_token

# Option 2: Set permanently
setx BANXICO_API_TOKEN "your_actual_token"

# Option 3: PowerShell
$env:BANXICO_API_TOKEN="your_actual_token"
```

## Security Notes

- Never commit your `.env` file to version control
- Use different tokens for development and production
- Rotate your tokens regularly
- Consider using a secrets manager for production deployments