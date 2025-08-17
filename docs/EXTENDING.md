# Extending the Banxico MCP Server

This guide explains how to add new API endpoints and tools to the Banxico MCP server.

## Understanding the Banxico SIE API

The Banxico SIE (Sistema de Información Económica) API provides access to various economic data series. Each series has a unique ID and follows a consistent pattern:

### API Endpoint Structure

```
Base URL: https://www.banxico.org.mx/SieAPIRest/service/v1

Patterns:
- Series metadata: /series/{seriesId}
- Latest data: /series/{seriesId}/datos/oportuno  
- All data: /series/{seriesId}/datos
- Date range: /series/{seriesId}/datos/{startDate}/{endDate}
```

### Common Series IDs

| Series ID | Description |
|-----------|-------------|
| SF63528 | USD/MXN daily exchange rate (since 1954) |
| SF61745 | Funding rate (average weighted) |
| SF60634 | Target rate |
| SF43773 | Core inflation (annual) |
| SP74665 | 91-day CETES yield rate |

## Adding a New Tool

### Step 1: Identify the Series

1. Browse the [Banxico catalog](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries)
2. Find the series ID for your desired data
3. Test the API endpoint manually

### Step 2: Create the Tool Function

Add a new tool using the `@mcp.tool()` decorator:

```python
@mcp.tool()
async def get_inflation_data(limit: Optional[int] = 30) -> str:
    """
    Get inflation data from Banxico.
    
    Args:
        limit: Maximum number of recent data points (default: 30)
        
    Returns:
        Formatted inflation data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    # SF43773 is the series ID for core inflation
    endpoint = "series/SF43773/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve inflation data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_exchange_rate_data(data)
```

### Step 3: Create Specialized Formatting (Optional)

For data that needs special formatting, create a custom formatter:

```python
def format_inflation_data(data: dict[str, Any]) -> str:
    """
    Format inflation data with percentage symbols and better labeling.
    """
    if not data or "bmx" not in data:
        return "No inflation data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No inflation series found"
    
    result = []
    for series in series_list:
        title = series.get("titulo", "Unknown Series")
        result.append(f"📊 {title}")
        
        datos = series.get("datos", [])
        for dato in datos:
            fecha = dato.get("fecha", "Unknown date")
            valor = dato.get("dato", "N/A")
            # Add percentage symbol for inflation data
            if valor != "N/A":
                valor = f"{valor}%"
            result.append(f"   {fecha}: {valor}")
    
    return "\n".join(result)
```

### Step 4: Add Multiple Series Support

For tools that work with multiple series:

```python
@mcp.tool()
async def get_interest_rates(rate_type: str = "all") -> str:
    """
    Get various interest rates from Banxico.
    
    Args:
        rate_type: Type of rate ('funding', 'target', 'cetes', 'all')
        
    Returns:
        Formatted interest rate data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set."
    
    # Define series IDs for different rate types
    series_map = {
        "funding": "SF61745",
        "target": "SF60634", 
        "cetes": "SP74665"
    }
    
    if rate_type == "all":
        series_ids = ",".join(series_map.values())
    elif rate_type in series_map:
        series_ids = series_map[rate_type]
    else:
        return f"Unknown rate type: {rate_type}. Available types: {list(series_map.keys())} or 'all'"
    
    endpoint = f"series/{series_ids}/datos/oportuno"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve interest rate data."
    
    return format_exchange_rate_data(data)
```

## Example: Adding GDP Data

Here's a complete example of adding GDP data:

```python
@mcp.tool()
async def get_gdp_data(frequency: str = "quarterly", limit: Optional[int] = 8) -> str:
    """
    Get GDP data from Banxico.
    
    Args:
        frequency: Data frequency ('quarterly' or 'annual')
        limit: Maximum number of data points (default: 8)
        
    Returns:
        Formatted GDP data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set."
    
    # Example series IDs (you'll need to find the actual ones)
    series_map = {
        "quarterly": "SR16676",  # Example ID
        "annual": "SR16677"      # Example ID
    }
    
    if frequency not in series_map:
        return f"Invalid frequency: {frequency}. Use 'quarterly' or 'annual'"
    
    series_id = series_map[frequency]
    endpoint = f"series/{series_id}/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return f"Failed to retrieve {frequency} GDP data."
    
    # Apply limit
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_gdp_data(data)

def format_gdp_data(data: dict[str, Any]) -> str:
    """Format GDP data with proper units and growth rates."""
    if not data or "bmx" not in data:
        return "No GDP data available"
    
    series_list = data["bmx"].get("series", [])
    result = []
    
    for series in series_list:
        title = series.get("titulo", "Unknown GDP Series")
        unit = series.get("unidad", "")
        result.append(f"💰 {title}")
        if unit:
            result.append(f"   Unit: {unit}")
        
        datos = series.get("datos", [])
        for dato in datos:
            fecha = dato.get("fecha", "Unknown")
            valor = dato.get("dato", "N/A")
            result.append(f"   {fecha}: {valor}")
    
    return "\n".join(result)
```

## Testing New Tools

### Manual Testing

Create a test script for your new tool:

```python
import asyncio
import os
from banxico_mcp_server import get_inflation_data

async def test_new_tool():
    os.environ["BANXICO_API_TOKEN"] = "your_test_token"
    result = await get_inflation_data(5)
    print(result)

if __name__ == "__main__":
    asyncio.run(test_new_tool())
```

### Integration Testing

Test with your MCP client:

1. Add the new tool to your server
2. Restart your MCP client
3. Ask questions that would use the new tool

## Best Practices

### Error Handling

Always include proper error handling:

```python
@mcp.tool()
async def your_new_tool() -> str:
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set."
    
    try:
        # Your API call here
        data = await make_banxico_request(endpoint, BANXICO_TOKEN)
        if not data:
            return "Failed to retrieve data. Check your token and connection."
        
        return format_your_data(data)
    except Exception as e:
        logger.error(f"Error in your_new_tool: {e}")
        return f"An error occurred: {str(e)}"
```

### Documentation

Document your tools clearly:

```python
@mcp.tool()
async def your_tool(param1: str, param2: Optional[int] = 10) -> str:
    """
    Brief description of what the tool does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 with default value
        
    Returns:
        Description of what is returned
        
    Examples:
        - "Get the inflation rate for Mexico"
        - "Show me the latest GDP data"
    """
```

### Performance

- Use appropriate data limits to avoid large responses
- Consider caching for frequently requested data
- Log API calls for debugging

### Formatting

- Use consistent formatting across all tools
- Include units and context in the output
- Use emojis sparingly for visual appeal
- Handle missing data gracefully

## Common Pitfalls

1. **Wrong Series ID**: Double-check series IDs in the Banxico catalog
2. **Date Format**: Banxico uses DD/MM/YYYY format in responses
3. **Missing Data**: Some series have gaps - handle `null` values
4. **Rate Limits**: Respect API rate limits (documented in Banxico API docs)
5. **Token Expiry**: API tokens may expire - provide clear error messages

## Contributing Back

When you add useful tools:

1. Test thoroughly with real data
2. Add proper documentation
3. Follow the existing code style
4. Consider submitting a pull request to share with others

## Getting Help

- Check the [Banxico API documentation](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/ejemplos)
- Browse the [series catalog](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries)
- Look at existing tools in the server for patterns
- Test API endpoints manually before implementing