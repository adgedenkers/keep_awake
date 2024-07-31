# Author:  Adge Denkers
# Created: 2024-07-23
# Updated: 2024-07-23
# File:    keep_awake.py
# Version: 1.0

# Importing necessary libraries
import argparse    # For parsing command-line arguments
import ctypes      # For interacting with low-level C functions
import datetime    # For handling dates and times
import time        # For sleeping and managing time intervals

from ctypes import wintypes   # For defining Windows data types used in ctypes

# Set debug flag to False initially
debug = False

# Define the idle time limit in seconds
IDLE_TIME_LIMIT = 150   # De-idle the machine when idle time hits 2-1/2 minutes (in seconds)
#IDLE_TIME_LIMIT = 30   # De-idle the machine when idle time hits 30 seconds (uncomment for testing)

# Define a ctypes Structure for retrieving the last input time information
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

# Function to get the idle time of the system in seconds
def get_idle_time():
    last_input_info = LASTINPUTINFO()  # Create an instance of LASTINPUTINFO
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)  # Set the size of the structure
    # Call the Windows API function GetLastInputInfo to fill the structure
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info)):
        # Calculate the idle time in milliseconds and convert to seconds
        millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
        return millis / 1000.0
    else:
        # Raise an error if the API call fails
        raise ctypes.WinError()

# Function to simulate user activity by pressing the Shift key
def simulate_activity():
    if debug:
        print(datetime.datetime.now(), "|", "starting to simulate activity")
    # Simulate a key press of the Shift key (key code 0x10)
    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)
    time.sleep(0.05)  # Small delay to ensure the key press is registered
    # Simulate a key release of the Shift key
    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)
    print(datetime.datetime.now(), "-", "Keeping Awake")
    if debug:
        print(datetime.datetime.now(), "|", "simulated pressing the `Shift` key")

# Main function to control the program flow
def main(debug):
    print(datetime.datetime.now(), "|", "Starting Keep Awake Protocol")
    while True:
        # Check the idle time
        idle_time = get_idle_time()
        if debug:
            print(datetime.datetime.now(), "|", "checking idle time...", idle_time)
        # If the idle time exceeds the limit, simulate activity
        if idle_time >= IDLE_TIME_LIMIT:
            print(datetime.datetime.now(), "|", "simulating activity")
            simulate_activity()
            print('---')
        # Sleep for 10 seconds before checking again
        time.sleep(10)

# Entry point of the script
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Prevent the protocol from locking")
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    # Call the main function with the debug flag
    main(args.debug)
