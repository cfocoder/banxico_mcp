#!/usr/bin/env python3
"""
Banxico MCP Server

A Model Context Protocol (MCP) server for accessing the Bank of Mexico (Banxico) 
SIE API to retrieve USD/MXN exchange rate data and other economic indicators.

Author: Your Name
License: MIT
Repository: https://github.com/yourusername/banxico-mcp-server
"""

from typing import Any, Optional
import httpx
import logging
import os
import signal

# MCP and FastMCP imports
try:
    from fastmcp import FastMCP
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastmcp", "httpx"])
    from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("banxico")

# Constants
BANXICO_API_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1"
USER_AGENT = "banxico-mcp/1.0"

# Get API token from environment variable
BANXICO_TOKEN = os.getenv("BANXICO_API_TOKEN")

# Get port from environment
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

# Configure logging to stderr (not stdout for STDIO servers)
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


# Health check endpoint for container orchestration
@mcp.tool()
async def health_check():
    """Health check endpoint for container monitoring.

    Returns:
        dict: Status information
    """
    return {"status": "healthy"}


async def make_banxico_request(endpoint: str, token: str) -> dict[str, Any] | None:
    """
    Make a request to the Banxico SIE API with proper error handling.
    
    Args:
        endpoint: The API endpoint to call (without base URL)
        token: The Banxico API token
        
    Returns:
        JSON response data or None if request failed
    """
    url = f"{BANXICO_API_BASE}/{endpoint}"
    headers = {"User-Agent": USER_AGENT}
    params = {"token": token}
    
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


def format_exchange_rate_data(data: dict[str, Any]) -> str:
    """
    Format exchange rate data into a readable string.
    
    Args:
        data: Raw JSON response from Banxico API
        
    Returns:
        Formatted string with exchange rate information
    """
    if not data or "bmx" not in data:
        return "No data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No series data found"
    
    result = []
    for series in series_list:
        series_title = series.get("titulo", "Unknown Series")
        series_id = series.get("idSerie", "Unknown ID")
        result.append(f"Series: {series_title} (ID: {series_id})")
        
        datos = series.get("datos", [])
        if not datos:
            result.append("  No data points available")
        else:
            result.append(f"  Total data points: {len(datos)}")
            # Show first few and last few data points
            if len(datos) <= 10:
                for dato in datos:
                    fecha = dato.get("fecha", "Unknown date")
                    valor = dato.get("dato", "N/A")
                    result.append(f"  {fecha}: {valor}")
            else:
                # Show first 5
                for i, dato in enumerate(datos[:5]):
                    fecha = dato.get("fecha", "Unknown date")
                    valor = dato.get("dato", "N/A")
                    result.append(f"  {fecha}: {valor}")
                
                result.append(f"  ... ({len(datos) - 10} more data points) ...")
                
                # Show last 5
                for dato in datos[-5:]:
                    fecha = dato.get("fecha", "Unknown date")
                    valor = dato.get("dato", "N/A")
                    result.append(f"  {fecha}: {valor}")
        
        result.append("")  # Empty line between series
    
    return "\n".join(result)


def format_inflation_data(data: dict[str, Any]) -> str:
    """
    Format inflation data with percentage symbols and better labeling.
    
    Args:
        data: Raw JSON response from Banxico API
        
    Returns:
        Formatted string with inflation data including percentage symbols
    """
    if not data or "bmx" not in data:
        return "No inflation data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No inflation series found"
    
    result = []
    for series in series_list:
        title = series.get("titulo", "Unknown Series")
        series_id = series.get("idSerie", "Unknown ID")
        result.append(f"📊 {title} (ID: {series_id})")
        
        datos = series.get("datos", [])
        if not datos:
            result.append("  No data points available")
        else:
            result.append(f"  Total data points: {len(datos)}")
            # Show recent data points with percentage formatting
            display_count = min(len(datos), 10)
            for dato in datos[-display_count:]:
                fecha = dato.get("fecha", "Unknown date")
                valor = dato.get("dato", "N/A")
                # Add percentage symbol for inflation data
                if valor != "N/A" and valor is not None:
                    try:
                        valor_num = float(valor)
                        valor = f"{valor_num}%"
                    except (ValueError, TypeError):
                        pass
                result.append(f"  {fecha}: {valor}")
        
        result.append("")  # Empty line between series
    
    return "\n".join(result)


