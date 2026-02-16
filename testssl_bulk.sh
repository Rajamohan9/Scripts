#!/bin/bash

### CONFIG
TARGET_FILE="$HOME/testssl/domains.txt"
REPORT_DIR="$HOME/testssl/reports"
LOG_DIR="$HOME/testssl/logs"
SCREENSHOT_DIR="$HOME/testssl/screenshots"
TESTSSL_BIN="testssl"

echo "[*] Starting Pre-checks..."

# Ensure folders exist
mkdir -p "$REPORT_DIR" "$LOG_DIR" "$SCREENSHOT_DIR"

# Check testssl
if ! command -v "$TESTSSL_BIN" >/dev/null 2>&1; then
  echo "[!] testssl not found. Installing..."
  sudo apt update && sudo apt install -y git
  if [ ! -d "/opt/testssl.sh" ]; then
    sudo git clone https://github.com/drwetter/testssl.sh.git /opt/testssl.sh
  else
    cd /opt/testssl.sh && sudo git pull && cd - >/dev/null
  fi
  sudo ln -sf /opt/testssl.sh/testssl.sh /usr/local/bin/testssl
fi

# Check scrot
if ! command -v scrot >/dev/null 2>&1; then
  echo "[!] scrot not found. Installing..."
  sudo apt update && sudo apt install -y scrot
fi

# Validate target file
if [ ! -f "$TARGET_FILE" ]; then
  echo "[!] Target file not found: $TARGET_FILE"
  echo "    Create it using:"
  echo "    cat << 'EOF' > $TARGET_FILE"
  exit 1
fi

echo "[✓] Pre-checks completed"
echo "----------------------------------------------"

i=1

while read -r domain; do
  [ -z "$domain" ] && continue

  ts=$(date +%Y%m%d_%H%M%S)
  clean=$(echo "$domain" | sed 's/[^a-zA-Z0-9]/_/g')

  echo "=============================================="
  echo "[+] [$i] Scanning: $domain"
  echo "Timestamp: $ts"
  echo "=============================================="

  # Start screenshot capture every 5 seconds
  (
    j=1
    while true; do
      sleep 10
      scrot "$SCREENSHOT_DIR/${i}_${clean}_${ts}_shot${j}.png" 2>/dev/null
      j=$((j+1))
    done
  ) &
  SCREEN_PID=$!

  # Run testssl
  "$TESTSSL_BIN" --htmlfile "$REPORT_DIR/${i}_${clean}_${ts}.html" "$domain" \
    | tee "$LOG_DIR/${i}_${clean}_${ts}.txt"

  # Stop screenshot capture when scan finishes
  kill "$SCREEN_PID" 2>/dev/null

  echo "[✓] [$i] Completed: $domain"
  echo "----------------------------------------------"

  i=$((i+1))
  sleep 2
done < "$TARGET_FILE"

echo "[✓] All scans completed successfully"
