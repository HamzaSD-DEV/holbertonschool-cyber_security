#!/bin/bash
TECHNIQUE_ID="T1087.001"
TECHNIQUE_NAME="Local Account Discovery"
RESULTS_FILE="atomic_results.txt"
LOG_FILE="atomic_log.txt"
STOP_FLAG="stop_test.flag"

# Check for stop flag before doing anything
if [ -f "$STOP_FLAG" ]; then
    echo "[!] stop_test.flag detected. Aborting simulation."
    echo "[!] Remove the flag file to allow execution."
    exit 1
fi

# Print technique info
echo "[*] MITRE ATT&CK Techniqe: $TECHNIQUE_ID - $TECHNIQUE_NAME"

# Log start time
START_TIME=$(date "+%Y-%m-%d %H:%M:%S")
echo "[*] Start time: $START_TIME"
echo "[$START_TIME] START - $TECHNIQUE_ID - $TECHNIQUE_NAME" >> "$LOG_FILE"

# Run simulation
echo "[*] Running simulation..."
cat /etc/passwd > "$RESULTS_FILE"

# Log end time
echo "[*] Output saved to $RESULTS_FILE"
END_TIME=$(date "+%Y-%m-%d %H:%M:%S")
echo "[*] End time: $END_TIME"
echo "[$END_TIME] END   - $TECHNIQUE_ID - $TECHNIQUE_NAME" >> "$LOG_FILE"

echo "[*] Simulation complete. Review $LOG_FILE for details."