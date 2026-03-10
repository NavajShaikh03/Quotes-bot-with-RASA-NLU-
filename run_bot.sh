#!/bin/bash

echo "============================================"
echo "Quotes Bot with RASA NLU - Starting..."
echo "============================================"

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Please create one:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "Step 1: Training RASA model..."
echo "============================================"
rasa train

echo ""
echo "Step 2: Starting RASA Action Server..."
echo "============================================"
rasa run actions --port 5055 &
ACTION_PID=$!

echo "Waiting for action server to initialize..."
sleep 3

echo ""
echo "Step 3: Starting RASA API server..."
echo "============================================"
rasa run --enable-api --cors "*" --port 5005 &
RASA_PID=$!

echo "Waiting for Rasa server to initialize..."
sleep 5

echo ""
echo "Step 4: Starting Web UI server..."
echo "============================================"
python web_integration/chat_ui.py &
WEB_PID=$!

echo "Waiting for web server to initialize..."
sleep 3

echo ""
echo "Step 5: Opening chatbot UI in browser..."
echo "============================================"
python -m webbrowser "http://localhost:5500"

echo ""
echo "============================================"
echo "Bot is ready! All servers started."
echo "============================================"
echo "Training: Complete"
echo "Action Server: http://localhost:5055"
echo "API Server: http://localhost:5005"
echo "Web UI: http://localhost:5500"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "============================================"

# Wait for all background processes
trap "kill $ACTION_PID $RASA_PID $WEB_PID 2>/dev/null; exit" INT TERM

wait
