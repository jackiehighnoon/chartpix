from fastapi import HTTPException
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

BIRDEYE_API_URL = "https://public-api.birdeye.so/defi/history_price"

async def fetch_historic_price(
    address: str,
    address_type: str = "token",
    time_type: str = "1m",
    time_from: int = None,
    time_to: int = None
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
        # Construct API URL with parameters
        params = {
            "address": address,
            "address_type": address_type,
            "type": time_type,
            "time_from": time_from,
            "time_to": time_to
        }
        
        # Add required headers
        headers = {
            'X-API-KEY': os.getenv('BIRDEYE_API_KEY'),
            'accept': 'application/json',
            'x-chain': 'solana'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(BIRDEYE_API_URL, params=params, headers=headers)
            response.raise_for_status()
            
            # Log the full API response
            print("API Response:", response.json())
            
            # Return the raw API response
            return response.json()
            
    except httpx.HTTPError as e:
        print(f"Error fetching data from Birdeye API: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None