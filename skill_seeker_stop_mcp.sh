#!/bin/bash
# Skill Seeker MCP Server - Stop Script
# This script stops the running MCP HTTP server

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory (where the PID file should be)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.mcp-server.pid"
PORT_FILE="$SCRIPT_DIR/.mcp-server.port"
LOG_FILE="$SCRIPT_DIR/.mcp-server.log"

echo "=========================================================="
echo "Skill Seeker MCP Server - Stop"
echo "=========================================================="
echo ""

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠${NC} PID file not found: $PID_FILE"
    echo ""
    echo "Server may not be running, or was started manually."
    echo ""
    echo "Try finding the process manually:"
    echo -e "  ${CYAN}ps aux | grep skill_seekers${NC}"
    echo -e "  ${CYAN}pgrep -f 'skill_seekers.mcp.server_fastmcp'${NC}"
    echo ""
    
    # Try to find and kill anyway
    FOUND_PID=$(pgrep -f "skill_seekers.mcp.server_fastmcp" 2>/dev/null | head -1)
    if [ -n "$FOUND_PID" ]; then
        echo -e "${CYAN}Found running process:${NC} PID $FOUND_PID"
        read -p "Stop this process? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill "$FOUND_PID" 2>/dev/null
            sleep 1
            if kill -0 "$FOUND_PID" 2>/dev/null; then
                echo -e "${YELLOW}Process still running, sending SIGKILL...${NC}"
                kill -9 "$FOUND_PID" 2>/dev/null
            fi
            echo -e "${GREEN}✓${NC} Process stopped"
        fi
    else
        echo "No running MCP server process found."
    fi
    exit 0
fi

# Read PID from file
SERVER_PID=$(cat "$PID_FILE")
echo "Found PID file: $PID_FILE"
echo "Server PID: $SERVER_PID"

# Read port if available
if [ -f "$PORT_FILE" ]; then
    SERVER_PORT=$(cat "$PORT_FILE")
    echo "Server Port: $SERVER_PORT"
fi
echo ""

# Check if process is running
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Process $SERVER_PID is not running"
    echo "Cleaning up PID file..."
    rm -f "$PID_FILE" "$PORT_FILE"
    echo -e "${GREEN}✓${NC} Cleanup complete"
    exit 0
fi

# Stop the server
echo "Stopping MCP server (PID: $SERVER_PID)..."

# Try graceful shutdown first (SIGTERM)
kill "$SERVER_PID" 2>/dev/null

# Wait a bit for graceful shutdown
sleep 2

# Check if it's still running
if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo -e "${YELLOW}Process still running, sending SIGKILL...${NC}"
    kill -9 "$SERVER_PID" 2>/dev/null
    sleep 1
fi

# Final check
if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo -e "${RED}✗${NC} Failed to stop server"
    echo "You may need to stop it manually:"
    echo -e "  ${CYAN}kill -9 $SERVER_PID${NC}"
    exit 1
fi

# Cleanup PID and port files
rm -f "$PID_FILE" "$PORT_FILE"

echo -e "${GREEN}✓${NC} MCP server stopped successfully"
echo ""

# Show log location
if [ -f "$LOG_FILE" ]; then
    echo "Log file preserved: $LOG_FILE"
    echo -e "View last logs: ${CYAN}tail -20 $LOG_FILE${NC}"
fi
echo ""

echo "To start the server again, run:"
echo -e "  ${CYAN}./skill_seeker_setup_mcp.sh${NC}"
echo ""