def format_interest_rate_data(data: dict[str, Any]) -> str:
    """
    Format interest rate data with percentage symbols and rate-specific formatting.
    
    Args:
        data: Raw JSON response from Banxico API
        
    Returns:
        Formatted string with interest rate data
    """
    if not data or "bmx" not in data:
        return "No interest rate data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No interest rate series found"
    
    result = []
    for series in series_list:
        title = series.get("titulo", "Unknown Series")
        series_id = series.get("idSerie", "Unknown ID")
        result.append(f"📈 {title} (ID: {series_id})")
        
        datos = series.get("datos", [])
        if not datos:
            result.append("  No data points available")
        else:
            result.append(f"  Total data points: {len(datos)}")
            # Show recent data points with percentage formatting
            display_count = min(len(datos), 10)
            for dato in datos[-display_count:]:
                fecha = dato.get("fecha", "Unknown date")
                valor = dato.get("dato", "N/A")
                # Add percentage symbol for interest rate data
                if valor != "N/A" and valor is not None:
                    try:
                        valor_num = float(valor)
                        valor = f"{valor_num}%"
                    except (ValueError, TypeError):
                        pass
                result.append(f"  {fecha}: {valor}")
        
        result.append("")  # Empty line between series
    
    return "\n".join(result)


def format_financial_data(data: dict[str, Any]) -> str:
    """
    Format financial data with appropriate units and formatting.
    
    Args:
        data: Raw JSON response from Banxico API
        
    Returns:
        Formatted string with financial data
    """
    if not data or "bmx" not in data:
        return "No financial data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No financial series found"
    
    result = []
    for series in series_list:
        title = series.get("titulo", "Unknown Series")
        series_id = series.get("idSerie", "Unknown ID")
        unit = series.get("unidad", "")
        result.append(f"💰 {title} (ID: {series_id})")
        if unit:
            result.append(f"  Unit: {unit}")
        
        datos = series.get("datos", [])
        if not datos:
            result.append("  No data points available")
        else:
            result.append(f"  Total data points: {len(datos)}")
            # Show recent data points with number formatting
            display_count = min(len(datos), 10)
            for dato in datos[-display_count:]:
                fecha = dato.get("fecha", "Unknown date")
                valor = dato.get("dato", "N/A")
                # Format large numbers with commas
                if valor != "N/A" and valor is not None:
                    try:
                        valor_num = float(valor)
                        if valor_num >= 1000:
                            valor = f"{valor_num:,.2f}"
                        else:
                            valor = f"{valor_num}"
                    except (ValueError, TypeError):
                        pass
                result.append(f"  {fecha}: {valor}")
        
        result.append("")  # Empty line between series
    
    return "\n".join(result)


def format_unemployment_data(data: dict[str, Any]) -> str:
    """
    Format unemployment data with percentage symbols and labor market formatting.
    
    Args:
        data: Raw JSON response from Banxico API
        
    Returns:
        Formatted string with unemployment rate data
    """
    if not data or "bmx" not in data:
        return "No unemployment data available"
    
    series_list = data["bmx"].get("series", [])
    if not series_list:
        return "No unemployment series found"
    
    result = []
    for series in series_list:
        title = series.get("titulo", "Unknown Series")
        series_id = series.get("idSerie", "Unknown ID")
        unit = series.get("unidad", "")
        result.append(f"👥 {title} (ID: {series_id})")
        if unit:
            result.append(f"  Unit: {unit}")
        
        datos = series.get("datos", [])
        if not datos:
            result.append("  No data points available")
        else:
            result.append(f"  Total data points: {len(datos)}")
            # Show recent data points with percentage formatting
            display_count = min(len(datos), 12)  # Show more for unemployment trends
            for dato in datos[-display_count:]:
                fecha = dato.get("fecha", "Unknown date")
                valor = dato.get("dato", "N/A")
                # Add percentage symbol for unemployment rate
                if valor != "N/A" and valor is not None:
                    try:
                        valor_num = float(valor)
                        valor = f"{valor_num}%"
                    except (ValueError, TypeError):
                        pass
                result.append(f"  {fecha}: {valor}")
        
        result.append("")  # Empty line between series
    
    return "\n".join(result)


@mcp.tool()
async def get_latest_usd_mxn_rate() -> str:
    """
    Get the latest USD/MXN exchange rate from Banxico.
        
    Returns:
        The most recent USD/MXN exchange rate with date
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SF63528/datos/oportuno"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve exchange rate data. Please check your API token and network connection."
    
    return format_exchange_rate_data(data)


@mcp.tool()
async def get_usd_mxn_historical_data(limit: Optional[int] = 30) -> str:
    """
    Get historical USD/MXN exchange rate data from Banxico.
    
    Args:
        limit: Maximum number of recent data points to return (default: 30)
        
    Returns:
        Historical USD/MXN exchange rate data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SF63528/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve historical exchange rate data. Please check your API token and network connection."
    
    # If limit is specified, truncate the data
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                # Keep the most recent data points
                series["datos"] = series["datos"][-limit:]
    
    return format_exchange_rate_data(data)


