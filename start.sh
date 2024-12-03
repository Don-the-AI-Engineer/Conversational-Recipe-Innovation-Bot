#!/bin/bash

echo "Starting Backend..."
cd backend
uvicorn main:app --reload &
BACKEND_PID=$!

echo "Starting Frontend..."
cd ../frontend
streamlit run app.py &
FRONTEND_PID=$!

# Stop services gracefully on exit
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait