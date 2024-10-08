# Author:  Adge Denkers
# Created: 2024-07-23
# Updated: 2024-07-23
# File:    keep_awake.py
# Version: 1.1

import argparse
import ctypes
import datetime
import time

from ctypes import wintypes

# Set debug flag to False initially
debug = False

# Define the idle time limit in seconds
IDLE_TIME_LIMIT = 150   # De-idle the machine when idle time hits 2-1/2 minutes (in seconds)

# Define a ctypes Structure for retrieving the last input time information
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

# Function to get the idle time of the system in seconds
def get_idle_time():
    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info)):
        millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
        return millis / 1000.0
    else:
        raise ctypes.WinError()

# Function to simulate user activity by pressing the Shift key
def simulate_activity():
    if debug:
        print(datetime.datetime.now(), "|", "starting to simulate activity")
    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)  # Press Shift
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)  # Release Shift
    print(datetime.datetime.now(), "-", "Keeping Awake")
    if debug:
        print(datetime.datetime.now(), "|", "simulated pressing the `Shift` key")

# Function to check if the current time is within the specified active time range
def is_within_active_time(start_time: datetime.time, end_time: datetime.time) -> bool:
    """Check if the current time is within the range [start_time, end_time].

    Args:
        start_time (datetime.time): Start of the active period.
        end_time (datetime.time): End of the active period.

    Returns:
        bool: True if current time is within the range, False otherwise.
    """
    now = datetime.datetime.now().time()
    # Handle cases where the end time is past midnight (e.g., 7:00 PM to 2:00 AM)
    if start_time < end_time:
        return start_time <= now <= end_time
    else:
        return now >= start_time or now <= end_time

# Main function to control the program flow
def main(debug, start_hour, start_minute, end_hour, end_minute):
    print(datetime.datetime.now(), "|", "Starting Keep Awake Protocol")

    # Define the start and end times based on user input
    start_time = datetime.time(start_hour, start_minute)
    end_time = datetime.time(end_hour, end_minute)

    while True:
        # Check the idle time
        idle_time = get_idle_time()
        if debug:
            print(datetime.datetime.now(), "|", "checking idle time...", idle_time)
        
        # Only simulate activity if current time is within active hours
        if is_within_active_time(start_time, end_time):
            if idle_time >= IDLE_TIME_LIMIT:
                print(datetime.datetime.now(), "|", "simulating activity")
                simulate_activity()
                print('---')
        else:
            print(datetime.datetime.now(), "|", "Outside active time, not keeping awake.")
        
        # Sleep for 10 seconds before checking again
        time.sleep(10)

# Entry point of the script
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Prevent the protocol from locking")
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--start_hour', type=int, default=7, help="Hour to start keeping awake (24-hour format, default is 7)")
    parser.add_argument('--start_minute', type=int, default=0, help="Minute to start keeping awake (default is 0)")
    parser.add_argument('--end_hour', type=int, default=16, help="Hour to stop keeping awake (24-hour format, default is 16)")
    parser.add_argument('--end_minute', type=int, default=30, help="Minute to stop keeping awake (default is 30)")
    args = parser.parse_args()
    
    # Call the main function with the debug flag and time range
    main(args.debug, args.start_hour, args.start_minute, args.end_hour, args.end_minute)


# python keep_awake.py --start_hour 7 --start_minute 0 --end_hour 16 --end_minute 30
