#!/bin/bash

cleanup() {
    echo ""
    echo "Shutting down servers..."
    # Kill the background process group
    kill $(jobs -p)
    exit
}

trap cleanup SIGINT

echo "Starting backend servers..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

echo "Starting frontend servers..."
cd frontend
npm run build