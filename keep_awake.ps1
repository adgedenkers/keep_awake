# Author:  Adge Denkers
# Created: 2024-09-17
# Updated: 2024-10-07
# File:    keep_awake.ps1
# Version: 1.2

# Description:
# This PowerShell script will run the keep_awake python application
# using the start and end hours saved as environment variables.
# The PowerShell window will start minimized, and the script will
# run with Administrator privileges.

# Retrieve start and end times from environment variables
$start_hour = $env:KEEP_AWAKE_START_HOUR
$start_minute = $env:KEEP_AWAKE_START_MINUTE
$end_hour = $env:KEEP_AWAKE_END_HOUR
$end_minute = $env:KEEP_AWAKE_END_MINUTE

# Ensure default values are set in case the variables are empty
if (-not $start_hour) { $start_hour = 7 }
if (-not $start_minute) { $start_minute = 0 }
if (-not $end_hour) { $end_hour = 16 }
if (-not $end_minute) { $end_minute = 30 }

# Define the script block to run the python application
$scriptBlock = {
    Set-Location $env:KEEPAWAKE_DIR
    . ".\venv\Scripts\Activate.ps1"
    python main.py --start_hour $using:start_hour --start_minute $using:start_minute --end_hour $using:end_hour --end_minute $using:end_minute
}

# Define the start info for the new minimized process
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "powershell.exe"
$startInfo.Arguments = "-NoExit -Command $([ScriptBlock]::Create($scriptBlock))"
$startInfo.Verb = "runas"  # Run the process with Administrator privileges
$startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Minimized  # Start minimized

# Start the process
[System.Diagnostics.Process]::Start($startInfo)
