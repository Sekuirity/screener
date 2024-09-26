import sys
import os
import requests
import time
import plotext as plt
import numpy as np

# Force Python to use UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Define a function to connect to the API, fetch data, and process the results
def fetch_ethusdt_data():
    url = 'https://api.delta.exchange/v2/trades/ETHUSDT'
    response = requests.get(url)
    data = response.json()
    
    # Extract price and size from the response
    trades = data['result']
    prices = [float(trade['price']) for trade in trades]
    sizes = [float(trade['size']) for trade in trades]
    
    # Calculate A (sum of prices) and B (sum of sizes)
    A = sum(prices)
    B = sum(sizes)
    
    # Calculate D (B - A) as an integer
    D = int(B - A)
    
    # Consistent output for every iteration
    print(f"\nDifference (D) = B - A: {D}")
    print(f"Sum of Prices (A): {int(A)}")
    print(f"Sum of Sizes (B): {int(B)}")
    print(f"Difference (D = B - A): {D}\n")
    
    return prices, sizes, D

# Function to plot the trend line and predict the next move
def plot_and_predict(prices):
    # Clear the previous data to refresh the console plot
    plt.clear_data()
    
    # Plotting the prices
    plt.plot(prices, label='Price')
    
    # Calculate the trend line using numpy's polyfit (1st-degree polynomial)
    z = np.polyfit(range(len(prices)), prices, 1)
    p = np.poly1d(z)
    
    # Plot the trend line
    trend_line = [p(x) for x in range(len(prices))]
    plt.plot(trend_line, label='Trend line', marker=".")
    
    # Predict the next move: if slope of the trend line is positive, predict UP, otherwise DOWN
    next_move = "UP" if z[0] > 0 else "DOWN"
    
    # Consistent print for predicted next move
    print(f"Predicted Next Move: {next_move}\n")
    
    # Display the plot in the console
    plt.show()

    return next_move

# Main loop that runs every minute
def main():
    prices = []
    while True:
        # Fetch data from the API and calculate D
        new_prices, sizes, D = fetch_ethusdt_data()
        
        # Store the latest prices (average price per minute, rounded to integer)
        prices.append(int(sum(new_prices) / len(new_prices)))
        
        # If enough data points, plot the trend and predict the next move
        if len(prices) >= 5:
            next_move = plot_and_predict(prices[-5:])  # Use the last 5 data points for trend analysis
        
        # Wait for 1 minute before fetching data again
        time.sleep(60)

# Run the main loop
if __name__ == "__main__":
    main()
