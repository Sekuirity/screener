import requests
from bs4 import BeautifulSoup
import time
import schedule

def fetch_option_chain_data():
    url = 'https://www.binance.com/en/eoptions/ETHUSDT'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Parsing logic here
        ce_sum = 0  # Placeholder for sum of CE options
        pe_sum = 0  # Placeholder for sum of PE options

        # Extract and sum CE and PE values (modify based on actual HTML structure)
        options_table = soup.find_all('some_selector')  # Find the correct table or tags
        
        for row in options_table:
            option_type = row.find('option_type_selector').text  # CE or PE
            option_value = float(row.find('option_value_selector').text)  # The option value
            
            if option_type == 'CE':
                ce_sum += option_value
            elif option_type == 'PE':
                pe_sum += option_value

        difference = ce_sum - pe_sum
        print(f"Sum of CE: {ce_sum}, Sum of PE: {pe_sum}, Difference: {difference}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

def job():
    fetch_option_chain_data()

# Schedule the job every 1 minute
schedule.every(1).minutes.do(job)

# Keep running the script
while True:
    schedule.run_pending()
    time.sleep(1)
