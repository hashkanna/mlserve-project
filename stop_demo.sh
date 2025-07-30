#!/bin/bash
# MLServe Demo Stop Script

echo "🛑 Stopping MLServe Demo Services..."
echo

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local service=$2
    
    local pids=$(lsof -ti:$port)
    if [ ! -z "$pids" ]; then
        echo "🔴 Stopping $service on port $port..."
        echo "$pids" | xargs kill -TERM 2>/dev/null
        sleep 2
        
        # Force kill if still running
        local remaining=$(lsof -ti:$port)
        if [ ! -z "$remaining" ]; then
            echo "   Force killing remaining processes..."
            echo "$remaining" | xargs kill -KILL 2>/dev/null
        fi
        echo "   ✅ $service stopped"
    else
        echo "   ℹ️  $service not running on port $port"
    fi
}

# Stop UI Server (port 3000)
kill_port 3000 "UI Server"

# Stop MLServe API (port 8000)
kill_port 8000 "MLServe API"

# Stop Ray Serve if running
echo "🔴 Stopping Ray Serve..."
if command -v ray &> /dev/null; then
    ray stop 2>/dev/null
    echo "   ✅ Ray stopped"
else
    echo "   ℹ️  Ray command not found"
fi

# Clean up log files
if [ -f "api.log" ]; then
    rm api.log
    echo "   🧹 Cleaned up api.log"
fi

if [ -f "ui.log" ]; then
    rm ui.log
    echo "   🧹 Cleaned up ui.log"
fi

echo
echo "🎉 All services stopped successfully!"
echo "   You can now restart with: ./start_demo.sh"