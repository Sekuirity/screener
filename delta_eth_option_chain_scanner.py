import requests
import time
from bs4 import BeautifulSoup

# URL to fetch data (Adjust as per actual API or webpage URL if scraping)
URL = 'https://www.delta.exchange/app/options_chain/trade/ETH/C-ETH-2380-140924'

# Array to store the historical values of A, B, and D
oi_data_history = []

# Function to fetch the option chain data
def fetch_option_chain():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch data from the server.", flush=True)
        return None

# Function to parse the option chain and extract OI and volume data
def parse_option_chain(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    
    # Assuming there is a structured table in the HTML for options data
    rows = soup.find_all('tr')  # Adjust this based on actual HTML structure
    option_data = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            strike_price = cols[0].text.strip()
            ce_oi = float(cols[1].text.strip().replace(",", ""))
            pe_oi = float(cols[2].text.strip().replace(",", ""))
            ce_vol = float(cols[3].text.strip().replace(",", ""))
            pe_vol = float(cols[4].text.strip().replace(",", ""))
            
            option_data.append({
                'strike_price': strike_price,
                'ce_oi': ce_oi,
                'pe_oi': pe_oi,
                'ce_vol': ce_vol,
                'pe_vol': pe_vol
            })
    
    return option_data

# Function to calculate the total OI, volume, and difference between CE and PE
def calculate_totals(option_data):
    total_oi_ce = 0
    total_oi_pe = 0
    total_vol_ce = 0
    total_vol_pe = 0

    for data in option_data:
        total_oi_ce += data['ce_oi']
        total_oi_pe += data['pe_oi']
        total_vol_ce += data['ce_vol']
        total_vol_pe += data['pe_vol']
    
    # Difference D = B - A (Total PE OI - Total CE OI)
    difference = total_oi_pe - total_oi_ce
    
    # Store the results in the history array
    oi_data_history.append({
        'total_oi_ce': total_oi_ce,
        'total_oi_pe': total_oi_pe,
        'total_vol_ce': total_vol_ce,
        'total_vol_pe': total_vol_pe,
        'difference': difference
    })

    return total_oi_ce, total_oi_pe, total_vol_ce, total_vol_pe, difference

# Main function to run the program every 1 minute
def main():
    while True:
        html_data = fetch_option_chain()
        if html_data:
            option_data = parse_option_chain(html_data)
            
            # Calculate the totals
            total_oi_ce, total_oi_pe, total_vol_ce, total_vol_pe, difference = calculate_totals(option_data)
            
            # Print the totals
            print("\nTotal OI (CE):", total_oi_ce, flush=True)
            print("Total OI (PE):", total_oi_pe, flush=True)
            print("Total Volume (CE):", total_vol_ce, flush=True)
            print("Total Volume (PE):", total_vol_pe, flush=True)
            print("Difference (PE OI - CE OI):", difference, flush=True)

            # Print the history of A, B, and D
            print("\nOI Data History (A = CE OI, B = PE OI, D = B - A):", flush=True)
            for idx, record in enumerate(oi_data_history):
                print(f"Iteration {idx + 1}: A = {record['total_oi_ce']}, B = {record['total_oi_pe']}, D = {record['difference']}", flush=True)

        # Wait for 1 minute before running again
        time.sleep(60)

if __name__ == "__main__":
    main()