@mcp.tool()
async def get_series_metadata(series_id: str = "SF63528") -> str:
    """
    Get metadata for a Banxico series.
    
    Args:
        series_id: The series ID to get metadata for (default: SF63528 for USD/MXN)
        
    Returns:
        Series metadata including title, description, and date range
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = f"series/{series_id}"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return f"Failed to retrieve metadata for series {series_id}. Please check your API token and network connection."
    
    if "bmx" not in data or "series" not in data["bmx"]:
        return "No series metadata found"
    
    result = []
    for series in data["bmx"]["series"]:
        title = series.get("titulo", "Unknown title")
        series_id = series.get("idSerie", "Unknown ID")
        fecha_inicio = series.get("fechaInicio", "Unknown")
        fecha_fin = series.get("fechaFin", "Unknown")
        periodicidad = series.get("periodicidad", "Unknown")
        cifra = series.get("cifra", "Unknown")
        unidad = series.get("unidad", "Unknown")
        
        result.append(f"Series ID: {series_id}")
        result.append(f"Title: {title}")
        result.append(f"Start Date: {fecha_inicio}")
        result.append(f"End Date: {fecha_fin}")
        result.append(f"Frequency: {periodicidad}")
        result.append(f"Type: {cifra}")
        result.append(f"Unit: {unidad}")
        result.append("")
    
    return "\n".join(result)


@mcp.tool()
async def get_date_range_data(start_date: str, end_date: str, series_id: str = "SF63528") -> str:
    """
    Get exchange rate data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        series_id: The series ID (default: SF63528 for USD/MXN)
        
    Returns:
        Exchange rate data for the specified date range
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = f"series/{series_id}/datos/{start_date}/{end_date}"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return f"Failed to retrieve data for {series_id} from {start_date} to {end_date}. Please check your API token and network connection."
    
    return format_exchange_rate_data(data)


@mcp.tool()
async def get_inflation_data(inflation_type: str = "monthly", limit: Optional[int] = 12) -> str:
    """
    Get inflation data from Banxico.
    
    Args:
        inflation_type: Type of inflation data ('monthly', 'accumulated', 'annual')
        limit: Maximum number of recent data points (default: 12)
        
    Returns:
        Formatted inflation data with percentages
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    # Map inflation types to series IDs
    series_map = {
        "monthly": "SP30577",      # Monthly Inflation
        "accumulated": "SP30579",   # Accumulated Inflation  
        "annual": "SP30578"        # Annual Inflation
    }
    
    if inflation_type not in series_map:
        return f"Invalid inflation type: {inflation_type}. Available types: {list(series_map.keys())}"
    
    series_id = series_map[inflation_type]
    endpoint = f"series/{series_id}/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return f"Failed to retrieve {inflation_type} inflation data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_inflation_data(data)


@mcp.tool()
async def get_udis_data(limit: Optional[int] = 30) -> str:
    """
    Get UDIS (Investment Units) data from Banxico.
    
    Args:
        limit: Maximum number of recent data points (default: 30)
        
    Returns:
        Current and historical UDIS values
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SP68257/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve UDIS data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_exchange_rate_data(data)


@mcp.tool()
async def get_cetes_28_data(limit: Optional[int] = 30) -> str:
    """
    Get CETES 28-day interest rate data from Banxico.
    
    Args:
        limit: Maximum number of recent data points (default: 30)
        
    Returns:
        Current and historical CETES 28-day rates
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SF282/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve CETES 28-day data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_interest_rate_data(data)


@mcp.tool()
async def get_banxico_reserves_data(limit: Optional[int] = 30) -> str:
    """
    Get Banxico Reserve Assets data.
    
    Args:
        limit: Maximum number of recent data points (default: 30)
        
    Returns:
        Current and historical Banxico reserve assets data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SF308843/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve Banxico reserve assets data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_financial_data(data)


@mcp.tool()
async def get_unemployment_data(limit: Optional[int] = 24) -> str:
    """
    Get unemployment rate data from Banxico.
    
    Args:
        limit: Maximum number of recent data points (default: 24 for 2 years of monthly data)
        
    Returns:
        Current and historical unemployment rate data
    """
    if not BANXICO_TOKEN:
        return "Error: BANXICO_API_TOKEN environment variable not set. Please configure your API token."
    
    endpoint = "series/SL1/datos"
    data = await make_banxico_request(endpoint, BANXICO_TOKEN)
    
    if not data:
        return "Failed to retrieve unemployment data. Please check your API token and network connection."
    
    # Apply limit if specified
    if limit and data.get("bmx", {}).get("series"):
        for series in data["bmx"]["series"]:
            if "datos" in series and len(series["datos"]) > limit:
                series["datos"] = series["datos"][-limit:]
    
    return format_unemployment_data(data)


# Graceful shutdown handler
def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received, exiting...")
    exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    # Run with uvicorn for HTTP server
    import uvicorn
    
    host = "0.0.0.0"
    port = MCP_PORT
    
    logger.info(f"Starting Banxico MCP server on {host}:{port}")
    
    # Create and run the Starlette app from FastMCP
    app = mcp.app
    uvicorn.run(app, host=host, port=port, log_level="info")


def main():
    """Entry point for package installation."""
    import uvicorn
    
    host = "0.0.0.0"
    port = MCP_PORT
    
    logger.info(f"Starting Banxico MCP server on {host}:{port}")
    app = mcp.app
    uvicorn.run(app, host=host, port=port, log_level="info")