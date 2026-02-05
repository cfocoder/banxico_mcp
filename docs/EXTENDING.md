# Extending Banxico MCP Server

⚠️ **This document is for contributors only.** If you just want to **use** this server, read the [README](../README.md).

---

## Quick Start: Add a New Tool

### 1. Find the Series ID

1. Browse the [Banxico SIE catalog](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries)
2. Find your desired data series ID
3. Test the endpoint: `https://www.banxico.org.mx/SieAPIRest/service/v1/series/{seriesId}/datos/oportuno?token=YOUR_TOKEN`

### 2. Add the Tool

```python
@mcp.tool()
async def get_your_data(limit: Optional[int] = 30) -> str:
    """Brief description of what this tool returns."""
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set."

    endpoint = "series/SF63528/datos"  # Replace with your series ID
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)

    if not data:
        return "Failed to retrieve data."

    # Apply limit if needed
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]

    return format_your_data(data)
```

### 3. Format the Output (Optional)

```python
def format_your_data(data: dict[str, Any]) -> str:
    """Format response for readability."""
    if not data or "bmx" not in data:
        return "No data available"

    result = []
    for series in data["bmx"].get("series", []):
        title = series.get("titulo", "Unknown")
        result.append(f"📊 {title}")

        for dato in series.get("datos", []):
            fecha = dato.get("fecha", "Unknown date")
            valor = dato.get("dato", "N/A")
            result.append(f"   {fecha}: {valor}")

    return "\n".join(result)
```

### 4. Test It

```python
# Quick test in Python REPL
import asyncio
import os

os.environ["BANXICO_API_TOKEN"] = "your_token"
result = await get_your_data(5)
print(result)
```

---

## Banxico API Patterns

### Endpoint Structure

```
Base: https://www.banxico.org.mx/SieAPIRest/service/v1

- Latest data:  /series/{seriesId}/datos/oportuno
- All data:     /series/{seriesId}/datos
- Date range:   /series/{seriesId}/datos/{startDate}/{endDate}
- Metadata:     /series/{seriesId}
```

### Common Series

| Series ID | Data |
|-----------|------|
| SF63528 | USD/MXN exchange rate |
| SF61745 | Funding rate |
| SP30577 | Monthly inflation |
| SP68257 | UDIS values |
| SF282 | CETES 28-day |
| SL1 | Unemployment rate |

---

## Important Notes

### Date Format
Banxico returns dates as `DD/MM/YYYY` (not ISO format).

### Response Structure
All responses follow this structure:
```json
{
  "bmx": {
    "series": [
      {
        "titulo": "Series Title",
        "datos": [
          {"fecha": "DD/MM/YYYY", "dato": "value"}
        ]
      }
    ]
  }
}
```

### Rate Limits
Respect Banxico's rate limits. Check their [API docs](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/ejemplos) for current limits.

### Error Handling
Always check for:
- Missing `BANXICO_TOKEN`
- Network failures
- Invalid series IDs
- Data gaps (some series have `null` values)

---

## Before Submitting a Pull Request

1. ✅ Test with real Banxico data
2. ✅ Follow existing code style (type hints, docstrings)
3. ✅ Add to README tools table if it's a major feature
4. ✅ No API tokens in code or commits

---

## Resources

- [Banxico API Documentation](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/ejemplos)
- [Series Catalog](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries)
- [Existing Tools](../banxico_mcp_server.py) - Use as reference
