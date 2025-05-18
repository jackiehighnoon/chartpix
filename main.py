from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from crud import fetch_historic_price
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:3000"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Add frontend proxy route
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Birdeye API endpoint
BIRDEYE_API_URL = "https://public-api.birdeye.so/defi/history_price"

@app.get("/historic_price")
async def get_historic_price(
    address: str,
    address_type: str = "token",
    time_type: str = "1m",
    time_from: Optional[int] = None,
    time_to: Optional[int] = None
):
    """
    Fetch historical price data from Birdeye API
    
    Args:
        address: Token or pool address
        address_type: Type of address (token or pool)
        time_type: Time interval (1m, 1h, 1d)
        time_from: Start timestamp
        time_to: End timestamp
        
    Returns:
        dict: API response with price data
    """
    try:
        # If timestamps not provided, use last 24 hours
        if not time_from:
            time_from = int((datetime.now() - timedelta(days=1)).timestamp())
        if not time_to:
            time_to = int(datetime.now().timestamp())
        
        # Fetch data from Birdeye API
        response = await fetch_historic_price(
            address=address,
            address_type=address_type,
            time_type=time_type,
            time_from=time_from,
            time_to=time_to
        )
        
        return response
    except Exception as e:
        print(f"Error fetching price data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data")
async def get_price_data(
    address: str,
    address_type: str = "token",
    time_type: str = "1m",
    time_from: Optional[int] = None,
    time_to: Optional[int] = None
):
    """
    Get price data formatted for charting
    
    Args:
        address: Token or pool address
        address_type: Type of address (token or pool)
        time_type: Time interval (1m, 1h, 1d)
        time_from: Start timestamp
        time_to: End timestamp
        
    Returns:
        dict: Chart-ready data
    """
    try:
        # Get the price data
        response = await get_historic_price(
            address=address,
            address_type=address_type,
            time_type=time_type,
            time_from=time_from,
            time_to=time_to
        )
        
        # Prepare the data for charting
        chart_data = []
        for item in response.get('data', {}).get('items', []):
            try:
                # Convert Unix timestamp to milliseconds for Plotly
                timestamp_ms = item['unixTime'] * 1000
                value = item.get('value')
                
                # Include all points, even if value is None
                chart_data.append({
                    "timestamp": timestamp_ms,
                    "value": value  # Keep the original value, even if it's None
                })
            except Exception as e:
                print(f"Warning: Could not parse item unix_time={item.get('unixTime')} value={item.get('value')}: {str(e)}")
                continue
        
        # Sort data by timestamp to ensure correct plotting
        chart_data.sort(key=lambda x: x['timestamp'])
        
        # Extract timestamps and values for Plotly
        timestamps = [point['timestamp'] for point in chart_data]
        values = [point['value'] for point in chart_data]
        
        # Log the data for debugging
        print("Chart data:", {
            "timestamps": timestamps,
            "values": values
        })
        
        return {
            "timestamps": timestamps,
            "values": values
        }
    except Exception as e:
        print(f"Error getting price data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))