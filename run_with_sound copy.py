import time
#import datetime
import subprocess
from datetime import datetime
#from datetime import datetime, time  # Importing datetime and time separately
import winsound

# Move arrays to the outer scope
nifty_diffs = []
banknifty_diffs = []

temp_nifty_diffs = []
temp_banknifty_diffs = []

def check_and_beep(index_name, previous_2_value, previous_value, current_value):
    # Calculate the difference between the values
#    print(int(current_value) , int(previous_value))
    difference = abs(int(current_value) - int(previous_value))

    sound = r"C:\Windows\Media\Ring08.wav" 

    prev_2_size = len(str(previous_2_value))
    prev_size = len(str(previous_value))
    curr_size = len(str(current_value))
    
    print("")
    print("")
    print("")
    print("")

#    print("difference # ", difference)
    flag = False

    if difference > 100000:
        # Sound for 1 time
        winsound.PlaySound(sound, winsound.SND_FILENAME)
        flag = False

    if previous_2_value == previous_value == current_value:
        # Sound for 1 time
        if difference == 0:
            print("Get Ready .... ")
            winsound.PlaySound(sound, winsound.SND_FILENAME)
            flag = False


    if abs(prev_size - curr_size) >= 1: # type: ignore
        flag = True
        #print (index_name+" # "+"prev_size # "+str(prev_size)+" curr_size # "+str(curr_size))

        if int(curr_size) > int(prev_size):
            print("Get Ready for PE BUY")
            # Beep for 10 seconds
            end_time = time.time() + 10
            while time.time() < end_time:
                winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 second

        if int(curr_size) < int(prev_size):
            print("Get Ready for CE BUY")
            # Beep for 10 seconds
            end_time = time.time() + 10
            while time.time() < end_time:
                winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 second

        if flag == True:
            if prev_2_size == prev_size == curr_size:
                print("BUY Now")
                winsound.PlaySound(sound, winsound.SND_FILENAME)
                flag = False

        print("")


def run_main_script():
    '''
        current_time = datetime.now().time()  # Get the current time using datetime directly
        start_time = time(9, 0)  # 9:00 AM
        end_time = time(23, 0)   # 11:00 PM
        return start_time <= current_time <= end_time
    '''
    while True:

        try:

            # Run the main.py script and capture the output
            result = subprocess.run(["python", "scripts/main.py"], capture_output=True, text=True)
            
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
                    temp_nifty_diffs.append(f"{nifty_diff}")
                    nifty_diffs.append(f"{calculated_time}# {nifty_diff}")

                    # append beep functionality if last two values of nifty_diffs array has a difference more than 50000 
                    if len(temp_nifty_diffs) >= 3:
                        previous_2_value = temp_nifty_diffs[-3]
                        previous_value = temp_nifty_diffs[-2]
                        current_value = temp_nifty_diffs[-1]
                        index_name = "Nifty"
                        check_and_beep(index_name, previous_2_value, previous_value, current_value)

                    temp_banknifty_diffs.append(f"{banknifty_diff}")
                    banknifty_diffs.append(f"{calculated_time}# {banknifty_diff}")

                    # append beep functionality if last two values of banknifty_diffs array has a difference more than 50000 
                    if len(temp_banknifty_diffs) >= 3:
                        previous_2_value = temp_banknifty_diffs[-3]
                        previous_value = temp_banknifty_diffs[-2]
                        current_value = temp_banknifty_diffs[-1]
                        index_name = "Bank Nifty"
                        check_and_beep(index_name, previous_2_value, previous_value, current_value)

            # Print the current arrays
            print("\nNifty OI Differences:")
            for item in nifty_diffs:
                print(item, flush=True)

            print("\nBank Nifty OI Differences:")
            for item in banknifty_diffs:
                print(item, flush=True)

            # Wait for 5 seconds before running the script again
#            time.sleep(300)
            time.sleep(180) # 180
        
        except Exception as e:
            print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    try:
        run_main_script()
    except KeyboardInterrupt:
        print("\nExecution interrupted. Printing stored OI differences:", flush=True)
        print("Nifty OI Differences:", nifty_diffs, flush=True)
        print("Bank Nifty OI Differences:", banknifty_diffs, flush=True)
