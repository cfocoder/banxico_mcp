# Complete Guide: Building MCP Servers from APIs

*A comprehensive guide based on the successful Banxico MCP server project*

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: API Research & Planning](#phase-1-api-research--planning)
4. [Phase 2: Server Development](#phase-2-server-development)
5. [Phase 3: Configuration & Testing](#phase-3-configuration--testing)
6. [Phase 4: Documentation](#phase-4-documentation)
7. [Phase 5: Distribution](#phase-5-distribution)
8. [Best Practices](#best-practices)
9. [Common Pitfalls](#common-pitfalls)
10. [Reference Materials](#reference-materials)

## Overview

This guide walks you through creating production-ready MCP (Model Context Protocol) servers from any REST API. We'll use patterns proven successful in the Banxico server, which provides Mexican economic data to AI assistants.

### What You'll Build

- **Professional MCP server** with proper error handling
- **Multiple distribution methods** (auto-updating and manual)
- **Comprehensive documentation** for users and developers
- **Example configurations** for major MCP clients
- **Extension guide** for adding new endpoints

## Prerequisites

### Required Knowledge
- Python 3.10+ programming
- REST API concepts
- JSON data handling
- Git and GitHub basics

### Required Tools
- Python 3.10+
- `uv` or `uvx` package manager
- Git
- Text editor/IDE
- API testing tool (curl, Postman, etc.)

### Required Accounts
- GitHub account
- API provider account (for tokens/keys)

## Phase 1: API Research & Planning

### Step 1.1: API Discovery

**Document everything about the target API:**

```markdown
## API Analysis Template

### Basic Information
- **API Name**: [e.g., Banxico SIE API]
- **Provider**: [e.g., Bank of Mexico]
- **Base URL**: [e.g., https://www.banxico.org.mx/SieAPIRest/service/v1]
- **Authentication**: [Type: API Key, OAuth, etc.]
- **Rate Limits**: [Requests per minute/hour]
- **Documentation**: [Official docs URL]

### Key Endpoints
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| /series/{id}/datos | GET | Get series data | id, token |
| /series/{id}/datos/oportuno | GET | Get latest data | id, token |

### Data Formats
- **Request Format**: Query parameters, JSON body, etc.
- **Response Format**: JSON structure analysis
- **Error Responses**: HTTP codes and error formats
- **Date Formats**: How dates are represented
```

**Example API exploration:**
```bash
# Test basic connectivity
curl "https://api.example.com/v1/status"

# Test authentication
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.example.com/v1/data"

# Analyze response structure
curl "https://api.example.com/v1/series/123" | jq .
```

### Step 1.2: Plan Your Tools

**Identify logical groupings:**

```markdown
## Tool Planning Template

### Core Tools (MVP)
1. **get_latest_data()** - Most recent data point
2. **get_historical_data(limit)** - Historical data with limits
3. **get_metadata(series_id)** - Series information

### Extended Tools
4. **get_date_range_data(start, end)** - Specific date ranges
5. **get_category_data(category)** - Grouped by data type

### Specialized Tools
6. **get_inflation_data(type)** - Domain-specific formatting
7. **get_financial_indicators()** - Multiple series combined
```

### Step 1.3: Project Structure Planning

```
your-mcp-server/
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Development guidelines
├── pyproject.toml              # Package configuration
├── your_mcp_server.py          # Main server file
└── docs/
    ├── EXTENDING.md            # Extension guide
    └── examples/               # Client configurations
        ├── claude-desktop.md
        ├── gemini-cli.md
        ├── continue.md
        ├── vscode-cline.md
        └── env-template.md
```

## Phase 2: Server Development

### Step 2.1: Set Up FastMCP Server

**Create the base server file:**

```python
#!/usr/bin/env python3
"""
[API Name] MCP Server

A Model Context Protocol (MCP) server for accessing [API Provider] 
API to retrieve [data type] and [other features].

Author: Your Name
License: MIT
Repository: https://github.com/yourusername/your-mcp-server
"""

from typing import Any, Optional
import httpx
import logging
import os

# MCP and FastMCP imports with auto-installation
try:
    from fastmcp import FastMCP
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastmcp", "httpx"])
    from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("your-server-name")

# Constants
API_BASE_URL = "https://api.example.com/v1"
USER_AGENT = "your-mcp/1.0"

# Get API credentials from environment
API_TOKEN = os.getenv("YOUR_API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)
```

### Step 2.2: Create HTTP Request Helper

**Generic request function with error handling:**

```python
async def make_api_request(endpoint: str, token: str, params: dict = None) -> dict[str, Any] | None:
    """
    Make a request to the API with proper error handling.
    
    Args:
        endpoint: The API endpoint to call (without base URL)
        token: The API token/key
        params: Additional query parameters
        
    Returns:
        JSON response data or None if request failed
    """
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {token}"  # Adjust auth method as needed
    }
    
    # Merge token into params if required by API
    if params is None:
        params = {}
    params["token"] = token  # If API uses query param authentication
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
```

### Step 2.3: Create Data Formatters

**Specialized formatters for different data types:**

```python
def format_general_data(data: dict[str, Any]) -> str:
    """
    Format general API response data into readable string.
    """
    if not data:
        return "No data available"
    
    # Customize based on your API's response structure
    result = []
    
    # Extract relevant fields from API response
    items = data.get("items", [])  # Adjust to your API structure
    
    for item in items:
        title = item.get("name", "Unknown")
        value = item.get("value", "N/A")
        date = item.get("date", "Unknown date")
        
        result.append(f"{title}: {value} ({date})")
    
    return "\n".join(result)

def format_financial_data(data: dict[str, Any]) -> str:
    """
    Format financial data with proper number formatting.
    """
    # Add percentage symbols, comma separators, currency symbols, etc.
    # Based on your specific data type
    pass

def format_time_series_data(data: dict[str, Any]) -> str:
    """
    Format time series data with date handling.
    """
    # Handle date parsing, sorting, limiting display count
    pass
```

### Step 2.4: Implement MCP Tools

**Core tools with proper documentation:**

```python
@mcp.tool()
async def get_latest_data() -> str:
    """
    Get the most recent data from [API Name].
        
    Returns:
        The most recent data point with relevant details
    """
    if not API_TOKEN:
        return "Error: YOUR_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "data/latest"  # Adjust to your API
    data = await make_api_request(endpoint, API_TOKEN)
    
    if not data:
        return "Failed to retrieve data. Please check your API token and network connection."
    
    return format_general_data(data)

@mcp.tool()
async def get_historical_data(limit: Optional[int] = 30) -> str:
    """
    Get historical data from [API Name].
    
    Args:
        limit: Maximum number of recent data points to return (default: 30)
        
    Returns:
        Historical data with specified limit
    """
    if not API_TOKEN:
        return "Error: YOUR_API_TOKEN environment variable not set."
    
    endpoint = "data/historical"
    params = {"limit": limit} if limit else {}
    data = await make_api_request(endpoint, API_TOKEN, params)
    
    if not data:
        return "Failed to retrieve historical data."
    
    return format_general_data(data)

@mcp.tool()
async def get_metadata(item_id: str = "default") -> str:
    """
    Get metadata for a specific data series or item.
    
    Args:
        item_id: The ID of the item to get metadata for
        
    Returns:
        Metadata including description, units, date range, etc.
    """
    if not API_TOKEN:
        return "Error: YOUR_API_TOKEN environment variable not set."
    
    endpoint = f"metadata/{item_id}"
    data = await make_api_request(endpoint, API_TOKEN)
    
    if not data:
        return f"Failed to retrieve metadata for {item_id}."
    
    return format_metadata(data)
```

### Step 2.5: Add Server Entry Points

```python
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()

def main():
    """Entry point for package installation."""
    mcp.run()
```

## Phase 3: Configuration & Testing

### Step 3.1: Create Package Configuration

**pyproject.toml for distribution:**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-mcp-server"
version = "1.0.0"
description = "MCP server for [API Provider] [data type] API"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.24.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/your-mcp-server"
Repository = "https://github.com/yourusername/your-mcp-server"
Issues = "https://github.com/yourusername/your-mcp-server/issues"

[project.scripts]
your-mcp-server = "your_mcp_server:main"

[tool.hatch.build.targets.wheel]
packages = ["."]
```

### Step 3.2: Test Server Functionality

**Basic testing commands:**

```bash
# Test server startup
YOUR_API_TOKEN=test_token timeout 5s python your_mcp_server.py

# Test with uvx (single file)
YOUR_API_TOKEN=test_token uvx --python 3.12 --from fastmcp --with httpx -- python your_mcp_server.py

# Test package installation
YOUR_API_TOKEN=test_token uvx --from . your-mcp-server

# Test from GitHub
YOUR_API_TOKEN=test_token uvx --from git+https://github.com/yourusername/your-mcp-server your-mcp-server
```

### Step 3.3: Test with MCP Clients

**Example Gemini CLI test:**

```json
{
  "mcpServers": {
    "your-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yourusername/your-mcp-server",
        "your-mcp-server"
      ],
      "env": {
        "YOUR_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Phase 4: Documentation

### Step 4.1: Create Comprehensive README

**README.md structure:**

```markdown
# Your API MCP Server

Brief description of what your server provides.

## Features
- Feature 1
- Feature 2
- MCP Compatible

## Prerequisites
- Python 3.10+
- uvx package manager
- API Token from [Provider]

## Installation Methods

### Option 1: Auto-Updates (Recommended)
[Configuration examples]

### Option 2: Manual File Download
[Download and setup instructions]

## Available Tools
[Table of all tools with parameters]

## Usage Examples
[Natural language examples]

## API Reference
[Endpoint documentation]

## Troubleshooting
[Common issues and solutions]

## Contributing
[Development setup and guidelines]
```

### Step 4.2: Create Client Configuration Examples

**For each major MCP client, create docs/examples/[client].md:**

- `claude-desktop.md`
- `gemini-cli.md`
- `continue.md`
- `vscode-cline.md`

**Template structure:**
```markdown
# Example Configuration: [Client Name]

## Method 1: Auto-Updates (Recommended)
[Configuration with git+https://...]

## Method 2: Local File
[Configuration with local file path]

## Setup Instructions
[Step-by-step setup]

## Testing
[How to verify it works]
```

### Step 4.3: Create Extension Guide

**docs/EXTENDING.md structure:**

```markdown
# Extending the [Your API] MCP Server

## Understanding the [API Provider] API
[API structure explanation]

## Adding a New Tool
### Step 1: Identify the Series/Endpoint
### Step 2: Create the Tool Function
### Step 3: Create Specialized Formatting
### Step 4: Add Multiple Series Support

## Example: Adding [Specific Feature]
[Complete working example]

## Testing New Tools
[Testing methodology]

## Best Practices
[Error handling, documentation, performance]

## Common Pitfalls
[Known issues and solutions]
```

## Phase 5: Distribution

### Step 5.1: GitHub Repository Setup

**Essential files checklist:**
- [ ] README.md (comprehensive)
- [ ] LICENSE (MIT recommended)
- [ ] CONTRIBUTING.md
- [ ] pyproject.toml
- [ ] main_server.py
- [ ] docs/EXTENDING.md
- [ ] docs/examples/ (all client configs)
- [ ] .gitignore (Python template)

### Step 5.2: Version Management

**Semantic versioning strategy:**
- `1.0.0` - Initial release
- `1.1.0` - New tools/features
- `1.0.1` - Bug fixes
- `2.0.0` - Breaking changes

### Step 5.3: Release Process

```bash
# 1. Update version in pyproject.toml
# 2. Test all functionality
# 3. Update CHANGELOG.md
# 4. Commit and tag

git add .
git commit -m "Release v1.1.0: Add unemployment data tool"
git tag v1.1.0
git push origin main --tags
```

## Best Practices

### Code Quality
- **Type hints** on all functions
- **Docstrings** with examples
- **Error handling** for all API calls
- **Logging** for debugging
- **Environment variables** for secrets

### User Experience
- **Clear error messages** with actionable advice
- **Consistent formatting** across all tools
- **Reasonable defaults** for parameters
- **Auto-installation** of dependencies
- **Multiple installation methods**

### Documentation
- **Examples before technical details**
- **Copy-paste ready** configurations
- **Troubleshooting sections**
- **Extension guides** for developers
- **Visual indicators** (emojis, formatting)

### Security
- **Never hardcode** API keys or tokens
- **Environment variable** authentication
- **Clear instructions** for token management
- **Example templates** without real credentials

## Common Pitfalls

### API Integration Issues
1. **Rate limiting** - Implement proper delays and retries
2. **Authentication** - Test token expiration scenarios
3. **Data formatting** - Handle null/missing values gracefully
4. **Date handling** - Parse API date formats correctly

### MCP Server Issues
1. **STDIO communication** - Don't print to stdout except for MCP messages
2. **Error propagation** - Return user-friendly error strings
3. **Tool naming** - Use descriptive, consistent function names
4. **Parameter validation** - Handle invalid inputs gracefully

### Distribution Issues
1. **Dependency management** - Pin version ranges, not exact versions
2. **Python compatibility** - Test with multiple Python versions
3. **Documentation sync** - Keep examples updated with code changes
4. **Breaking changes** - Version appropriately and document migrations

## Reference Materials

### Essential Documentation
- **[Model Context Protocol Specification](https://modelcontextprotocol.io/)**
- **[FastMCP Documentation](https://gofastmcp.com/)**
- **[uvx Documentation](https://docs.astral.sh/uv/)**
- **[MCP Servers Collection](https://github.com/modelcontextprotocol/servers)**

### API Best Practices
- **[RESTful API Design](https://restfulapi.net/)**
- **[HTTP Status Codes](https://httpstatuses.com/)**
- **[JSON API Specification](https://jsonapi.org/)**

### Python Development
- **[Python Type Hints](https://docs.python.org/3/library/typing.html)**
- **[asyncio Documentation](https://docs.python.org/3/library/asyncio.html)**
- **[httpx Documentation](https://www.python-httpx.org/)**

### MCP Client Documentation
- **[Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)**
- **[Gemini CLI Documentation](https://github.com/google-gemini/gemini-cli)**
- **[Continue.dev MCP Setup](https://docs.continue.dev/)**

### Successful MCP Server Examples
- **[Banxico MCP Server](https://github.com/cfocoder/banxico_mcp)** - Economic data (this project)
- **[MCP Servers Repository](https://github.com/modelcontextprotocol/servers)** - Official examples
- **[Weather MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/weather)** - Weather API example

## Conclusion

Building a successful MCP server requires careful planning, solid development practices, and comprehensive documentation. The patterns established in this guide have been proven successful with the Banxico MCP server, which provides Mexican economic data to AI assistants.

Key success factors:
1. **Thorough API research** before coding
2. **User-focused design** with clear error messages
3. **Multiple distribution methods** for different user preferences
4. **Comprehensive documentation** with working examples
5. **Extensible architecture** for future enhancements

Follow this guide, adapt the patterns to your specific API, and you'll create a professional MCP server that users will love to use and developers will love to extend.

---

*This guide is based on the successful development of the Banxico MCP Server. For questions or improvements, please open an issue in the [Banxico MCP repository](https://github.com/cfocoder/banxico_mcp).*