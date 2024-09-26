import sys
import io
import time
import subprocess
from datetime import datetime
import plotext as plt

# Set the encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Move arrays to the outer scope
nifty_diffs = []
banknifty_diffs = []

def plot_differences():
    if nifty_diffs and banknifty_diffs:
        # Use indices as x-axis values
        indices = list(range(len(nifty_diffs)))
        nifty_values = [int(item.split("#")[1].strip()) for item in nifty_diffs]
        banknifty_values = [int(item.split("#")[1].strip()) for item in banknifty_diffs]

        # Clear the console plot
        plt.clear_figure()

        # Plot Nifty OI differences
        plt.title("Nifty OI Differences Over Time")
        plt.plot(indices, nifty_values, label="Nifty OI Difference", marker='o', color='blue')
        plt.canvas_color('black')
        plt.axes_color('black')
        plt.ticks_color('white')
        plt.xlabel("Data Points")
        plt.ylabel("OI Difference")
        plt.grid(True)
        plt.show()

        # Plot Bank Nifty OI differences
        plt.title("Bank Nifty OI Differences Over Time")
        plt.plot(indices, banknifty_values, label="Bank Nifty OI Difference", marker='o', color='green')
        plt.canvas_color('black')
        plt.axes_color('black')
        plt.ticks_color('white')
        plt.xlabel("Data Points")
        plt.ylabel("OI Difference")
        plt.grid(True)
        plt.show()

def update_data_and_plot():
    last_nifty_diff = None
    last_banknifty_diff = None
    
    while True:
        try:
            # Run the main.py script and capture the output
            result = subprocess.run(["python", "scripts/main.py"], capture_output=True, text=True, encoding='utf-8')
            
            # Get the current time
            calculated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract the Nifty and BankNifty OI differences from the output
            lines = result.stdout.splitlines()
            for line in lines:
                try:
                    if "Nifty OI Difference" in line:
                        parts = line.split(":")
                        if len(parts) >= 3:  # Ensure there are enough parts to split
                            nifty_diff = int(parts[1].split(",")[0].strip())
                            banknifty_diff = int(parts[2].strip())

                            # Check if the new data is different from the last recorded data
                            if nifty_diff != last_nifty_diff or banknifty_diff != last_banknifty_diff:
                                nifty_diffs.append(f"{calculated_time}# {nifty_diff}")
                                banknifty_diffs.append(f"{calculated_time}# {banknifty_diff}")
                                last_nifty_diff = nifty_diff
                                last_banknifty_diff = banknifty_diff
                        else:
                            print(f"Warning: Unexpected line format: {line}")
                except ValueError as ve:
                    print(f"Error parsing line: {line}\nError: {ve}")

            # Print the current arrays
            print("\nNifty OI Differences:")
            for item in nifty_diffs:
                print(item, flush=True)

            print("\nBank Nifty OI Differences:")
            for item in banknifty_diffs:
                print(item, flush=True)
            
            # Plot the differences in the console
            plot_differences()

            # Wait for 5 minutes (300 seconds) before running the script again
            time.sleep(300)
        
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

def run_main_script():
    update_data_and_plot()  # Start the data update and plot

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("Nifty OI Differences:", nifty_diffs, flush=True)
        print("Bank Nifty OI Differences:", banknifty_diffs, flush=True)
