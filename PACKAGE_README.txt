====================================================
MaryDubai Multi-Agent System v1.0
Buyer's Quick Start Guide
====================================================

Thank you for purchasing!

## What's Included

- 7 specialized AI agents
- Unified CLI (main.py)
- Test suite (74 tests)
- Documentation (README.md, PITCH.md, PRICING.md)
- Interactive demo (demo.sh)

## System Requirements

- Python 3.10 or higher
- SQLite (built-in with Python)
- 50 MB free space

## Quick Start (5 minutes)

### Step 1: Extract

    tar -xzf marydubai_v1.0.tar.gz
    cd termux_secops_project

### Step 2: Run the demo

    bash demo.sh

### Step 3: List all agents

    python3 main.py --list

### Step 4: Run tests

    python3 -m unittest discover -s tests -v

### Step 5: Try individual agents

    # Legal consultant
    python3 main.py --agent legal --action "Review this contract"

    # Temporal safety
    python3 main.py --agent temporal --time 1.5

    # Loop breaker
    python3 main.py --agent loop --action "step" --result "output"

    # RAG search
    python3 main.py --agent rag --query "How does HITL work?"

## Optional: Enable Better Embeddings

The default LocalHashEmbedder works offline but produces
low similarity scores (~0.1). For production use:

1. Get a free API key from https://aistudio.google.com/app/apikey
2. Install the library:
       pip install google-generativeai
3. Export the key:
       export GEMINI_API_KEY="your_key_here"
4. Run with --use-gemini flag:
       python3 main.py --agent rag --query "..." --use-gemini

## How HITL Works

Every agent stops after each step and waits for your explicit
approval. Type "yes" to proceed, anything else to freeze.

Example:
    👤 [الموجه كابتن] هل توافق؟ (yes/no): yes

## Building Your Own Index

To index your own documents for RAG:

    # Local mode (offline)
    python3 index_builder.py --source ./docs --local

    # With Gemini (better quality)
    python3 index_builder.py --source ./docs --clear

## Adding New Agents

1. Create file: my_agent.py
2. Define class with same pattern as existing agents
3. Register in main.py AGENTS dictionary
4. Use same HITL pattern: await_*_command

## Support

Email: fneed68@gmail.com
Response time: 24-48 hours

## License

Commercial license. See LICENSE file.

## Refund Policy

14 days. Contact support first.

====================================================
Enjoy MaryDubai!
====================================================
