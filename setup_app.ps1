# Author:  Adge Denkers
# Created: 2024-09-23
# Updated: 2024-10-07
# File:    setup_app.ps1
# Version: 1.2

# Description: This PowerShell script sets up your local environment
# for `keep_awake`, creates a folder structure for the `keep_awake`
# application, and allows setting start and end times for the application.

# Ask user for the directory to create the `keep_awake` folder - the default is C:\src\
$dir = Read-Host "Enter the directory to create the 'keep_awake' folder (default: C:\src\)"
if (-not $dir) {
    $dir = "C:\src\"
}

# Set the directory plus the folder `keep_awake` as an environment variable
$env:KEEPAWAKE_DIR = $dir + "\keep_awake"
$app_dir = $env:KEEPAWAKE_DIR

# Create the parent directory if it doesn't exist
if (-not (Test-Path $app_dir)) {
    New-Item -ItemType Directory -Path $app_dir
}

# Clone the `keep_awake` repository from GitHub
git clone https://github.com/adgedenkers/keep_awake.git $app_dir

# Create a virtual environment for the `keep_awake` application
cd $app_dir
python -m venv .venv

# Install the required packages for the `keep_awake` application
.venv\Scripts\Activate.ps1

# Update pip
python -m pip install --upgrade pip

# Install the required packages for the `keep_awake` application
pip install -r requirements.txt

# Ask the user to provide start and end times for the application
$start_hour = Read-Host "Enter the start hour (default: 7)"
if (-not $start_hour) {
    $start_hour = 7
}

$start_minute = Read-Host "Enter the start minute (default: 0)"
if (-not $start_minute) {
    $start_minute = 0
}

$end_hour = Read-Host "Enter the end hour (default: 16)"
if (-not $end_hour) {
    $end_hour = 16
}

$end_minute = Read-Host "Enter the end minute (default: 30)"
if (-not $end_minute) {
    $end_minute = 30
}

# Save the user-provided times as environment variables
[Environment]::SetEnvironmentVariable("KEEP_AWAKE_START_HOUR", $start_hour, [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("KEEP_AWAKE_START_MINUTE", $start_minute, [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("KEEP_AWAKE_END_HOUR", $end_hour, [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("KEEP_AWAKE_END_MINUTE", $end_minute, [EnvironmentVariableTarget]::User)

Write-Host "The start and end times have been saved as environment variables:"

Write-Host "KEEP_AWAKE_START_HOUR = $start_hour"
Write-Host "KEEP_AWAKE_START_MINUTE = $start_minute"
Write-Host "KEEP_AWAKE_END_HOUR = $end_hour"
Write-Host "KEEP_AWAKE_END_MINUTE = $end_minute"

# Set the directory as the current location
Set-Location $app_dir

# Run the `keep_awake` application with the user-defined start and end times
python main.py --start_hour $start_hour --start_minute $start_minute --end_hour $end_hour --end_minute $end_minute --debug

# End of script
