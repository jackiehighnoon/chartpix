async function fetchChart() {
    const address = document.getElementById('address').value;
    const addressType = document.getElementById('addressType').value;
    const timeType = document.getElementById('timeType').value;
    const title = document.getElementById('title').value;

    if (!address) {
        alert('Please enter an address');
        return;
    }

    try {
        // Show loading state
        document.getElementById('chart').innerHTML = '<div class="loading">Loading chart...</div>';

        // Fetch data from API
        const response = await fetch(`http://localhost:8000/data?address=${encodeURIComponent(address)}&address_type=${addressType}&time_type=${timeType}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Received data:', data);
        
        // Convert timestamps to ISO strings for Plotly
        const timestamps = data.timestamps.map(ts => new Date(ts).toISOString());
        
        // Create chart trace
        const trace = {
            x: timestamps,
            y: data.values,
            type: 'scatter',
            mode: 'lines',
            name: 'Price',
            line: {
                color: 'blue',
                width: 2
            }
        };

        // Create chart layout
        const layout = {
            title: title,
            xaxis: {
                title: 'Time',
                type: 'date',
                tickformat: '%Y-%m-%d %H:%M:%S',
                showgrid: true,
                gridwidth: 1,
                gridcolor: 'rgba(255,255,255,0.1)'
            },
            yaxis: {
                title: 'Price',
                showgrid: true,
                gridwidth: 1,
                gridcolor: 'rgba(255,255,255,0.1)'
            },
            template: 'plotly_dark',
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                yanchor: "top",
                y: 0.99,
                xanchor: "left",
                x: 0.01
            },
            margin: {
                l: 50,
                r: 20,
                b: 50,
                t: 60,
                pad: 4
            }
        };

        console.log('Trace:', trace);
        console.log('Layout:', layout);

        // Ensure the chart container exists
        const chartContainer = document.getElementById('chart');
        if (!chartContainer) {
            throw new Error('Chart container not found');
        }

        // Clear any existing chart
        chartContainer.innerHTML = '';

        // Plot the chart
        Plotly.newPlot('chart', [trace], layout);

        // Add success message
        setTimeout(() => {
            alert('Chart generated successfully!');
        }, 1000);
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Error generating chart. Please check the console for details.');
        document.getElementById('chart').innerHTML = '';
    }
}
