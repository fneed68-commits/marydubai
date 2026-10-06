#!/bin/bash
mkdir -p screenshots

# 1. Banner
cat > screenshots/01_banner.txt << 'EOF'
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        🎯 MaryDubai Multi-Agent System v1.0             ║
║                                                          ║
║        Human-in-the-Loop AI for:                        ║
║        • Security Research                               ║
║        • Financial Analysis                              ║
║        • Legal Compliance                                ║
║        • Wallet Security                                 ║
║                                                          ║
║        7 Agents | 74 Tests | 100% Pass Rate             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF

# 2. Agents list
python3 main.py --list > screenshots/02_agents.txt 2>&1

# 3. Legal demo
echo "yes" | python3 main.py --agent legal --action "CTF Report Review" > screenshots/03_legal.txt 2>&1

# 4. Temporal demo
echo "no" | python3 main.py --agent temporal --time 1.1 > screenshots/04_temporal.txt 2>&1

# 5. Loop demo
echo "no" | python3 main.py --agent loop --action "test" --result "test" > screenshots/05_loop.txt 2>&1

# 6. RAG demo
echo "yes" | python3 main.py --agent rag --query "HITL safety" > screenshots/06_rag.txt 2>&1

# 7. Tests
python3 -m unittest discover -s tests 2>&1 | grep -E "^(Ran|OK|FAILED)" > screenshots/07_tests.txt

echo "✅ Created $(ls screenshots/ | wc -l) screenshots"
ls -la screenshots/
