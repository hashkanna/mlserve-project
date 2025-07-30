#!/bin/bash
# MLServe Demo Launcher Script

echo "🚀 MLServe Interview Demo Launcher"
echo "=================================="
echo

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "Please activate your virtual environment first:"
    echo "source venv/bin/activate  # or source .venv/bin/activate"
    echo
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Check if API is already running
if check_port 8000; then
    echo "✅ API already running on port 8000"
    API_RUNNING=true
else
    echo "🔄 Starting MLServe API..."
    API_RUNNING=false
fi

# Check if UI server is already running
if check_port 3000; then
    echo "✅ UI Server already running on port 3000"
    UI_RUNNING=true
else
    echo "🔄 Starting UI Server..."
    UI_RUNNING=false
fi

echo
echo "📋 Demo URLs:"
echo "  🖥️  MLServe UI:     http://localhost:3000"
echo "  🔌 API Endpoints:  http://localhost:8000/api/v1/docs"
echo "  📊 Ray Dashboard:  http://localhost:8265"
echo

# Start API if not running
if [ "$API_RUNNING" = false ]; then
    echo "Starting MLServe API in background..."
    python main.py > api.log 2>&1 &
    API_PID=$!
    echo "API PID: $API_PID"
    
    # Wait for API to start
    echo "Waiting for API to start..."
    for i in {1..30}; do
        if check_port 8000; then
            echo "✅ API started successfully!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ API failed to start. Check api.log for details."
            exit 1
        fi
        sleep 1
        echo -n "."
    done
    echo
fi

# Start UI server if not running
if [ "$UI_RUNNING" = false ]; then
    echo "Starting UI Server in background..."
    python serve_ui.py > ui.log 2>&1 &
    UI_PID=$!
    echo "UI Server PID: $UI_PID"
    
    # Wait for UI server to start
    echo "Waiting for UI Server to start..."
    for i in {1..10}; do
        if check_port 3000; then
            echo "✅ UI Server started successfully!"
            break
        fi
        if [ $i -eq 10 ]; then
            echo "❌ UI Server failed to start. Check ui.log for details."
            exit 1
        fi
        sleep 1
        echo -n "."
    done
    echo
fi

echo "🎉 Demo is ready!"
echo
echo "🎯 Interview Demo Guide:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Show image classification with sample images"
echo "3. Demonstrate load testing and autoscaling"
echo "4. Reference Ray Dashboard at http://localhost:8265"
echo "5. Show API docs at http://localhost:8000/api/v1/docs"
echo
echo "📝 Demo Script:"
echo "  python demo_interview.py  # Run command-line demo"
echo
echo "🛑 To stop all services:"
echo "  Press Ctrl+C or run: ./stop_demo.sh"
echo

# Open browser
if command -v open &> /dev/null; then
    echo "🌐 Opening browser..."
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    echo "🌐 Opening browser..."
    xdg-open http://localhost:3000
fi

# Keep script running and handle cleanup
cleanup() {
    echo
    echo "🧹 Cleaning up..."
    if [ ! -z "$API_PID" ]; then
        echo "Stopping API (PID: $API_PID)..."
        kill $API_PID 2>/dev/null
    fi
    if [ ! -z "$UI_PID" ]; then
        echo "Stopping UI Server (PID: $UI_PID)..."
        kill $UI_PID 2>/dev/null
    fi
    echo "Demo stopped. Thanks for using MLServe! 🚀"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Press Ctrl+C to stop all services..."
wait