# Banxico MCP Server

A Model Context Protocol (MCP) server for accessing the Bank of Mexico (Banxico) SIE API to retrieve USD/MXN exchange rate data and other economic indicators.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Real-time Exchange Rates**: Get the latest USD/MXN exchange rate from Banxico
- **Historical Data**: Retrieve historical exchange rate data with customizable limits
- **Series Metadata**: Access detailed information about economic data series
- **Date Range Queries**: Get exchange rate data for specific date ranges
- **MCP Compatible**: Works with Claude Desktop, Gemini CLI, and other MCP clients

## Prerequisites

1. **Python 3.10+** installed on your system
2. **uvx** (recommended) or **uv** package manager
3. **Banxico API Token** - Get one from [Banxico SIE API](https://www.banxico.org.mx/SieAPIRest/service/v1/token)

## Installation Methods

### Option 1: Using uvx (Recommended)

The easiest way to run this server is using `uvx`, which automatically handles dependencies:

1. **Install uvx** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Download the server file**:
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/banxico-mcp-server/main/banxico_mcp_server.py
   ```

3. **Test the server**:
   ```bash
   BANXICO_API_TOKEN=your_token_here uvx --python 3.12 --from fastmcp --with httpx -- python banxico_mcp_server.py
   ```

### Option 2: Traditional Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/banxico-mcp-server.git
   cd banxico-mcp-server
   ```

2. **Install dependencies**:
   ```bash
   pip install fastmcp httpx
   ```

3. **Run the server**:
   ```bash
   BANXICO_API_TOKEN=your_token_here python banxico_mcp_server.py
   ```

## Configuration

### Get Your Banxico API Token

1. Visit [Banxico Token Registration](https://www.banxico.org.mx/SieAPIRest/service/v1/token)
2. Fill out the form to request an API token
3. You'll receive your token via email

### Configure MCP Clients

#### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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
        "BANXICO_API_TOKEN": "your_banxico_token_here"
      }
    }
  }
}
```

#### Gemini CLI

Add to `~/.gemini/settings.json`:

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
        "BANXICO_API_TOKEN": "your_banxico_token_here"
      }
    }
  }
}
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_latest_usd_mxn_rate()` | Get the most recent USD/MXN exchange rate | None |
| `get_usd_mxn_historical_data(limit)` | Get historical exchange rate data | `limit`: Max data points (default: 30) |
| `get_series_metadata(series_id)` | Get metadata for a data series | `series_id`: Series ID (default: SF63528) |
| `get_date_range_data(start_date, end_date, series_id)` | Get data for specific date range | `start_date`, `end_date`: YYYY-MM-DD format |

## Usage Examples

Once configured with your MCP client, you can ask:

- "What's the current USD to MXN exchange rate?"
- "Show me the USD/MXN exchange rate for the last 10 days"
- "Get the exchange rate data from 2024-01-01 to 2024-01-31"
- "What's the metadata for the USD/MXN series?"

## API Reference

The server uses the [Banxico SIE API](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/ejemplos) with the following endpoints:

- **Latest Data**: `/series/SF63528/datos/oportuno`
- **Historical Data**: `/series/SF63528/datos`
- **Series Metadata**: `/series/SF63528`
- **Date Range**: `/series/SF63528/datos/{start_date}/{end_date}`

## Development

### Project Structure

```
banxico-mcp-server/
├── banxico_mcp_server.py    # Main server file
├── README.md                # This file
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Development guidelines
└── docs/                    # Documentation and examples
    ├── EXTENDING.md         # Guide for adding new endpoints
    └── examples/            # Configuration examples
        ├── claude-desktop.md
        ├── continue.md
        ├── env-template.md
        ├── gemini-cli.md
        └── vscode-cline.md
```

### Testing

To test the server without an MCP client:

```bash
# Set your token
export BANXICO_API_TOKEN=your_token_here

# Run the server with a timeout to test startup
timeout 5s python banxico_mcp_server.py && echo "Server starts successfully"
```

### Adding New Tools

See [EXTENDING.md](docs/EXTENDING.md) for detailed instructions on adding new Banxico API endpoints.

## Troubleshooting

### Common Issues

1. **"BANXICO_API_TOKEN environment variable not set"**
   - Ensure your API token is properly configured in the MCP client settings

2. **"Failed to retrieve data"**
   - Check your internet connection
   - Verify your API token is valid
   - Ensure the Banxico API is accessible

3. **Server doesn't start**
   - Verify Python 3.10+ is installed
   - Check that uvx or required dependencies are available

### Debug Mode

Run with debug logging:

```bash
BANXICO_API_TOKEN=your_token PYTHONPATH=. python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from banxico_mcp_server import mcp
mcp.run()
"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Bank of Mexico (Banxico)](https://www.banxico.org.mx/) for providing the SIE API
- [Model Context Protocol](https://modelcontextprotocol.io/) for the protocol specification
- [FastMCP](https://github.com/jlowin/fastmcp) for the excellent MCP server framework

## Related Projects

- [MCP Servers Collection](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)
- [Gemini CLI Documentation](https://github.com/google-gemini/gemini-cli)
