import sys
import io
import time
import subprocess
from datetime import datetime
import plotext as plt

# Set the encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Move arrays to the outer scope
ethusdt_diffs = []

def plot_differences():
    if ethusdt_diffs:
        # Use indices as x-axis values
        indices = list(range(len(ethusdt_diffs)))
        ethusdt_values = [int(item.split("#")[1].strip()) for item in ethusdt_diffs]

        # Clear the console plot
        plt.clear_figure()

        # Plot ETHUSDT OI differences
        plt.title("ETHUSDT OI Differences Over Time")
        plt.plot(indices, ethusdt_values, label="ETHUSDT OI Difference", marker='o', color='blue')
        plt.canvas_color('black')
        plt.axes_color('black')
        plt.ticks_color('white')
        plt.xlabel("Data Points")
        plt.ylabel("OI Difference")
        plt.grid(True)
        plt.show()

def update_data_and_plot():
    while True:
        try:
            # Run the main_ethusdt.py script and capture the output
            result = subprocess.run(["python", "scripts/main_ethusdt.py"], capture_output=True, text=True, encoding='utf-8')
            
            # Get the current time
            calculated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract the ETHUSDT OI differences from the output
            lines = result.stdout.splitlines()
            for line in lines:
                if "ETHUSDT OI Difference" in line:
                    parts = line.split(":")
                    ethusdt_diff = int(parts[1].strip())

                    # Store the differences in the arrays with their calculated times
                    ethusdt_diffs.append(f"{calculated_time}# {ethusdt_diff}")

            # Print the current arrays
            print("\nETHUSDT OI Differences:")
            for item in ethusdt_diffs:
                print(item, flush=True)
            
            # Plot the differences in the console
            plot_differences()

            # Wait for 5 minutes (300 seconds) before running the script again
            time.sleep(10)
        
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

def run_main_script():
    update_data_and_plot()  # Start the data update and plot

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("ETHUSDT OI Differences:", ethusdt_diffs, flush=True)
