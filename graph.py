import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def preprocess_gpu_data(file_path):
    # Load the data
    gpu_data = pd.read_csv(file_path)
    
    # Clean the 'eBay Price' column: Replace invalid entries, remove '$', convert to float
    gpu_data['eBay Price'] = gpu_data['eBay Price'].replace(['-', '—'], None)
    gpu_data['eBay Price'] = gpu_data['eBay Price'].replace('[\$,]', '', regex=True).astype(float)
    
    # Ensure 'QTY Sold' is numeric
    gpu_data['QTY Sold'] = pd.to_numeric(gpu_data['QTY Sold'], errors='coerce')
    
    return gpu_data

def filter_by_brand(gpu_data, brand):
    """
    Filter GPU data by a specific brand (e.g., 'GeForce', 'Intel', 'Radeon').
    """
    return gpu_data[gpu_data['GPU'].str.contains(brand, case=False, na=False)]

import matplotlib.colors as mcolors

def assign_colors_geforce(gpu_data):
    """
    Assign color gradients to GPUs based on their series:
        - Warm colors for 20 series
    - Cool colors for 30 series
    - Grayscale for 40 series
    """
    color_map = {}
    series_colors = {
            '16': cm.Greys,
            '20': cm.spring,
            '30': cm.winter,
            '40': cm.autumn
            }

    for series, cmap in series_colors.items():
        series_gpus = sorted([gpu for gpu in gpu_data['GPU'] if (f"RTX {series}" in gpu or f"GTX {series}" in gpu)])
        n = len(series_gpus)
        for i, gpu in enumerate(series_gpus):
            color_map[gpu] = cmap(i / max(n - 1, 1))  # Normalize the index for gradient

    return color_map

def plot_with_colors(gpu_data, color_map):
    """
    Plot GPU data with line colors based on a provided color map.
    """
    plt.style.use('fivethirtyeight')  # Apply a clean grid-based financial style

    gpu_data['Month'] = pd.to_datetime(gpu_data['Month'], format='%B %Y')
    gpu_data = gpu_data.sort_values(by='Month')
    gpu_prices = gpu_data.pivot(index='Month', columns='GPU', values='eBay Price')

    plt.figure(figsize=(12, 6))
    for gpu in gpu_prices.columns:
        color = color_map.get(gpu, 'gray')  # Default to gray if GPU not in the map
        plt.plot(gpu_prices.index, gpu_prices[gpu], label=gpu, color=color)

    plt.title('eBay Prices of GPUs Over Time', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.grid(visible=True, which='major', linestyle='--', linewidth=0.7, color='gray')  # Add horizontal gridlines
    plt.legend(title='GPU', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.show()






def plot(gpu_data):
# Convert the 'Month' column to datetime
    gpu_data['Month'] = pd.to_datetime(gpu_data['Month'], format='%B %Y')

# Sort the data by 'Month'
    gpu_data = gpu_data.sort_values(by='Month')

# Pivot the data for time-series plotting
    gpu_prices = gpu_data.pivot(index='Month', columns='GPU', values='eBay Price')

# Plot the data
    plt.figure(figsize=(12, 6))
    gpu_prices.plot(ax=plt.gca())
    plt.title('eBay Prices of GPUs Over Time')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend(title='GPU', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    file_path = "gpu_time_series.csv"
    cleaned_data = preprocess_gpu_data(file_path)
    geforce_data = filter_by_brand(cleaned_data, 'GeForce')
    color_map = assign_colors_geforce(geforce_data)
    plot_with_colors(geforce_data, color_map)
