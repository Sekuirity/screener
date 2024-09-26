# Libraries
import requests
import json
import math
import time as t  # Renaming `time` to avoid conflicts with the `time` module
import os
from termcolor import colored

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

# Urls for fetching Data
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

'''
# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""
'''

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

def get_data(url):
    for i in range(3):  # Retry mechanism with 3 attempts
        try:
            set_cookie()
            response = sess.get(url, headers=headers, timeout=10, cookies=cookies)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed with status code {response.status_code}", flush=True)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}", flush=True)
            if i < 2:
                print(f"Retrying in 5 seconds...", flush=True)
                t.sleep(5)
            else:
                print("Max retries reached. Exiting.", flush=True)
                return None


def set_header():
    global bnf_ul
    global nf_ul
    global bnf_nearest
    global nf_nearest
    response_text = get_data(url_indices)
    data = json.loads(response_text)
    for index in data["data"]:
        if index["index"]=="NIFTY 50":
            nf_ul = index["last"]
            print("nifty", flush=True)
        if index["index"]=="NIFTY BANK":
            bnf_ul = index["last"]
            print("banknifty", flush=True)
    bnf_nearest=nearest_strike_bnf(bnf_ul)
    nf_nearest=nearest_strike_nf(nf_ul)

# Showing Header in structured format with Last Price and Nearest Strike

def print_header(index="",ul=0,nearest=0):
    print(strPurple( index.ljust(12," ") + " => ")+ strLightPurple(" Last Price: ") + strBold(str(ul)) + strLightPurple(" Nearest Strike: ") + strBold(str(nearest)), flush=True)

def print_hr():
    print(strYellow("|".rjust(110,"-")), flush=True)

