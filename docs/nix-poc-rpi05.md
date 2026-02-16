# Nix Bootstrap POC: rpi05 Migration Guide

This guide walks you through migrating **rpi05** from Ansible-managed k3s to
Nix-managed k3s as a proof-of-concept.

## Overview

**Goal**: Migrate rpi05 (Raspberry Pi 3B+ worker node) from Ansible to Nix
management

**Expected Duration**: 20-30 minutes

**Risk Level**: Low (single worker node, can revert easily)

**Prerequisites**:

- Bitwarden CLI authenticated (`bw login` and `bw unlock`)
- Ansible environment set up (`make install`)
- SSH access to rpi05
- kubectl access to cluster

---

## Phase 1: Pre-Flight Checks (5 minutes)

### 1.1 Verify Current State

```bash
# Check rpi05 is in cluster
kubectl get node rpi05
# Should show: Ready

# Check current k3s service (Ansible-managed)
ssh rpi05 'systemctl status k3s-agent'
# Should show: active (running)

# Check current workloads
kubectl get pods -A -o wide | grep rpi05
# Note which pods are running on rpi05
```

### 1.2 Backup Current Configuration

```bash
# Create backup directory
mkdir -p backups/rpi05-$(date +%Y%m%d)

# Backup current k3s service
ssh rpi05 'cat /etc/systemd/system/k3s-agent.service' > backups/rpi05-$(date +%Y%m%d)/k3s-agent.service

# Backup current k3s config
ssh rpi05 'cat /etc/rancher/k3s/config.yaml' > backups/rpi05-$(date +%Y%m%d)/config.yaml 2>/dev/null || echo "No config.yaml"

# Get current node status
kubectl describe node rpi05 > backups/rpi05-$(date +%Y%m%d)/node-status.txt
```

---

## Phase 2: Run Bootstrap (10-15 minutes)

### 2.1 Authenticate Bitwarden

```bash
# Ensure Bitwarden session is active
export BW_SESSION=$(bw unlock --raw)

# Verify token can be fetched
bw get item 0c769bf1-4a82-4cde-876f-b1a3018171e6 --session $BW_SESSION
```

### 2.2 Run Ansible Bootstrap Playbook

```bash
# Dry-run first (check mode)
ansible-playbook playbooks/bootstrap-nix.yml --limit rpi05 --check --diff

# Review what will change
# - Nix will be installed
# - system-manager will be installed
# - k3s service will transition from Ansible to Nix management

# Execute bootstrap
ansible-playbook playbooks/bootstrap-nix.yml --limit rpi05

# When prompted, type 'yes' to confirm
```

**What happens during bootstrap:**

1. ✓ Installs Nix (multi-user daemon)
2. ✓ Installs system-manager
3. ✓ Generates age keys from SSH host key
4. ✓ Deploys Nix configuration to `/etc/nix-system/`
5. ✓ Stops Ansible-managed k3s-agent service
6. ✓ Activates system-manager (starts Nix-managed k3s-agent)
7. ✓ Waits for node to rejoin cluster

### 2.3 Monitor Bootstrap Progress

In another terminal, watch the node status:

```bash
# Watch node status
watch -n 2 'kubectl get nodes'

# Watch rpi05 logs
ssh rpi05 'journalctl -u k3s-agent -f'
```

---

## Phase 3: Validation (5-10 minutes)

### 3.1 Verify Nix Installation

```bash
# SSH to rpi05
ssh rpi05

# Check Nix version
nix --version
# Should show: nix (Nix) 2.x.x

# Check system-manager
system-manager --version

# Check age public key
cat /etc/nix-system/age.pub
# Save this key - you'll need it for sops-nix setup
```

### 3.2 Verify K3s Service

```bash
# Check k3s-agent service (now managed by system-manager)
systemctl status k3s-agent
# Should show:
# - Loaded: loaded (/nix/store/...)
# - Active: active (running)

# Check service is NOT the old Ansible one
systemctl cat k3s-agent | head -5
# Should show path to /nix/store, not /etc/systemd/system
```

### 3.3 Verify Node in Cluster

```bash
# Exit from rpi05
exit

# Check node is Ready
kubectl get node rpi05
# Should show: Ready

# Check node details
kubectl describe node rpi05

# Verify pods scheduled back on rpi05
kubectl get pods -A -o wide | grep rpi05
# Should see pods running again
```

### 3.4 Test Idempotency

```bash
# SSH back to rpi05
ssh rpi05

# Re-run system-manager (should show no changes)
cd /etc/nix-system
system-manager switch --flake .

# Should output something like:
# "Activating configuration..."
# "No service changes needed"

exit
```

---

## Phase 4: Set Up deploy-rs (Optional, 10 minutes)

