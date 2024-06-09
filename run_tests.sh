#!/bin/sh
# Start the Flask app in the background
python3 main.py &

# Wait a bit for the Flask server to start
sleep 5

# Run unittest
python3 -m pytest test_app.py