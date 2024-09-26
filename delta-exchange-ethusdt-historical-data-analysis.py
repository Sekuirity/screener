import requests
import numpy as np
import time
import datetime

# Function to calculate the current time and 5 years ago in Unix time
def get_time_range():
    current_time = int(time.time())  # Current time in seconds (Unix timestamp)
    five_years_seconds = 1 * 365 * 24 * 60 * 60  # 5 years in seconds
    start_time = current_time - five_years_seconds  # 5 years back from current time
    return start_time, current_time

# Define a function to fetch historical data from the API
def fetch_historical_data():
    start_time, end_time = get_time_range()

    # Endpoint and parameters for historical data (15-minute intervals)
    url = 'https://api.delta.exchange/v2/history/candles'
    params = {
        'resolution': '15m',  # 15-minute interval
        'symbol': 'ETHUSD',
        'start': start_time,  # Start timestamp (5 years ago)
        'end': end_time       # End timestamp (current time)
    }

    # Fetch the data from the API
    response = requests.get(url, params=params)
    data = response.json()

    print(data)


    if 'result' in data:
        return data['result']
    else:
        print("Error fetching data")
        return []

# Function to analyze the historical data and predict the next move
def analyze_and_predict(historical_data):
    # Extract close prices from the historical data
    close_prices = [float(candle['close']) for candle in historical_data]
    
    # Calculate the recent trend by finding the slope of the last 5 data points
    recent_prices = close_prices[-5:]
    time_intervals = range(5)  # Assume equal time intervals for the last 5 data points

    # Use numpy's polyfit to calculate the slope of the trend line
    z = np.polyfit(time_intervals, recent_prices, 1)
    slope = z[0]

    # Predict the next move based on the slope
    if slope > 0:
        prediction = "UP"
    else:
        prediction = "DOWN"

    # Consistent print for recent prices and prediction
    print(f"Recent prices: {recent_prices}")
    print(f"Predicted Next Move: {prediction}")

    return prediction

# Main function to run the analysis and prediction
def main():
    try:
        while True:
            # Fetch historical data and make predictions
            historical_data = fetch_historical_data()
            if historical_data:
                # Analyze the historical data and make a prediction
                prediction = analyze_and_predict(historical_data)

                # Print the current date and time for reference
                current_time = datetime.datetime.now()
                print(f"Prediction at {current_time}: {prediction}\n")
            
            # Wait for 1 minute before fetching and analyzing data again
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")

# Run the main function
if __name__ == "__main__":
    main()
