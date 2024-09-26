import requests
import pandas as pd
from datetime import datetime, timedelta

# URLs for fetching option chain data
url_bnf = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

# Function to fetch option chain data from NSE
def fetch_option_chain(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # Sending GET request to fetch data
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None

# Function to filter strikes with high OI and low volume
def filter_oi_volume(data, volume_threshold=1000, oi_threshold=100000):
    ce_data = []
    pe_data = []

    # Iterate over all strikes and extract CE and PE data
    if 'records' in data and 'data' in data['records']:
        for strike in data['records']['data']:
            if 'CE' in strike and 'PE' in strike:
                ce = strike['CE']
                pe = strike['PE']
                expiry_date = datetime.strptime(ce['expiryDate'], '%d-%b-%Y').date()

                # Check for CE with low volume and high OI
                if 'volume' in ce and 'openInterest' in ce:
                    if ce['volume'] < volume_threshold and ce['openInterest'] > oi_threshold:
                        ce_data.append({
                            'Strike Price': ce['strikePrice'],
                            'Volume': ce['volume'],
                            'Open Interest': ce['openInterest'],
                            'Expiry Date': ce['expiryDate'],
                            'Type': 'CE'
                        })

                # Check for PE with low volume and high OI
                if 'volume' in pe and 'openInterest' in pe:
                    if pe['volume'] < volume_threshold and pe['openInterest'] > oi_threshold:
                        pe_data.append({
                            'Strike Price': pe['strikePrice'],
                            'Volume': pe['volume'],
                            'Open Interest': pe['openInterest'],
                            'Expiry Date': pe['expiryDate'],
                            'Type': 'PE'
                        })

    return ce_data, pe_data

# Fetch Nifty and BankNifty option chain data
print("Fetching Nifty option chain data...")
nifty_data = fetch_option_chain(url_nf)
if not nifty_data:
    print("Failed to fetch Nifty option chain data.")
    nifty_data = {}

print("Fetching BankNifty option chain data...")
banknifty_data = fetch_option_chain(url_bnf)
if not banknifty_data:
    print("Failed to fetch BankNifty option chain data.")
    banknifty_data = {}

# Process and filter Nifty data
if nifty_data:
    print("Processing Nifty options data...")
    nifty_ce, nifty_pe = filter_oi_volume(nifty_data)
    print(f"Nifty Call Options with low volume but high OI (Weekly Expiries):\n{pd.DataFrame(nifty_ce)}")
    print(f"Nifty Put Options with low volume but high OI (Weekly Expiries):\n{pd.DataFrame(nifty_pe)}")
else:
    print("Nifty data is not available, skipping Nifty processing.")

# Process and filter BankNifty data
if banknifty_data:
    print("Processing BankNifty options data...")
    banknifty_ce, banknifty_pe = filter_oi_volume(banknifty_data)
    print(f"BankNifty Call Options with low volume but high OI (Weekly Expiries):\n{pd.DataFrame(banknifty_ce)}")
    print(f"BankNifty Put Options with low volume but high OI (Weekly Expiries):\n{pd.DataFrame(banknifty_pe)}")
else:
    print("BankNifty data is not available, skipping BankNifty processing.")
