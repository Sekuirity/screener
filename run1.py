import time
import subprocess
from datetime import datetime

# Move arrays to the outer scope
nifty_diffs = []
banknifty_diffs = []

def run_main_script():
    while True:
        try:
            # Run the main.py script and capture the output
            result = subprocess.run(["python", "scripts/main1.py"], capture_output=True, text=True)
            
            # Get the current time
            calculated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract the Nifty and BankNifty OI differences from the output
            lines = result.stdout.splitlines()
            for line in lines:
                if "Nifty OI Difference" in line:
                    parts = line.split(":")
                    nifty_diff = int(parts[1].split(",")[0].strip())
                    banknifty_diff = int(parts[2].strip())

                    # Store the differences in the arrays with their calculated times
                    nifty_diffs.append(f"{calculated_time}# {nifty_diff}")
                    banknifty_diffs.append(f"{calculated_time}# {banknifty_diff}")

            # Print the current arrays
            print("\nNifty OI Differences:")
            for item in nifty_diffs:
                print(item, flush=True)

            print("\nBank Nifty OI Differences:")
            for item in banknifty_diffs:
                print(item, flush=True)

            # Wait for 5 seconds before running the script again
            time.sleep(5)
        
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("Nifty OI Differences:", nifty_diffs, flush=True)
        print("Bank Nifty OI Differences:", banknifty_diffs, flush=True)
