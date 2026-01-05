# Nix Remote Development Environment

## Overview

This is a Nix-based remote development environment deployed via Flux to your K3S cluster. It provides:

- **Fish shell** with your complete configuration (200+ aliases, 33 functions, Fisher plugins)
- **Neovim** with your full config from GitHub (lazy.nvim + 60+ plugins)
- **TMUX** with continuum auto-restore and persistence
- **Access**: SSH (key pair) + OAuth2-protected web terminal (GotTY)
- **Storage**: TrueNAS NFS via democratic-csi (43Gi total)
- **Resource optimized**: ~850m CPU, 1.75Gi RAM

## Quick Start

### 1. Generate SSH Keys

```bash
cd nix/scripts
./generate-ssh-keys.sh
```

This generates a key pair for SSH access. Store the private key securely in Bitwarden.

### 2. Create Authentik Application

Navigate to `https://authentik.cloudydad.world` and create:

1. **Provider**: Name `nix-dev`, Type `Proxy Provider`
2. **Application**: Name `nix-dev-web`, Type `Proxy`, Provider `nix-dev`
   - Redirect URI: `https://dev.cloudydad.world/oauth2/callback`
   - Authorization flow: `forward_auth (forwardAuth)`
3. **Policy**: Name `nix-dev-policy`
   - Users: Select your user
   - Permissions: `Can use applications` → `nix-dev-web`

### 3. Create Sealed Secret

```bash
# Edit clusters/cloudydad/apps/nix-dev/app/nix-dev-ssh-secret.yaml
# Replace ssh-public-key and ssh-private-key with actual values

# Then run:
kubeseal --format yaml < clusters/cloudydad/apps/nix-dev/app/nix-dev-ssh-secret.yaml \
  > clusters/cloudydad/apps/nix-dev/app/nix-dev-ssh-sealed.yaml
```

### 4. Deploy to Cluster

```bash
git add clusters/cloudydad/apps/nix-dev
git commit -m "Add nix-dev environment - Fish + nvim + TMUX"
git push origin develop
```

Flux will automatically deploy within 5 minutes.

## Access

### SSH Access

```bash
# Get LoadBalancer IP
kubectl get svc nix-dev-ssh -n nix-dev

# Connect
ssh -p 2222 -i ~/.ssh/nix-dev dev@<loadbalancer-ip>
```

### Browser Access (GotTY + Authentik OAuth2)

1. Navigate to `https://dev.cloudydad.world`
2. Authenticate via Authentik (OAuth2)
3. GotTY web terminal appears with Fish shell
4. Type `nvim` to start (plugins auto-install via lazy.nvim)
5. Type `tmux` to attach to sessions (auto-restored)

## Nix Strategy

### What Nix Manages:

1. **Package installation** via nixpkgs
2. **Clone nvim config** from GitHub to `~/.config/nvim` on first activation
3. **Install dependencies** (Node.js, Python, Lua, Go, etc.)
4. **Environment setup** (PATH, etc.)

### What Nix Does NOT Manage:

1. **nvim plugins** - lazy.nvim handles this
2. **nvim configuration** - managed by your GitHub repo
3. **LSP/formatters** - Mason manages these

### Benefits

- ✅ Declarative package management via Nix
- ✅ Git-based nvim config management (pull/commit like normal)
- ✅ Lazy.nvim handles plugin management automatically
- ✅ Clean separation of concerns

## Configuration

### Nix Structure

```
nix/
├── flake.nix                          # Nix flake entry point
├── home.nix                           # Home Manager config
├── modules/
│   ├── fish/                          # Fish shell module
│   ├── nvim/                          # nvim PACKAGE ONLY (no config management)
│   ├── tmux/                          # TMUX module
│   ├── starship/                       # Starship prompt
│   ├── git/                            # Git configuration
│   └── packages/                       # Dev packages
└── scripts/
    ├── generate-ssh-keys.sh            # SSH key generation
    └── activate-dev-env.sh           # Helper script
```

### Kubernetes Resources

- **Namespace**: `nix-dev`
- **Deployment**: 3 containers (nix-dev + gotty + sshd)
- **Storage**: 43Gi total on TrueNAS NFS
  - Workspace: 30Gi
  - Config: 3Gi
  - Nix Store: 10Gi
- **Services**:
  - LoadBalancer: SSH on port 2222
  - ClusterIP: GotTY on port 8080
- **Ingress**: Traefik with Authentik OAuth2 middleware

### Resource Requirements

- **Total**: 850m CPU / 1.75Gi RAM
  - Main container (Nix + Home Manager): 750m CPU / 1.5Gi RAM
  - GotTY sidecar: 50m CPU / 256Mi RAM
  - SSHD sidecar: 50m CPU / 256Mi RAM

## Troubleshooting

### nvim Config Not Cloned

If nvim config doesn't clone, manually SSH into the container and run:

```bash
rm -rf ~/.config/nvim
git clone --depth 1 https://github.com/wrightbradley/nvim.git ~/.config/nvim
```

### TMUX Sessions Not Restoring

Ensure TMUX continuum is enabled:

```bash
tmux show -g @continuum-restore  # Should be 'on'
tmux show -g @continuum-save-interval  # Should be '15' (minutes)
```

### Home Manager Activation Issues

Re-run Home Manager activation:

```bash
# From inside the container
cd /home/developer
nix run home-manager/master --switch
```

## Maintenance

### Updating nvim Config

```bash
cd ~/.config/nvim
git pull origin main
# nvim will use updated config on next restart
```

### Updating Packages

```bash
# Nix packages
nix flake update
nix run nixpkgs#home-manager --switch

# nvim plugins (lazy.nvim)
nvim
:Lazy sync
```

## Resources

- [Nix Documentation](https://nixos.org/manual/nix/stable/)
- [Home Manager Documentation](https://nix-community.github.io/home-manager/)
- [nvim Config](https://github.com/wrightbradley/nvim)
- [Authentik Documentation](https://goauthentik.io/docs/)
