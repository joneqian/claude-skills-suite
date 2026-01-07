#!/bin/bash
# Skill Seeker MCP Server - Start Script
# This script starts the MCP HTTP server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.mcp-server.pid"
PORT_FILE="$SCRIPT_DIR/.mcp-server.port"
LOG_FILE="$SCRIPT_DIR/.mcp-server.log"

# Default port
HTTP_PORT=3000

echo "=========================================================="
echo "Skill Seeker MCP Server - Start"
echo "=========================================================="
echo ""

# Parse arguments
FOREGROUND=false
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            HTTP_PORT="$2"
            shift 2
            ;;
        -f|--foreground)
            FOREGROUND=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -p, --port PORT    Set HTTP server port (default: 3000)"
            echo "  -f, --foreground   Run in foreground (default: background)"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                 # Start on port 3000 in background"
            echo "  $0 -p 8080         # Start on port 8080 in background"
            echo "  $0 -f              # Start in foreground (Ctrl+C to stop)"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use -h for help"
            exit 1
            ;;
    esac
done

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        OLD_PORT=$(cat "$PORT_FILE" 2>/dev/null || echo "unknown")
        echo -e "${YELLOW}⚠${NC} Server already running"
        echo "  PID: $OLD_PID"
        echo "  Port: $OLD_PORT"
        echo ""
        read -p "Stop existing server and start new one? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Stopping existing server..."
            kill "$OLD_PID" 2>/dev/null
            sleep 1
            rm -f "$PID_FILE" "$PORT_FILE"
        else
            echo "Keeping existing server running"
            exit 0
        fi
    else
        # PID file exists but process not running, cleanup
        rm -f "$PID_FILE" "$PORT_FILE"
    fi
fi

# Check if port is available
if lsof -i ":$HTTP_PORT" > /dev/null 2>&1; then
    echo -e "${RED}✗${NC} Port $HTTP_PORT is already in use"
    echo ""
    echo "Check what's using it:"
    echo -e "  ${CYAN}lsof -i :$HTTP_PORT${NC}"
    echo ""
    echo "Use a different port:"
    echo -e "  ${CYAN}$0 -p 8080${NC}"
    exit 1
fi

# Check Python and dependencies
if ! python3 -c "import skill_seekers.mcp.server_fastmcp" 2>/dev/null; then
    echo -e "${RED}✗${NC} skill_seekers module not found"
    echo ""
    echo "Please run the setup script first:"
    echo -e "  ${CYAN}./skill_seeker_setup_mcp.sh${NC}"
    exit 1
fi

echo "Starting MCP HTTP server..."
echo "  Port: $HTTP_PORT"
echo "  Log: $LOG_FILE"
echo ""

if [ "$FOREGROUND" = true ]; then
    echo -e "${CYAN}Running in foreground mode (Ctrl+C to stop)${NC}"
    echo ""
    
    # Save PID and port before starting (for consistency)
    echo "$$" > "$PID_FILE"
    echo "$HTTP_PORT" > "$PORT_FILE"
    
    # Cleanup on exit
    trap "rm -f '$PID_FILE' '$PORT_FILE'; echo ''; echo 'Server stopped'" EXIT
    
    # Run in foreground
    cd "$SCRIPT_DIR"
    python3 -m skill_seekers.mcp.server_fastmcp --http --port $HTTP_PORT
else
    # Start server in background
    cd "$SCRIPT_DIR"
    nohup python3 -m skill_seekers.mcp.server_fastmcp --http --port $HTTP_PORT > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!

    # Save PID and port
    echo "$SERVER_PID" > "$PID_FILE"
    echo "$HTTP_PORT" > "$PORT_FILE"

    sleep 2

    # Check if server started
    if curl -s http://127.0.0.1:$HTTP_PORT/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} MCP server started successfully"
        echo ""
        echo "  PID: $SERVER_PID"
        echo "  Health check: http://127.0.0.1:$HTTP_PORT/health"
        echo "  SSE endpoint: http://127.0.0.1:$HTTP_PORT/sse"
        echo ""
        echo "To stop the server:"
        echo -e "  ${CYAN}./skill_seeker_stop_mcp.sh${NC}"
        echo ""
        echo "To view logs:"
        echo -e "  ${CYAN}tail -f $LOG_FILE${NC}"
    else
        echo -e "${RED}✗${NC} Failed to start server"
        echo ""
        echo "Check logs for errors:"
        echo -e "  ${CYAN}cat $LOG_FILE${NC}"
        
        # Cleanup
        rm -f "$PID_FILE" "$PORT_FILE"
        exit 1
    fi
fi
