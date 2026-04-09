#!/bin/bash

# 0. The Anchor: Find the exact folder this script lives in automatically
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "📡 Initializing Enterprise Microservices at $PROJECT_ROOT..."

# 1. Improved Cleanup
cleanup() {
    echo "🛑 Shutting down services..."
    kill $(jobs -p) 2>/dev/null
    rm -f "$PROJECT_ROOT/python_ai/cluster_"*.wav "$PROJECT_ROOT/python_ai/splicer_log.txt" 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

# 2. Port Guard
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    kill -9 $(lsof -t -i:8080) 2>/dev/null
fi

# 3. Start Go Gateway
echo "🚀 Starting Go Orchestrator..."
cd "$PROJECT_ROOT/go_gateway" || exit
go build -o main main.go && ./main & 

sleep 2

# 4. Start Dashboard
echo "📊 Booting Streamlit Interface..."
cd "$PROJECT_ROOT" || exit
source "$PROJECT_ROOT/python_ai/venv/bin/activate"
streamlit run dashboard.py --server.port 8501