#!/usr/bin/env bash
set -euo pipefail

KEY_DIR="$(dirname "$0")/../keys"
mkdir -p "$KEY_DIR"

echo "Generating SSH key pair for nix-dev environment..."
ssh-keygen -t ed25519 -f "$KEY_DIR/nix-dev" -C "developer@cloudydad.world" -N ""

echo ""
echo "=========================================="
echo "SSH Key Pair Generated"
echo "=========================================="
echo ""
echo "Private key: $KEY_DIR/nix-dev"
echo "Public key:"
cat "$KEY_DIR/nix-dev.pub"
echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo "1. Store nix-dev (private) securely in Bitwarden"
echo "2. Add nix-dev.pub to GitHub/SSH keys if needed for git access"
echo "3. Update nix-dev-ssh-secret.yaml with the public key"
echo "4. Run: kubeseal --format yaml < clusters/cloudydad/apps/nix-dev/app/nix-dev-ssh-secret.yaml > clusters/cloudydad/apps/nix-dev/app/nix-dev-ssh-sealed.yaml"
echo ""
