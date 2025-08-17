# Banxico MCP Server

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/banxico-mcp-server.git`
3. Get a Banxico API token from https://www.banxico.org.mx/SieAPIRest/service/v1/token
4. Set your token: `export BANXICO_API_TOKEN="your_token"`
5. Test the server: `uvx run banxico_mcp_server`

## Adding New Features

See `docs/EXTENDING.md` for detailed instructions on adding new API endpoints.

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to all public functions
- Include error handling for API calls

## Testing

Before submitting a PR:
1. Test all existing functionality still works
2. Test your new features with real API calls
3. Update documentation as needed
4. Ensure no API tokens are committed

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push and create a Pull Request

Thank you for contributing!