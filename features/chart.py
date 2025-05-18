import plotly.graph_objects as go
from datetime import datetime
from typing import List, Dict, Any
from features.schema import PriceData

def create_price_chart(data: List[PriceData], title: str = "Price History") -> Dict[str, Any]:
    """
    Create a price chart using Plotly from the price data
    
    Args:
        data: List of PriceData objects containing the price history
        title: Title for the chart
        
    Returns:
        Dict containing the Plotly figure in JSON format
    """
    # Convert the data to datetime and price lists
    timestamps = [item.unix_time for item in data]
    values = [item.value for item in data]
    
    # Create the figure
    fig = go.Figure()
    
    # Add the price trace
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=values,
        mode='lines',
        name='Price',
        line=dict(
            color='blue',
            width=2
        )
    ))
    
    # Configure layout
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        template='plotly_dark',  # Use dark theme
        hovermode='x unified',  # Show hover data for the same x value
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    
    # Convert to JSON for API response
    return fig.to_dict()

def create_candlestick_chart(data: List[PriceData], title: str = "Price History") -> Dict[str, Any]:
    """
    Create a candlestick chart using Plotly from the price data
    
    Args:
        data: List of PriceData objects containing the price history
        title: Title for the chart
        
    Returns:
        Dict containing the Plotly figure in JSON format
    """
    # Convert the data to datetime and price lists
    timestamps = [datetime.fromtimestamp(item.unix_time) for item in data]
    values = [item.value for item in data]
    
    # Create the figure
    fig = go.Figure()
    
    # Add the candlestick trace
    fig.add_trace(go.Candlestick(
        x=timestamps,
        open=values,
        high=values,
        low=values,
        close=values,
        name='Price',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    
    # Configure layout
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        template='plotly_dark',  # Use dark theme
        hovermode='x unified',  # Show hover data for the same x value
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    
    # Convert to JSON for API response
    return fig.to_dict()