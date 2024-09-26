import requests
import time
import plotext as plt
from datetime import datetime
import sys

# Store previous differences to predict direction
previous_diffs_oi = []
previous_diffs_vol = []

# Maximum length for historical data
max_history = 6  # Equivalent to 1-hour data (assuming 10-min intervals)

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Function to fetch data from the API
def fetch_data():
    url = "https://api.delta.exchange/v2/tickers"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data. Status code: {response.status_code}", flush=True)
        return None

# Function to extract OI values for "ETH Call" and "ETH Put"
def calculate_oi(data):
    eth_call_oi = 0.0
    eth_put_oi = 0.0
    eth_call_volume = 0.0
    eth_put_volume = 0.0
    
    for item in data['result']:
        description = item.get('description', '')
        oi_value = float(item.get('oi_value_usd', 0))
        volume = float(item.get('volume', 0))
        
        if "ETH  Call" in description:
            eth_call_oi += oi_value
            eth_call_volume += volume
        elif "ETH  Put" in description:
            eth_put_oi += oi_value
            eth_put_volume += volume

    return eth_call_oi, eth_put_oi, eth_call_volume, eth_put_volume

# Function to save the diff value to a text file
def save_diff_to_file(diff_oi, diff_vol):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"ETH-OI-{current_date}.txt"
    
    with open(file_name, 'a') as f:
        f.write(f"{current_date_time}#{diff_oi}#{diff_vol}\n")

# Function to read the file and plot the data
def read_and_plot(diff_oi, diff_vol):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"ETH-OI-{current_date}.txt"
    
    timestamps = []
    diffs_oi = []
    diffs_vol = []

    try:
        with open(file_name, 'r') as f:
            for line in f:
                parts = line.strip().split('#')
                if len(parts) == 3:
                    timestamps.append(parts[0])
                    diffs_oi.append(float(parts[1]))
                    diffs_vol.append(float(parts[2]))
    except FileNotFoundError:
        print(f"No data file found for {file_name}.", flush=True)
        return

    if diffs_oi and diffs_vol:
        # Plot the data
        plt.clear_data()
        plt.plot(diffs_oi, diffs_vol, label='Vol and OI Difference (ETH Put - ETH Call)')
        plt.title("Vol and OI Difference Over Time")
        plt.show()
        print(flush=True)
    else:
        print("No data available to plot.", flush=True)

# Function to predict direction based on recent data
def predict_direction():
    if len(previous_diffs_oi) >= 2 and len(previous_diffs_vol) >= 2:
        # Use the most recent two data points to predict the trend
        oi_trend = previous_diffs_oi[-1] - previous_diffs_oi[-2]
        vol_trend = previous_diffs_vol[-1] - previous_diffs_vol[-2]

        # Heuristic for prediction
        if oi_trend > 0 and vol_trend > 0:
            return "Bearish (Market Down Expected)"
        elif oi_trend < 0 and vol_trend < 0:
            return "Bullish (Market Up Expected)"
        else:
            return "Neutral"
    else:
        return "Insufficient Data for Prediction"

# Main function to run every 5 minutes
def main():
    try:
        while True:
            # Fetch data from the API
            data = fetch_data()
            
            if data:
                # Calculate OI and Volume values
                eth_call_oi, eth_put_oi, eth_call_volume, eth_put_volume = calculate_oi(data)
                
                # Calculate the difference
                diff_oi = eth_put_oi - eth_call_oi
                diff_vol = eth_put_volume - eth_call_volume

                print(f"ETH Put OI: {eth_put_oi}, ETH Call OI: {eth_call_oi}, OI Difference: {diff_oi}", flush=True)
                print(f"ETH Put Vol: {eth_put_volume}, ETH Call Vol: {eth_call_volume}, Vol Difference: {diff_vol}", flush=True)
                
                # Save the diff to a file
                save_diff_to_file(diff_oi, diff_vol)
                
                # Store differences in memory for prediction
                previous_diffs_oi.append(diff_oi)
                previous_diffs_vol.append(diff_vol)

                # Limit the history length to 6 data points (1 hour with 10 min intervals)
                if len(previous_diffs_oi) > max_history:
                    previous_diffs_oi.pop(0)
                if len(previous_diffs_vol) > max_history:
                    previous_diffs_vol.pop(0)

                # Predict the direction based on recent data
                prediction = predict_direction()
                print(f"Market Prediction for Next Hour: {prediction}", flush=True)
                
                # Read the file and plot the data
                read_and_plot(diff_oi, diff_vol)
            
            # Wait for 10 minutes before running again (600 seconds)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...", flush=True)

# Run the main function
if __name__ == "__main__":
    main()
