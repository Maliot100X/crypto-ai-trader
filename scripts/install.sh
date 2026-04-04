#!/bin/bash
# Solana Agent Trader - Master Installation Script
set -e

echo "============================================="
echo "  SOLANA AGENT TRADER - Installation"
echo "  Self-Assembling AI Trading Lab"
echo "============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
info() { echo -e "${BLUE}[*]${NC} $1"; }

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    log "Detected Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    log "Detected macOS"
else
    warn "Unsupported OS: $OSTYPE"
fi

# Python
info "Checking Python..."
if command -v python3 &>/dev/null; then
    log "Python3 found: $(python3 --version)"
else
    warn "Python3 not found. Installing..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
fi

# Node.js
info "Checking Node.js..."
if command -v node &>/dev/null; then
    log "Node.js found: $(node --version)"
else
    warn "Node.js not found. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Create Python virtual environment
info "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
log "Python dependencies installed"

# Setup Dashboard
info "Setting up Dashboard..."
cd dashboard
npm install
log "Dashboard dependencies installed"
cd ..

# Copy env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    warn "Created .env from .env.example - please configure your API keys"
fi

# Run sub-scripts
info "Running setup scripts..."
bash scripts/setup_skills.sh
bash scripts/setup_agents.sh

echo ""
echo "============================================="
echo "  Installation Complete!"
echo "============================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run: python verify_env.py"
echo "  3. Start API: python api_server.py"
echo "  4. Start Dashboard: cd dashboard && npm run dev"
echo "  5. Or use Docker: cd docker && docker-compose up"
echo ""
