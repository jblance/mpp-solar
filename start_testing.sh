#!/bin/bash

# CYCLE 6 Phase 6: Testing Setup Script
# This script helps prepare the environment for chart testing

set -e

echo "========================================="
echo "CYCLE 6 Phase 6: Testing Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "web_interface.py" ]; then
    echo -e "${RED}Error: web_interface.py not found${NC}"
    echo "Please run this script from the mpp-solar root directory"
    exit 1
fi

echo -e "${GREEN}✓ Found web_interface.py${NC}"

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠ Port 5000 is already in use${NC}"
    echo "Web interface may already be running"
    PID=$(lsof -Pi :5000 -sTCP:LISTEN -t)
    echo "Process ID: $PID"
    echo ""
    read -p "Kill existing process and restart? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $PID
        echo -e "${GREEN}✓ Killed process $PID${NC}"
        sleep 2
    else
        echo "Keeping existing process running"
        echo ""
        echo -e "${GREEN}Web interface already accessible at:${NC}"
        echo "  Standard Charts: http://localhost:5000/charts"
        echo "  LCARS Charts:    http://localhost:5000/charts/lcars"
        echo ""
        echo "Proceeding to open test documents..."
        sleep 2
    fi
else
    echo -e "${GREEN}✓ Port 5000 is available${NC}"
fi

# Check Python version
echo ""
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Check if daemon is running
echo ""
echo "Checking MPP-Solar daemon status..."
if systemctl is-active --quiet mpp-solar-daemon 2>/dev/null; then
    echo -e "${GREEN}✓ MPP-Solar daemon is running${NC}"
    DAEMON_RUNNING=true
else
    echo -e "${YELLOW}⚠ MPP-Solar daemon is not running${NC}"
    echo "  Some tests require daemon to be running for data"
    echo "  You can still test error scenarios without it"
    DAEMON_RUNNING=false
fi

# Start web interface if not running
if ! lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo ""
    echo "Starting web interface..."
    echo -e "${YELLOW}Note: Web interface will run in background${NC}"
    echo "  Log file: web_interface.log"
    echo "  To stop: kill \$(lsof -t -i:5000)"

    nohup python3 web_interface.py > web_interface.log 2>&1 &
    WEB_PID=$!
    echo -e "${GREEN}✓ Web interface started (PID: $WEB_PID)${NC}"

    # Wait for server to start
    echo "Waiting for server to start..."
    sleep 3

    # Check if server is actually running
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${GREEN}✓ Web interface is running on port 5000${NC}"
    else
        echo -e "${RED}✗ Web interface failed to start${NC}"
        echo "Check web_interface.log for errors"
        exit 1
    fi
fi

# Summary
echo ""
echo "========================================="
echo "Test Environment Ready!"
echo "========================================="
echo ""
echo -e "${GREEN}Access Points:${NC}"
echo "  Standard Charts: http://localhost:5000/charts"
echo "  LCARS Charts:    http://localhost:5000/charts/lcars"
echo "  Main Dashboard:  http://localhost:5000/"
echo ""
echo -e "${GREEN}Test Documents:${NC}"
echo "  Full Test Plan:  CYCLE_6_TEST_PLAN.md"
echo "  Quick Checklist: CYCLE_6_TEST_CHECKLIST.md"
echo ""
echo -e "${GREEN}Useful Commands:${NC}"
echo "  View web logs:   tail -f web_interface.log"
echo "  Stop web server: kill \$(lsof -t -i:5000)"
echo "  Check daemon:    sudo systemctl status mpp-solar-daemon"
echo ""

if [ "$DAEMON_RUNNING" = false ]; then
    echo -e "${YELLOW}Recommendations:${NC}"
    echo "  1. Start daemon for full data testing:"
    echo "     sudo systemctl start mpp-solar-daemon"
    echo ""
    echo "  2. Or proceed with error scenario testing (no daemon needed)"
    echo ""
fi

# Open browser if available
if command -v xdg-open &> /dev/null; then
    echo "Opening test documents and web interface..."
    xdg-open CYCLE_6_TEST_CHECKLIST.md &
    sleep 1
    xdg-open http://localhost:5000/charts &
    sleep 1
    xdg-open http://localhost:5000/charts/lcars &
elif command -v open &> /dev/null; then
    # macOS
    echo "Opening test documents and web interface..."
    open CYCLE_6_TEST_CHECKLIST.md &
    sleep 1
    open http://localhost:5000/charts &
    sleep 1
    open http://localhost:5000/charts/lcars &
else
    echo -e "${YELLOW}Manual browser opening required:${NC}"
    echo "  1. Open CYCLE_6_TEST_CHECKLIST.md"
    echo "  2. Open http://localhost:5000/charts in browser"
    echo "  3. Open http://localhost:5000/charts/lcars in browser"
fi

echo ""
echo -e "${GREEN}Happy Testing! 🧪${NC}"
echo ""
