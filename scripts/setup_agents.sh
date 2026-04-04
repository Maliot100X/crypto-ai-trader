#!/bin/bash
# Setup trading agents
echo "[*] Configuring trading agents..."

AGENTS_DIR="agents"
if [ -d "$AGENTS_DIR" ]; then
    echo "[+] Agent modules found"
    python3 -c "
import sys
sys.path.insert(0, '.')
from agents.runtime import AgentRuntime
runtime = AgentRuntime()
for i in range(5):
    personalities = ['aggressive', 'conservative', 'analytical', 'momentum', 'contrarian']
    runtime.create_agent(f'agent_{i+1}', {'personality': personalities[i]})
print(f'[+] Created {len(runtime.agents)} agents')
for aid, agent in runtime.agents.items():
    print(f'    - {aid}: {agent.config.get(\"personality\", \"default\")}')
" 2>/dev/null || echo "[!] Agent setup will complete on first run"
fi
echo "[+] Agent setup complete"
