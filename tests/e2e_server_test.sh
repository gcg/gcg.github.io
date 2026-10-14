#!/bin/bash
set -e

# Find available port or use 8000
PORT=8000

# Start local server in background
python3 -m http.server $PORT &
PID=$!

# Ensure cleanup on exit
trap "kill -9 $PID 2>/dev/null || true" EXIT

sleep 2

# Verify HTTP 200 and expected payload
curl -s -I "http://localhost:${PORT}" | grep -q "200 OK" || { echo "Failed HTTP 200"; exit 1; }
curl -s "http://localhost:${PORT}" | grep -q "Solo Leveling" || { echo "Missing page content"; exit 1; }
curl -s "http://localhost:${PORT}" | grep -q "Guney Can Gokoglu" || { echo "Missing name in page"; exit 1; }
curl -s "http://localhost:${PORT}/assets/img/gcg.jpg" -I | grep -q "200 OK" || { echo "Missing gcg.jpg"; exit 1; }
curl -s "http://localhost:${PORT}/assets/css/style.css" -I | grep -q "200 OK" || { echo "Missing style.css"; exit 1; }
curl -s "http://localhost:${PORT}/assets/js/rotating-id.js" -I | grep -q "200 OK" || { echo "Missing rotating-id.js"; exit 1; }

echo "E2E server test passed!"
