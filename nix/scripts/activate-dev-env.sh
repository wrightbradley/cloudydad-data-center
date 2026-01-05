#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=========================================="
echo "Nix Development Environment Setup"
echo "=========================================="
echo ""

echo "Prerequisites check:"
if ! command -v nix &> /dev/null; then
  echo "❌ Nix is not installed"
  echo "Please install Nix first: https://nixos.org/download.html"
  exit 1
fi

echo "✅ Nix is installed"
echo ""

echo "Initializing Home Manager..."
if [ ! -d "$HOME/.config/nix" ]; then
  echo "Installing Home Manager..."
  nix-channel --add https://github.com/nix-community/home-manager/archive/master-24.05.tar.gz home-manager
  nix-channel --update
  nix run home-manager/master --init --switch
else
  echo "✅ Home Manager already initialized"
  nix run home-manager/master --switch
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "You can now:"
echo "  - Use 'nvim' to start Neovim (your config from GitHub will be cloned)"
echo "  - Use 'tmux' to start TMUX (continuum auto-restore enabled)"
echo "  - Use 'fish' shell with your aliases and functions"
echo ""
