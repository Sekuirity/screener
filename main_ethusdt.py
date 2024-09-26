import json
import math
from datetime import datetime

# Method to get nearest strikes for ETHUSDT
def nearest_strike_ethusdt(x): return int(math.ceil(float(x)/25)*25)  # Assuming 25 as the nearest interval for ETHUSDT

# Mock function to simulate fetching ETHUSDT option chain data
def mock_get_data():
    # This is a mock response simulating what you might get from an actual API
    return json.dumps({
        "records": {
            "expiryDates": ["2024-12-31"],
            "data": [
                {"expiryDate": "2024-12-31", "strikePrice": 4000, "CE": {"openInterest": "120"}, "PE": {"openInterest": "100"}},
                {"expiryDate": "2024-12-31", "strikePrice": 4025, "CE": {"openInterest": "130"}, "PE": {"openInterest": ""}},  # Simulate an issue
                # Add more data as required...
            ]
        }
    })

def safe_int_conversion(value, label):
    if value.isdigit():
        return int(value)
    else:
        print(f"Conversion error: Could not convert '{value}' to an integer for {label}. Defaulting to 0.")
        return 0

def total_oi_CE_PE_with_difference(num, step, nearest):
    total_oi_CE = 0
    total_oi_PE = 0
    strike = nearest - (step * num)
    start_strike = nearest - (step * num)
    response_text = mock_get_data()  # Replace this with the actual API call
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]

    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if start_strike <= item["strikePrice"] < start_strike + (step * num * 2):
                ce_oi = safe_int_conversion(item["CE"].get("openInterest", "0"), f"CE at strike {item['strikePrice']}")
                pe_oi = safe_int_conversion(item["PE"].get("openInterest", "0"), f"PE at strike {item['strikePrice']}")
                total_oi_CE += ce_oi
                total_oi_PE += pe_oi
                strike = strike + step
                # Debug output to trace accumulation
                print(f"Matched Strike: {item['strikePrice']} | CE OI: {ce_oi} | PE OI: {pe_oi}")
    
    oi_difference = total_oi_PE - total_oi_CE
    # Debug output to check final sums
    print(f"Total CE OI: {total_oi_CE} | Total PE OI: {total_oi_PE} | OI Difference: {oi_difference}")
    return total_oi_CE, total_oi_PE, oi_difference

def run_script():
    ethusdt_nearest = nearest_strike_ethusdt(4000)  # Example nearest strike value
    ethusdt_total_oi_CE, ethusdt_total_oi_PE, ethusdt_oi_difference = total_oi_CE_PE_with_difference(10, 25, ethusdt_nearest)
    return ethusdt_oi_difference

if __name__ == "__main__":
    ethusdt_diff = run_script()
    print(f"ETHUSDT OI Difference: {ethusdt_diff}")

    # Assuming this is within some kind of loop or repeated execution:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"ETHUSDT OI Differences:\n{current_time}# {ethusdt_diff}")
