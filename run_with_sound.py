import time as t  # Renaming `time` to avoid conflicts with the `time` module
import subprocess
from datetime import datetime, time  # Import `time` directly
import winsound

# Move arrays to the outer scope
nifty_diffs = []
banknifty_diffs = []

temp_nifty_diffs = []
temp_banknifty_diffs = []

def check_and_beep(index_name, previous_2_value, previous_value, current_value):
    # Calculate the difference between the values
    difference = abs(int(current_value) - int(previous_value))

    sound = r"C:\Windows\Media\Ring08.wav" 

    prev_2_size = len(str(previous_2_value))
    prev_size = len(str(previous_value))
    curr_size = len(str(current_value))

    flag = False

    if difference > 100000:
        # Sound for 1 time
        winsound.PlaySound(sound, winsound.SND_FILENAME)
        flag = False

    if previous_2_value == previous_value == current_value:
        # Sound for 1 time
        if difference == 0:
            print("Get Ready for .... "+index_name, flush=True)
            winsound.PlaySound(sound, winsound.SND_FILENAME)
            flag = False

    if abs(prev_size - curr_size) >= 1:
        flag = True

        if int(curr_size) > int(prev_size):
            print("")
            print("")
            print("Get Ready for PE BUY for "+index_name, flush=True)
            end_time = t.time() + 5
            while t.time() < end_time:
                winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 second

        if int(curr_size) < int(prev_size):
            print("")
            print("")
            print("Get Ready for CE BUY for "+index_name, flush=True)
            end_time = t.time() + 5
            while t.time() < end_time:
                winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 second

        if flag == True:
            if prev_2_size == prev_size == curr_size:
                print("")
                print("")
                print("BUY Now "+index_name, flush=True)
                winsound.PlaySound(sound, winsound.SND_FILENAME)
                flag = False

def is_within_time_range():
    current_time = datetime.now().time()  # Get the current time
    start_time = time(9, 0)  # 9:00 AM
    end_time = time(23, 0)   # 4:00 PM
    return start_time <= current_time <= end_time

def run_main_script():
    while True:
        # Check if current time is between 9 AM and 4 PM
        if not is_within_time_range():
            print("Script paused: outside of allowed time range (9 AM to 4 PM).", flush=True)
            t.sleep(600)  # Sleep for 10 minutes before checking again
            continue

        try:
            # Run the main.py script and capture the output
            result = subprocess.run(["python", "scripts/main.py"], capture_output=True, text=True)
            
            calculated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            lines = result.stdout.splitlines()

            for line in lines:
                if "Nifty OI Difference" in line:
                    parts = line.split(":")
                    nifty_diff = int(parts[1].split(",")[0].strip())
                    banknifty_diff = int(parts[2].strip())

                    temp_nifty_diffs.append(f"{nifty_diff}")
                    nifty_diffs.append(f"{calculated_time}# {nifty_diff}")

                    if len(temp_nifty_diffs) >= 3:
                        previous_2_value = temp_nifty_diffs[-3]
                        previous_value = temp_nifty_diffs[-2]
                        current_value = temp_nifty_diffs[-1]
                        index_name = "Nifty"
                        check_and_beep(index_name, previous_2_value, previous_value, current_value)

                    temp_banknifty_diffs.append(f"{banknifty_diff}")
                    banknifty_diffs.append(f"{calculated_time}# {banknifty_diff}")

                    if len(temp_banknifty_diffs) >= 3:
                        previous_2_value = temp_banknifty_diffs[-3]
                        previous_value = temp_banknifty_diffs[-2]
                        current_value = temp_banknifty_diffs[-1]
                        index_name = "Bank Nifty"
                        check_and_beep(index_name, previous_2_value, previous_value, current_value)

            print("\nNifty OI Differences:", flush=True)
            for item in nifty_diffs:
                print(item, flush=True)

            print("\nBank Nifty OI Differences:", flush=True)
            for item in banknifty_diffs:
                print(item, flush=True)

            t.sleep(10)  # Sleep for 3 minutes before running again
        
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("Nifty OI Differences:", nifty_diffs, flush=True)
        print("Bank Nifty OI Differences:", banknifty_diffs, flush=True)