After validating the bootstrap, set up deploy-rs for remote deployments from
your laptop.

### 4.1 Update sops-nix Configuration

```bash
# Add rpi05's age public key to nix-cluster/secrets/.sops.yaml
# Replace the placeholder with actual key from rpi05:/etc/nix-system/age.pub

vim nix-cluster/secrets/.sops.yaml
```

Update the file:

```yaml
keys:
  - &admin YOUR_PERSONAL_AGE_KEY # Generate with: age-keygen
  - &rpi05 age1xxxxxx... # From rpi05:/etc/nix-system/age.pub
```

### 4.2 Initialize Flake

```bash
cd nix-cluster/

# Enter dev shell with deploy-rs
nix develop

# Initialize flake.lock
nix flake update

# Test build
nix flake check
```

### 4.3 Test Deploy

```bash
# Dry-run deployment
deploy --dry-activate .#rpi05

# Deploy configuration
deploy .#rpi05

# Verify k3s-agent restarted successfully
kubectl get node rpi05
```

---

## Phase 5: Make a Test Change (5 minutes)

Verify you can make configuration changes via Nix.

### 5.1 Edit Node Configuration

```bash
# Edit rpi05 config
vim nix-cluster/nodes/rpi05.nix

# Add a new package (example):
environment.systemPackages = with pkgs; [
  # ... existing packages ...
  jq  # Add JSON processor
];
```

### 5.2 Deploy Change

```bash
# Deploy via deploy-rs
deploy .#rpi05

# Or SSH and activate manually
ssh rpi05
cd /etc/nix-system
git pull  # If you've pushed to git
system-manager switch --flake .
```

### 5.3 Verify Change

```bash
# SSH to rpi05
ssh rpi05

# Check new package is available
which jq
# Should show: /nix/store/.../bin/jq

jq --version
```

---

## Rollback Plan

If something goes wrong, you can revert to Ansible-managed k3s:

### Option 1: Quick Rollback (On Node)

```bash
# SSH to rpi05
ssh rpi05

# Stop Nix-managed k3s-agent
systemctl stop k3s-agent

# Restore Ansible systemd service
cp backups/rpi05-YYYYMMDD/k3s-agent.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable k3s-agent
systemctl start k3s-agent

# Verify
systemctl status k3s-agent
```

### Option 2: Full Ansible Re-Deployment

```bash
# Re-run Ansible site playbook
ansible-playbook playbooks/site.yml --limit rpi05

# This will overwrite Nix-managed config
```

---

## Success Criteria

✅ **Bootstrap Successful** if:

1. `kubectl get node rpi05` shows `Ready`
2. Pods schedule and run on rpi05 normally
3. `ssh rpi05 'systemctl status k3s-agent'` shows service from `/nix/store/...`
4. Re-running `system-manager switch` is idempotent (no changes)
5. Node stays stable for 24-48 hours

❌ **Bootstrap Failed** if:

1. Node shows `NotReady` for >5 minutes
2. k3s-agent service crashes or restarts repeatedly
3. Pods won't schedule on rpi05
4. Network connectivity issues

---

## Troubleshooting

### Node Won't Join Cluster

```bash
# Check k3s-agent logs
ssh rpi05 'journalctl -u k3s-agent -n 100'

# Common issues:
# - Token mismatch: Check /etc/rancher/k3s/k3s-token
# - Network: Ping apiserver endpoint: ping 172.18.255.253
# - Firewall: Check iptables rules
```

### System-Manager Fails to Activate

```bash
ssh rpi05

# Check Nix configuration for errors
cd /etc/nix-system
nix flake check

# Try activating with verbose output
system-manager switch --flake . --verbose
```

### Age Key Issues

```bash
# Regenerate age keys
ssh rpi05
cd /etc/nix-system
rm age.key age.pub
ssh-to-age < /etc/ssh/ssh_host_ed25519_key.pub > age.pub
ssh-to-age -private-key < /etc/ssh/ssh_host_ed25519_key > age.key
chmod 600 age.key
```

---

## Next Steps After Successful POC

1. **Monitor for 1 week**: Watch rpi05 stability, check for any issues
2. **Migrate another worker**: Repeat for `mini` or a `beelink` node
3. **Set up CI/CD**: Automate deploy-rs deployments on git push
4. **Migrate masters**: Plan careful migration of control plane nodes
5. **Deprecate Ansible**: Archive old playbooks, keep only bootstrap

---

## Questions?

Check:

- `nix-cluster/README.md` - Nix cluster management docs
- `roles/nix-bootstrap/README.md` - Bootstrap role details
- System-manager docs: https://github.com/numtide/system-manager
- Deploy-rs docs: https://github.com/serokell/deploy-rs
