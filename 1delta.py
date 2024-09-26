import time
from colorama import Fore, Style, init
# Libraries
import requests
import json
import math
import time as t  # Renaming `time` to avoid conflicts with the `time` module
import os
from termcolor import colored


# Initialize colorama
init(autoreset=True)

# API URL for Delta Exchange Tickers
url = "https://api.delta.exchange/v2/tickers"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

def set_cookie():
    for i in range(3):  # Retry mechanism with 3 attempts
        try:
            request = sess.get(url_oc, headers=headers, timeout=10)
            cookies = dict(request.cookies)
            break  # Exit the loop if successful
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}", flush=True)
            if i < 2:
                print(f"Retrying in 5 seconds...", flush=True)
                t.sleep(5)
            else:
                print("Max retries reached. Exiting.", flush=True)
                return None


# Python program to print
# colored text and background
def strRed(skk):         return "\033[91m {}\033[00m".format(skk)
def strGreen(skk):       return "\033[92m {}\033[00m".format(skk)
def strYellow(skk):      return "\033[93m {}\033[00m".format(skk)
def strLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
def strPurple(skk):      return "\033[95m {}\033[00m".format(skk)
def strCyan(skk):        return "\033[96m {}\033[00m".format(skk)
def strLightGray(skk):   return "\033[97m {}\033[00m".format(skk)
def strBlack(skk):       return "\033[98m {}\033[00m".format(skk)
def strBold(skk):        return "\033[1m {}\033[0m".format(skk)

# Method to get nearest strikes
def round_nearest(x,num=50): return int(math.ceil(float(x)/num)*num)
def nearest_strike_bnf(x): return round_nearest(x,100)
def nearest_strike_nf(x): return round_nearest(x,50)


# Function to print column headers in yellow
def print_headers():
    print(Fore.YELLOW + f"{'OI Contracts':<15}  {'Total OI':<10}  {'Volume':<12}  {'Spot Price':<12}  {'Mark Price':<12}", flush=True)

# Function to fetch ETHUSD data
def fetch_ethusd_data():
    response = requests.get(url)
    data = response.json()

    # Find data for the symbol "ETHUSD"
    for item in data['result']:
        if item['symbol'] == "ETHUSD":
            # Extract required fields
            oi_contracts = item.get('oi_contracts')
            oi = int(float(item.get('oi', 0)))  # Convert to integer (no decimals)
            size = item.get('size')
            spot_price = int(float(item.get('spot_price', 0)))
            volume = item.get('volume')
            mark_price = int(float(item.get('mark_price', 0))) 

            # Print the extracted values exactly below headers
            print(f"{oi_contracts:<15}  {oi:<10}  {volume:<12}  {spot_price:<12}  {mark_price:<12}", flush=True)

# Main loop to run the fetch function every 10 seconds
row_count = 0  # Keep track of rows printed
while True:
    if row_count % 10 == 0:  # Print headers every 10 rows
        print_headers()
    
    fetch_ethusd_data()
    
    row_count += 1
    time.sleep(300)  # Pause for 5 minutes
