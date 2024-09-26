import numpy as np
import pandas as pd
import requests
import winsound
import time

# API URL for Delta Exchange Tickers
url = "https://api.delta.exchange/v2/tickers"

def get_ticker_data(symbol="ETHUSDT"):
    """Fetch live price data for the specified symbol"""
    response = requests.get(url)
    data = response.json()
    for item in data['result']:
        if item['symbol'] == symbol:
            return float(item['mark_price'])
    return None

def calculate_sma(prices, period):
    """Simple Moving Average"""
    return pd.Series(prices).rolling(window=period).mean()

def calculate_ema(prices, period):
    """Exponential Moving Average"""
    return pd.Series(prices).ewm(span=period, adjust=False).mean()

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    """Calculate MACD and Signal Line"""
    short_ema = calculate_ema(prices, short_period)
    long_ema = calculate_ema(prices, long_period)
    macd = short_ema - long_ema
    signal = calculate_ema(macd, signal_period)
    return macd, signal

def calculate_momentum(prices, period=10):
    """Momentum Indicator"""
    momentum = pd.Series(prices).diff(period)
    return momentum

def check_crossover(line1, line2):
    """Check if two lines have crossed over each other"""
    if len(line1) < 2 or len(line2) < 2:
        return False  # Not enough data points to check crossover
    return (line1.iloc[-2] < line2.iloc[-2] and line1.iloc[-1] > line2.iloc[-1]) or (line1.iloc[-2] > line2.iloc[-2] and line1.iloc[-1] < line2.iloc[-1])

def calculate_smio(prices, period=14):
    """Calculate SMIO (Stochastic Momentum Index Oscillator)"""
    high_period = pd.Series(prices).rolling(window=period).max()
    low_period = pd.Series(prices).rolling(window=period).min()
    k = 100 * (pd.Series(prices) - low_period) / (high_period - low_period)
    d = k.rolling(window=3).mean()
    return k, d

# Main loop to fetch data, calculate indicators, and check conditions
prices = []
i=0

while True:
    
    # Fetch live price
    price = get_ticker_data("ETHUSDT")
    
    print(price)

    if price:
        prices.append(price)

        # Keep the price history to a manageable size
        if len(prices) > 50:
            prices.pop(0)

        if len(prices) >= 26:  # Ensure enough data points
            # Calculate SMIO
            smio_k, smio_d = calculate_smio(prices)
            smio_cross = check_crossover(smio_k, smio_d)

            # Calculate MACD
            macd, signal = calculate_macd(prices)
            macd_cross = check_crossover(macd, signal)

            # Calculate Momentum
            momentum = calculate_momentum(prices)
            if len(momentum) >= 2:  # Check if momentum has enough data points
                mom_dir = np.sign(momentum.iloc[-1] - momentum.iloc[-2])
                macd_dir = np.sign(macd.iloc[-1] - macd.iloc[-2])
                smio_dir = np.sign(smio_k.iloc[-1] - smio_k.iloc[-2])

                # Check if Momentum follows the same direction
                same_direction = (mom_dir == macd_dir == smio_dir)

                # If all conditions are met, trigger the beep
                print("smio_cross", smio_cross , "macd_cross", macd_cross , "same_direction", same_direction, flush=True)

                if smio_cross and macd_cross and same_direction:
                    print("All conditions met! Beeping twice.")
                    for _ in range(2):
                        winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms

    time.sleep(10)  # Check every 60 seconds
    i=i+1
    print ("Run # ", i, flush=True)
