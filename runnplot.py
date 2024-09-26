import sys
import io
import time
import subprocess
from datetime import datetime, timedelta
import plotext as plt

# Set the encoding to UTF-8 for handling output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Lists to store Nifty and Bank Nifty OI differences
nifty_diffs = []
banknifty_diffs = []

def display_values():
    # Ensure both lists have the same length
    if len(nifty_diffs) == len(banknifty_diffs):
        print("Nifty and Bank Nifty Values:")
        for nifty, banknifty in zip(nifty_diffs, banknifty_diffs):
            print(f"{nifty}  |  {banknifty}")
    else:
        print(f"Mismatch in list lengths! Nifty: {len(nifty_diffs)}, Bank Nifty: {len(banknifty_diffs)}")

def plot_differences():
    try:
        # Display values in a columnar format
        display_values()

        # Use indices as x-axis values based on the current length of the lists
        indices = list(range(len(nifty_diffs)))
        
        # Convert differences to integers
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
        
    except IndexError as ie:
        print(f"Index error during plotting: {ie}")
    except Exception as e:
        print(f"Error during plotting: {e}")

def update_data_and_plot():
    last_nifty_diff = None
    last_banknifty_diff = None
    
    while True:
        start_time = datetime.now()
        
        try:
            # Run the main.py script and capture the output
            result = subprocess.run(["python", "scripts/main.py"], capture_output=True, text=True, encoding='utf-8')
            
            # Get the current time
            calculated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract the Nifty and Bank Nifty OI differences from the output
            lines = result.stdout.splitlines()
            for line in lines:
                try:
                    if "Nifty OI Difference" in line:
                        parts = line.split(":")
                        if len(parts) >= 3:  # Ensure there are enough parts to split
                            nifty_diff_part = parts[1].split(",")
                            if len(nifty_diff_part) > 0:
                                nifty_diff = int(nifty_diff_part[0].strip())
                                banknifty_diff = int(parts[2].strip())

                                # Print debug information
                                print(f"Parsed Nifty OI Difference: {nifty_diff}")
                                print(f"Parsed Bank Nifty OI Difference: {banknifty_diff}")

                                # Check if the new data is different from the last recorded data
                                if nifty_diff != last_nifty_diff or banknifty_diff != last_banknifty_diff:
                                    nifty_diffs.append(f"{calculated_time}# {nifty_diff}")
                                    banknifty_diffs.append(f"{calculated_time}# {banknifty_diff}")
                                    last_nifty_diff = nifty_diff
                                    last_banknifty_diff = banknifty_diff
                                else:
                                    print("Data unchanged, not appending.")
                            else:
                                print(f"Warning: Unexpected Nifty OI format: {parts[1]}")
                        else:
                            print(f"Warning: Unexpected line format: {line}")
                except ValueError as ve:
                    print(f"ValueError parsing line: {line}\nError: {ve}")
                except IndexError as ie:
                    print(f"IndexError: {ie}\nLine causing issue: {line}")
                except Exception as e:
                    print(f"Unexpected error: {e}\nLine: {line}")

            # Ensure both lists are populated before plotting
            if nifty_diffs and banknifty_diffs:
                plot_differences()
            else:
                print("One of the lists is empty, skipping plot.")

        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

        # Calculate time to sleep to ensure the next iteration starts 5 minutes after the start of this iteration
        elapsed_time = datetime.now() - start_time
        sleep_time = max(0, (timedelta(minutes=5) - elapsed_time).total_seconds())
        time.sleep(sleep_time)

def run_main_script():
    update_data_and_plot()  # Start the data update and plot

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("Nifty OI Differences:", nifty_diffs, flush=True)
        print("Bank Nifty OI Differences:", banknifty_diffs, flush=True)
