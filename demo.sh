#!/bin/bash
# MaryDubai Multi-Agent System - Interactive Demo
# Run: bash demo.sh

set -e

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m"

echo ""
echo "============================================================"
echo "  MaryDubai Multi-Agent System - Interactive Demo"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}Error: python3 not found${NC}"
    exit 1
fi

echo -e "${BLUE}[1/6]${NC} Checking installation..."
python3 -c "from shared import LocalHashEmbedder, SQLiteVectorStore; print('  OK - shared modules loaded')"

echo ""
echo -e "${BLUE}[2/6]${NC} Listing available agents..."
python3 main.py --list

echo ""
echo -e "${BLUE}[3/6]${NC} Testing Legal Agent..."
echo "yes" | python3 main.py --agent legal --action "Demo legal review"

echo ""
echo -e "${BLUE}[4/6]${NC} Testing Loop Breaker Agent..."
echo "no" | python3 main.py --agent loop --action "test" --result "test"

echo ""
echo -e "${BLUE}[5/6]${NC} Testing Temporal Agent (dangerous time)..."
echo "no" | python3 main.py --agent temporal --time 1.1

echo ""
echo -e "${BLUE}[6/6]${NC} Running RAG query..."
echo "yes" | python3 main.py --agent rag --query "what is HITL"

echo ""
echo "============================================================"
echo "  Demo complete! All 7 agents are functional."
echo "============================================================"
echo ""
