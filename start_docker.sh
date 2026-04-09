#!/bin/bash
PROJECT_ROOT="/app"

echo "📡 Initializing Enterprise Microservices in Docker..."

# Cleanup trap
cleanup() {
    echo "🛑 Shutting down container services..."
    kill $(jobs -p) 2>/dev/null
    rm -f "$PROJECT_ROOT/python_ai/cluster_"*.wav "$PROJECT_ROOT/python_ai/splicer_log.txt" 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM EXIT

# Start Go Gateway
echo "🚀 Starting Go Orchestrator..."
cd "$PROJECT_ROOT/go_gateway" || exit
./main & 

sleep 2

# Start Dashboard (No venv needed in Docker)
echo "📊 Booting Streamlit Interface..."
cd "$PROJECT_ROOT" || exit
streamlit run dashboard.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false