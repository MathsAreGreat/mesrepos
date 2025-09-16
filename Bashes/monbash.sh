#!/bin/bash

# Exit on any error
set -e

# --- Configuration ---
WORK_DIR="/home/mohamed/Documents/Projects/Python/Jobs"
LOGS_PATH="/home/mohamed/Documents/Stuff"
LOCK_FILE="/tmp/backup_cron.lock"
SUMMARY_LOG="$LOGS_PATH/summary.log"

# --- Setup and Pre-checks ---

# Ensure log directory exists
mkdir -p "$LOGS_PATH"

# Setup trap to remove the lock file on exit (even on errors)
trap 'rm -f "$LOCK_FILE"' EXIT

# Prevent concurrent runs
if [ -f "$LOCK_FILE" ]; then
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Script already running. Exiting." | tee -a "$SUMMARY_LOG"
    exit 1
fi
touch "$LOCK_FILE"

# Check for 'bc' utility
if ! command -v bc >/dev/null; then
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Error: 'bc' utility not found. Please install it." | tee -a "$SUMMARY_LOG" >&2
    exit 1
fi

# Activate Python virtual environment
# It's generally better to use the full path to the activate script
# and to source it to affect the current shell.
source "/home/mohamed/moha13/bin/activate"

# Change to working directory
cd "$WORK_DIR" || {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Error: Failed to change to $WORK_DIR. Exiting." | tee -a "$SUMMARY_LOG" >&2
    exit 1
}

# --- Script Execution ---

# Array of script filenames only (without python path)
scripts=(
    "backup.py"
    "check.py"
    "save.py"
    "salat.py"
    "dwn_manager.py"
    "save_insta_kays.py"
)

# Clear summary log at start (or append with a separator)
# Using '>' will clear it each time. If you want to keep historical runs, use '>>' with a separator.
: > "$SUMMARY_LOG" # Clears the file

echo "$(date +'%Y-%m-%d %H:%M:%S') - Starting script execution loop." >> "$SUMMARY_LOG"
echo "---" >> "$SUMMARY_LOG"

while true; do
    echo "" > "$SUMMARY_LOG"
    for script in "${scripts[@]}"; do
        command_to_run="uv run $script"
        script_name=$(basename "$script" .py)
        log_file="$LOGS_PATH/$script_name.log"

        echo "$(date +'%Y-%m-%d %H:%M:%S') - Running '$script'..." | tee -a "$SUMMARY_LOG" # Log to console and summary

        start_time=$(date +%s.%N)

        # Execute the command, redirecting stdout and stderr to the specific log file
        if eval "$command_to_run" > "$log_file" 2>&1; then # Appends output to log_file
            end_time=$(date +%s.%N)
            execution_time=$(bc -l <<< "$end_time - $start_time")
            echo "$(date +'%Y-%m-%d %H:%M:%S') - Command '$command_to_run' completed successfully." | tee -a "$SUMMARY_LOG"
            echo "Command took $execution_time seconds" > "$log_file" # Add execution time to specific log
            echo "---" >> "$SUMMARY_LOG" # Separator for summary log
        else
            end_time=$(date +%s.%N)
            execution_time=$(bc -l <<< "$end_time - $start_time")
            echo "$(date +'%Y-%m-%d %H:%M:%S') - ERROR: Command '$command_to_run' failed. See '$log_file' for details." | tee -a "$SUMMARY_LOG" >&2
            echo "Command took $execution_time seconds (failed)" > "$log_file" # Add execution time to specific log
            echo "---" >> "$SUMMARY_LOG" # Separator for summary log
        fi

        # Small delay between script runs
        sleep 0.5
    done
    echo "$(date +'%Y-%m-%d %H:%M:%S') - All scripts in the list have been run once. Restarting loop." >> "$SUMMARY_LOG"
    echo "========================================" >> "$SUMMARY_LOG" # Clearer separator for loop cycles
done