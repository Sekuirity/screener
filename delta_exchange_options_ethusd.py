import requests
from bs4 import BeautifulSoup
import schedule
import time

def fetch_option_chain_data():
    url = 'https://www.delta.exchange/app/options_chain/trade/ETH/C-ETH-2380-140924'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        ce_sum = 0
        pe_sum = 0

        # Adjust based on actual class names or tags for the option rows
        options_table = soup.find_all('div', class_='option-row')  # Find all option rows
        
        for row in options_table:
            # Locate OI and option type for each row
            option_type = row.find('div', class_='strike')  # Adjust based on actual class for option type
            oi_value = row.find('div', class_='oi-class')  # Adjust with actual class for OI
            
            if option_type and oi_value:
                option_type_text = option_type.text.strip()
                oi_value_text = oi_value.text.strip()

                # Convert OI value to float, handling cases like 71.99K, 402.42K, etc.
                if 'K' in oi_value_text:
                    oi_value_float = float(oi_value_text.replace('K', '').replace('$', '').replace(',', '')) * 1000
                elif 'M' in oi_value_text:
                    oi_value_float = float(oi_value_text.replace('M', '').replace('$', '').replace(',', '')) * 1000000
                else:
                    oi_value_float = float(oi_value_text.replace('$', '').replace(',', ''))

                # Sum OI values based on Call or Put (adjust this check based on the HTML structure)
                if 'Call' in option_type_text:  # Adjust this based on actual text for Calls
                    ce_sum += oi_value_float
                elif 'Put' in option_type_text:  # Adjust this based on actual text for Puts
                    pe_sum += oi_value_float

        # Calculate the difference D = B - A
        difference = pe_sum - ce_sum
        print(f"Sum of CE (Call) OI: {ce_sum}, Sum of PE (Put) OI: {pe_sum}, Difference (D = B - A): {difference}", flush=True)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}", flush=True)

def job():
    fetch_option_chain_data()

# Schedule the job every 10 seconds
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