# Fetching CE and PE data based on Nearest Expiry Date
def print_oi(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    print("Strike------------------OI------------Volume-------------------OI------------Volume----------OI Diff----------Volume Diff", flush=True)
    for item in data['records']['data']:
        #print(data['records'], flush=True)
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                #print("Strike------------------OI------------Volume-------------------OI------------Volume------OI Diff-------Volume Diff", flush=True)
                #print(strCyan(str(item["strikePrice"])) + strGreen(" CE ") + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" +  "[ " + strBold(str(item["CE"]["totalTradedVolume"]).rjust(10," ")) + " ]" + strRed(" PE ")+"[ " + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + strBold(str(item["PE"]["totalTradedVolume"]).rjust(10," ")) + "\t\t" + str((item["PE"]["openInterest"]) - (item["CE"]["openInterest"])) + "\t\t" + str((item["PE"]["totalTradedVolume"]) - (item["CE"]["totalTradedVolume"])) + "   ]", flush=True)
                #print(strCyan(str(item["strikePrice"])) + ",\t" + strGreen("CE") + ",\t" + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + ",\t" + strBold(str(item["CE"]["totalTradedVolume"]).rjust(10," ")) + ",\t" + strRed("PE") + ",\t" + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + ",\t" + strBold(str(item["PE"]["totalTradedVolume"]).rjust(10," ")) + ",\t" + strBold(str((item["PE"]["openInterest"]) - (item["CE"]["openInterest"]))) + ",\t\t" + strBold(str((item["PE"]["totalTradedVolume"]) - (item["CE"]["totalTradedVolume"]))) , flush=True)
                #print(data["records"]["expiryDates"][0] + " " + str(item["strikePrice"]) + " CE " + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + " PE " + "[ " + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + " ]", flush=True)
                print(
                    strCyan(str(item["strikePrice"])) + ",\t" +
                    strGreen("CE") + ",\t" +
                    strBold(str(item["CE"]["openInterest"]).rjust(10, " ")) + ",\t" +
                    strBold(str(item["CE"]["totalTradedVolume"]).rjust(10, " ")) + ",\t" +
                    strRed("PE") + ",\t" +
                    strBold(str(item["PE"]["openInterest"]).rjust(10, " ")) + ",\t" +
                    strBold(str(item["PE"]["totalTradedVolume"]).rjust(10, " ")) + ",\t" +
                    strBold(str((item["PE"]["openInterest"] - item["CE"]["openInterest"])).rjust(10, " ")) + ",\t" +  # OI Diff aligned
                    strBold(str((item["PE"]["totalTradedVolume"] - item["CE"]["totalTradedVolume"])).rjust(12, " "))   # Volume Diff aligned
                , flush=True)
                
                strike = strike + step

# Finding highest Open Interest of People's in CE based on CE data         
def highest_oi_CE(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["CE"]["openInterest"] > max_oi:
                    max_oi = item["CE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

# Finding highest Open Interest of People's in PE based on PE data 
def highest_oi_PE(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["PE"]["openInterest"] > max_oi:
                    max_oi = item["PE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

set_header()
print('\033c', flush=True)
print_hr()
print_header("Nifty",nf_ul,nf_nearest)
print_hr()
print_oi(10,50,nf_nearest,url_nf)
print_hr()
print_header("Bank Nifty",bnf_ul,bnf_nearest)
print_hr()
print_oi(10,100,bnf_nearest,url_bnf)
print_hr()

# Finding Highest OI in Call Option In Nifty
nf_highestoi_CE = highest_oi_CE(10,50,nf_nearest,url_nf)

# Finding Highet OI in Put Option In Nifty
nf_highestoi_PE = highest_oi_PE(10,50,nf_nearest,url_nf)

# Finding Highest OI in Call Option In Bank Nifty
bnf_highestoi_CE = highest_oi_CE(10,100,bnf_nearest,url_bnf)

# Finding Highest OI in Put Option In Bank Nifty
bnf_highestoi_PE = highest_oi_PE(10,100,bnf_nearest,url_bnf)


print(strCyan(str("Major Resistance in Nifty:")) + str(nf_highestoi_CE), flush=True)
print(strCyan(str("Major Support in Nifty:")) + str(nf_highestoi_PE), flush=True)
print_hr()
print(strPurple(str("Major Resistance in Bank Nifty:")) + str(bnf_highestoi_CE), flush=True)
print(strPurple(str("Major Support in Bank Nifty:")) + str(bnf_highestoi_PE), flush=True)

print_hr()

def total_oi_CE_PE_with_difference(num, step, nearest, url):
    total_oi_CE = 0
    total_oi_PE = 0
    strike = nearest - (step * num)
    start_strike = nearest - (step * num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike + (step * num * 2):
                total_oi_CE += item["CE"]["openInterest"]
                total_oi_PE += item["PE"]["openInterest"]
                strike = strike + step
    
    oi_difference = total_oi_PE - total_oi_CE
    return total_oi_CE, total_oi_PE, oi_difference

# Calculate and print total OI for Nifty and the difference
nifty_total_oi_CE, nifty_total_oi_PE, nifty_oi_difference = total_oi_CE_PE_with_difference(10, 50, nf_nearest, url_nf)
nifty_difference_symbol = "+" if nifty_oi_difference > 0 else "-"
#print(f'Total OI for Nifty - CE: {nifty_total_oi_CE}, PE: {nifty_total_oi_PE}, OI Difference: {nifty_difference_symbol}{abs(nifty_oi_difference)}')

# Calculate and print total OI for Bank Nifty and the difference
banknifty_total_oi_CE, banknifty_total_oi_PE, banknifty_oi_difference = total_oi_CE_PE_with_difference(10, 100, bnf_nearest, url_bnf)
banknifty_difference_symbol = "+" if banknifty_oi_difference > 0 else "-"
#print(f'Total OI for Bank Nifty - CE: {banknifty_total_oi_CE}, PE: {banknifty_total_oi_PE}, OI Difference: {banknifty_difference_symbol}{abs(banknifty_oi_difference)}')

'''
def run_script():
    # Existing code should be here, ensuring it calculates the OI differences and returns them
    
    def total_oi_CE_PE_with_difference(num, step, nearest, url):
        total_oi_CE = 0
        total_oi_PE = 0
        strike = nearest - (step * num)
        start_strike = nearest - (step * num)
        response_text = get_data(url)
        data = json.loads(response_text)
        currExpiryDate = data["records"]["expiryDates"][0]
        
        for item in data['records']['data']:
            if item["expiryDate"] == currExpiryDate:
                if item["strikePrice"] == strike and item["strikePrice"] < start_strike + (step * num * 2):
                    total_oi_CE += item["CE"]["openInterest"]
                    total_oi_PE += item["PE"]["openInterest"]
                    strike = strike + step
        
        oi_difference = total_oi_PE - total_oi_CE
        return total_oi_CE, total_oi_PE, oi_difference

    # Assuming necessary code exists to set nf_nearest, bnf_nearest, url_nf, and url_bnf variables

    nifty_total_oi_CE, nifty_total_oi_PE, nifty_oi_difference = total_oi_CE_PE_with_difference(10, 50, nf_nearest, url_nf)
    banknifty_total_oi_CE, banknifty_total_oi_PE, banknifty_oi_difference = total_oi_CE_PE_with_difference(10, 100, bnf_nearest, url_bnf)

    return nifty_oi_difference, banknifty_oi_difference, nifty_vol_diff, banknifty_vol_diff 
'''

def total_oi_vol_CE_PE_with_difference(num, step, nearest, url):
    total_oi_CE = 0
    total_oi_PE = 0
    total_vol_CE = 0
    total_vol_PE = 0
    strike = nearest - (step * num)
    start_strike = nearest - (step * num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike + (step * num * 2):
                total_oi_CE += item["CE"]["openInterest"]
                total_oi_PE += item["PE"]["openInterest"]
                total_vol_CE += item["CE"]["totalTradedVolume"]
                total_vol_PE += item["PE"]["totalTradedVolume"]
                strike = strike + step
    
    oi_difference = total_oi_PE - total_oi_CE
    vol_difference = total_vol_PE - total_vol_CE
    
    return total_oi_CE, total_oi_PE, oi_difference, total_vol_CE, total_vol_PE, vol_difference

def clear_console():
    # Clear the console based on the OS
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')


# Run script to calculate OI and volume differences
def run_script1():
    print()

    while True:

        clear_console()
        
        try:
            nifty_total_oi_CE, nifty_total_oi_PE, nifty_oi_difference, nifty_total_vol_CE, nifty_total_vol_PE, nifty_vol_difference = total_oi_vol_CE_PE_with_difference(10, 50, nf_nearest, url_nf)
            banknifty_total_oi_CE, banknifty_total_oi_PE, banknifty_oi_difference, banknifty_total_vol_CE, banknifty_total_vol_PE, banknifty_vol_difference = total_oi_vol_CE_PE_with_difference(10, 100, bnf_nearest, url_bnf)

            print(strCyan(str("N OI Diff:")) + strCyan(str(f"{nifty_oi_difference}")) + strCyan(str(", ")) + strCyan(str("N CE Tot Vol:")) + strCyan(str(f"{nifty_total_vol_CE}")) + strCyan(str(", ")) + strCyan(str("N PE Tot Vol:")) + strCyan(str(f"{nifty_total_vol_PE}")) + strCyan(str(", ")) + strCyan(str("N Tot Vol Diff:")) + strCyan(str(f"{nifty_vol_difference}"))  + strCyan(str(", ")) + strPurple(str("BN OI Diff:")) + strPurple(str(f"{banknifty_oi_difference}")) + strPurple(str(", ")) + strPurple(str("BN CE Tot Vol:")) + strPurple(str(f"{banknifty_total_vol_CE}")) + strPurple(str(", "))  + strPurple(str("BN PE Tot Vol:")) + strPurple(str(f"{banknifty_total_vol_PE}")) + strPurple(str(", ")) + strPurple(str("BN Tot Vol Diff:")) + strPurple(str(f"{banknifty_vol_difference}"))  + strPurple(str(", ")),  flush=True)
            #print(f"N CE Tot Vol: {nifty_total_vol_CE}, N PE Tot Vol: {nifty_total_vol_PE}, N Tot Vol Diff: {nifty_vol_difference}", flush=True)
            #print(f"BN CE Tot Vol: {banknifty_total_vol_CE}, BN PE Tot Vol: {banknifty_total_vol_PE}, BN Tot Vol Diff: {banknifty_vol_difference}", flush=True)


        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

        #return nifty_oi_difference, banknifty_oi_difference, nifty_vol_difference, banknifty_vol_difference, nifty_total_vol_CE, nifty_total_vol_PE, banknifty_total_vol_CE, banknifty_total_vol_PE 
        t.sleep(180)  # Sleep for 3 minutes before running again



# Function to print column headers with appropriate colors and fixed width
def print_headers():
    '''
        print(
            colored(f"{'N OI Diff':<12}", "yellow") +
            colored(f"{'N CE Tot Vol':<15}", "yellow") +
            colored(f"{'N PE Tot Vol':<15}", "yellow") +
            colored(f"{'N Tot Vol Diff':<18}", "yellow") +
            colored(f"{'BN OI Diff':<12}", "magenta") +
            colored(f"{'BN CE Tot Vol':<15}", "magenta") +
            colored(f"{'BN PE Tot Vol':<15}", "magenta") +
            colored(f"{'BN Tot Vol Diff':<18}", "magenta")
        , flush=True)
    '''
    print(
        strCyan(str(f"{'N OI Diff':<12}")) +
        strCyan(str(f"{'N CE Tot Vol':<15}")) +
        strCyan(str(f"{'N PE Tot Vol':<15}")) +
        strCyan(str(f"{'N Tot Vol Diff':<18}")) +
        strPurple(str(f"{'BN OI Diff':<12}")) +
        strPurple(str(f"{'BN CE Tot Vol':<15}")) +
        strPurple(str(f"{'BN PE Tot Vol':<15}")) +
        strPurple(str(f"{'BN Tot Vol Diff':<18}"))
    , flush=True)

# Run script to calculate OI and volume differences
def run_script():
    print("")

    record_count = 0  # To track when to repeat the column headers
    
    while True:
        clear_console()
        
        try:
            nifty_total_oi_CE, nifty_total_oi_PE, nifty_oi_difference, nifty_total_vol_CE, nifty_total_vol_PE, nifty_vol_difference = total_oi_vol_CE_PE_with_difference(10, 50, nf_nearest, url_nf)
            banknifty_total_oi_CE, banknifty_total_oi_PE, banknifty_oi_difference, banknifty_total_vol_CE, banknifty_total_vol_PE, banknifty_vol_difference = total_oi_vol_CE_PE_with_difference(10, 100, bnf_nearest, url_bnf)

            # Print headers every 10 records
            if record_count % 10 == 0:
                print_headers()
                print("")
            # Print the data with yellow for Nifty and magenta for BankNifty columns, aligned with headers
            '''
            print(
                colored(f"{nifty_oi_difference:<12}", "yellow") +
                colored(f"{nifty_total_vol_CE:<15}", "yellow") +
                colored(f"{nifty_total_vol_PE:<15}", "yellow") +
                colored(f"{nifty_vol_difference:<18}", "yellow") +
                colored(f"{banknifty_oi_difference:<12}", "magenta") +
                colored(f"{banknifty_total_vol_CE:<15}", "magenta") +
                colored(f"{banknifty_total_vol_PE:<15}", "magenta") +
                colored(f"{banknifty_vol_difference:<18}", "magenta")
            , flush=True)
            '''
            print(
                strCyan(str(f"{nifty_oi_difference:<12}")) +
                strCyan(str(f"{nifty_total_vol_CE:<15}")) +
                strCyan(str(f"{nifty_total_vol_PE:<15}")) +
                strCyan(str(f"{nifty_vol_difference:<18}")) +
                strPurple(str(f"{banknifty_oi_difference:<12}")) +
                strPurple(str(f"{banknifty_total_vol_CE:<15}")) +
                strPurple(str(f"{banknifty_total_vol_PE:<15}")) +
                strPurple(str(f"{banknifty_vol_difference:<18}"))
            , flush=True)

            record_count += 1  # Increment record count

        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

        t.sleep(10)  # Sleep for 3 minutes before running again



if __name__ == "__main__":
            nifty_diff, banknifty_diff, nifty_vol_diff, banknifty_vol_diff, nifty_total_vol_CE, nifty_total_vol_PE, banknifty_total_vol_CE, banknifty_total_vol_PE = run_script()
        
            '''
                print()
                print(f"Nifty OI Difference: {nifty_diff}, Bank Nifty OI Difference: {banknifty_diff}", flush=True)
                #print(f"Nifty Vol Difference: {nifty_vol_diff}, Bank Nifty Vol Difference: {banknifty_vol_diff}", flush=True)
                print(f"Total Nifty CE Volume: {nifty_total_vol_CE}, PE Volume: {nifty_total_vol_PE}, Total Vol Difference: {nifty_vol_diff}", flush=True)
                print(f"Total Bank Nifty CE Volume: {banknifty_total_vol_CE}, PE Volume: {banknifty_total_vol_PE}, Total Vol Difference: {banknifty_vol_diff}", flush=True)
            '''



