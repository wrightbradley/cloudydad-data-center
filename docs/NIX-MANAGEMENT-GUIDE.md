# Nix-Based K3s Cluster Management Guide

**Status**: 7 of 7 nodes fully operational with Nix-managed k3s ✅\
**Configuration Version**: 2.0 (Phase 1 - Maximum Nix Adoption)\
**Last Updated**: 2026-02-16 17:47 UTC

## Overview

This cluster is now primarily managed via **Nix** with **system-manager** for
declarative, immutable, and idempotent configuration. Phase 1 of the "Maximum
Nix Adoption" strategy has been implemented, expanding Nix management to cover
~80% of k3s infrastructure while maintaining safety. Ansible is relegated to
one-time bootstrap operations only.

### Architecture

- **System Management**: Nix + system-manager (declarative)
- **K3s Version**: v1.32.11+k3s3 (pinned via `k3s_1_32` package)
- **Configuration Version**: 2.0 (Phase 1 expansion)
- **Secrets Management**: sops-nix with age keys derived from SSH host keys
- **Application Management**: Flux (unchanged, manages k8s resources)
- **Bootstrap Tool**: Ansible (one-time use only)

### What Nix Manages (Phase 1)

- ✅ **K3s services** - Server and agent systemd units
- ✅ **System packages** - All k3s dependencies (kubectl, storage tools,
  monitoring)
- ✅ **Storage services** - multipathd, iscsid (for persistent volumes)
- ✅ **Configuration files** - multipath.conf, static configs
- ✅ **Sysctl parameters** - Network forwarding, bridge netfilter
- ✅ **Kernel modules** - br_netfilter, overlay
- ✅ **Service dependencies** - Proper ordering (storage before k3s)
- ✅ **Timezone** - System-wide UTC

### What Ansible Still Manages

- 🔧 **Bootstrap** - Nix installation, initial setup
- 🔧 **Network** - NetworkManager, DNS, interfaces
- 🔧 **Users** - bwright, ansible users, SSH keys
- 🔧 **SSH hardening** - Security policies
- 🔧 **OS updates** - apt dist-upgrade, system reboots

See [NIX-PHASE1-MIGRATION.md](./NIX-PHASE1-MIGRATION.md) for full details on
Phase 1 changes.

## Cluster Status

### ✅ Operational Nix-Managed Nodes (7/7)

**Master Nodes:**

- `surfacebook` (172.18.2.2) - x86_64, Debian 12 - ✅ Ready
- `rpi07` (172.18.2.17) - ARM64, Debian 12 - ✅ Ready
- `rpi06` (172.18.2.16) - ARM64, Debian 13/trixie - ✅ Ready (multipathd failed,
  non-critical)

**Worker Nodes:**

- `mini` (172.18.2.1) - x86_64, Debian 12 - ✅ Ready
- `beelink-1` (172.18.2.21) - x86_64, Debian 12 - ✅ Ready
- `beelink-2` (172.18.2.22) - x86_64, Debian 12 - ✅ Ready
- `beelink-3` (172.18.2.23) - x86_64, Debian 12 - ✅ Ready (recovered)

All operational nodes:

- Running k3s v1.32.11+k3s3
- Managed by: **system-manager** (Nix)
- Configuration: **Version 2.0 (Phase 1)**
- Old Ansible services: Removed
- Old k3s binaries: Cleaned up

### ⚠️ Known Issues

**rpi06 multipathd service**

- **Status:** Failed (DM multipath kernel driver not loaded)
- **Impact:** None - k3s and iscsid operational, node Ready
- **Cause:** Debian 13 kernel 6.12.62 may not have dm_multipath module
- **Resolution:** Not required unless multipath storage needed

### 🗑️ Deleted Node

- `rpi05` (172.18.2.15) - ARM64, Debian 13 - Permanently removed from cluster

## Daily Operations (Nix-First)

### Making Configuration Changes

All configuration changes should be made to the Nix configuration files, NOT
through Ansible playbooks.

#### 1. Update Nix Configuration

Edit the configuration on each node:

```bash
# On the target node
sudo vi /etc/nix-system/configuration.nix
```

Common changes:

- K3s server/agent arguments
- Service resource limits
- Environment variables
- Package versions

#### 2. Apply Changes

Activate the new configuration:

```bash
# On the target node
cd /etc/nix-system
sudo /nix/var/nix/profiles/default/bin/nix flake update  # Optional: update inputs
sudo /nix/var/nix/profiles/default/bin/nix run 'github:numtide/system-manager' -- switch --flake .
```

#### 3. Verify

Check service status:

```bash
sudo systemctl status k3s.service         # Master nodes
sudo systemctl status k3s-agent.service   # Worker nodes
sudo systemctl status system-manager.target
```

### Using Ansible for Remote Changes (Temporary)

Until we have a central Nix configuration repository, you can use Ansible to
distribute and activate configuration changes:

```bash
# Update configuration on all nodes
ansible all:!rpi05 -m copy -a "src=new-configuration.nix dest=/etc/nix-system/configuration.nix" -b

# Activate on all nodes
ansible all:!rpi05 -m shell -a "cd /etc/nix-system && /nix/var/nix/profiles/default/bin/nix run 'github:numtide/system-manager' -- switch --flake ." -b
```

### Upgrading K3s Version

#### Option 1: Update Nix Package Pin (Recommended)

Edit `/etc/nix-system/configuration.nix` and change the k3s package:

```nix
# Current: pkgs.k3s_1_32  (v1.32.11+k3s3)
# To upgrade to 1.33.x:
pkgs.k3s_1_33  # When available in nixpkgs
```

Then activate as shown above.

#### Option 2: Use Latest Stable

```nix
# Change from:
pkgs.k3s_1_32

# To:
pkgs.k3s  # Latest stable version
```

**Note**: Verify version compatibility across all nodes before upgrading.

### Rolling Back Changes

System-manager maintains generations, allowing easy rollbacks:

```bash
# List generations
ls -la /nix/var/nix/gcroots/system-manager-*

# Rollback to previous generation
sudo /nix/var/nix/profiles/default/bin/nix run 'github:numtide/system-manager' -- rollback
```

## Verification Commands

### Check Cluster Health

```bash
# From any master node
kubectl get nodes -o wide

# Or via Ansible
ansible surfacebook -m shell -a "kubectl get nodes -o wide" -b
```

### Verify Nix Management

```bash
# Check system-manager status on all nodes
ansible all:!rpi05 -m shell -a "systemctl status system-manager.target --no-pager" -b

# Verify k3s services are Nix-managed
ansible all:!rpi05 -m shell -a "systemctl list-units 'k3s*.service' --all --no-pager --no-legend" -b

# Check for old Ansible binaries (should return "not found")
ansible all:!rpi05 -m shell -a "ls -la /usr/local/bin/k3s 2>&1 || true" -b
```

### Verify Configuration Files

```bash
# Check Nix configs exist
ansible all:!rpi05 -m shell -a "ls -la /etc/nix-system/configuration.nix /etc/nix-system/flake.nix" -b

# View current generation
ansible all:!rpi05 -m shell -a "ls -la /nix/var/nix/gcroots/system-manager-current" -b
```

### Verify Storage Services (Phase 1)

Check that storage services are running (required for k3s persistent volumes):

```bash
# On each node
sudo systemctl status multipathd.service
sudo systemctl status iscsid.service

# Via Ansible
ansible all:!rpi05 -m shell -a "systemctl is-active multipathd iscsid" -b

# Verify service dependencies
sudo systemctl list-dependencies k3s.service | grep -E "(multipath|iscsi)"
```

### Verify Phase 1 Packages

Check that all Phase 1 packages are available:

```bash
# On each node
which k3s kubectl htop iotop iftop vim nvim tmux mosh rg dig lspci lsscsi

# Check multipath configuration
cat /etc/multipath.conf

# List Nix-managed packages
nix profile list --profile /nix/var/nix/profiles/system-manager
```

## Troubleshooting

### Service Not Starting After Changes

1. Check service logs:
   ```bash
   sudo journalctl -u k3s.service -n 100
   sudo journalctl -u k3s-agent.service -n 100
   ```

2. Verify configuration syntax:
   ```bash
   cd /etc/nix-system
   sudo /nix/var/nix/profiles/default/bin/nix flake check
   ```

3. Rollback to previous generation:
   ```bash
   sudo /nix/var/nix/profiles/default/bin/nix run 'github:numtide/system-manager' -- rollback
   ```

### Nix Command Not Found

Nix is not in the default PATH for non-interactive shells. Use full paths:

```bash
/nix/var/nix/profiles/default/bin/nix
```

Or source Nix profile:

```bash
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

### "No space left on device"

Root filesystem too small. Expand before making changes:

```bash
# Check disk space
df -h /
sudo lvs

# Expand (adjust VG name as needed)
sudo lvextend -L +5G /dev/VGNAME/root
sudo resize2fs /dev/VGNAME/root
```

### Unmanaged `/etc/nix/nix.conf` Warning

This warning is expected and non-fatal. The file was created by the Nix
installer and system-manager cannot manage it. No action needed.

## Future Improvements

### 1. Central Configuration Repository

**Goal**: Single source of truth for all node configurations.

**Approach**:

- Create a Git repository with flake.nix defining all nodes
- Use `nixosConfigurations` or similar pattern
- Each node pulls configuration from repo instead of local files
- Configuration changes are Git commits

**Benefits**:

- Version control for all configuration changes
- Easy rollback via Git history
- PR-based change review
- Consistent configuration across nodes

### 2. Automated Configuration Deployment

**Options**:

- **Option A**: Cron job on each node to pull and activate changes
- **Option B**: CI/CD pipeline to push changes to nodes
- **Option C**: NixOps or similar deployment tool

### 3. Remove Ansible Dependency

Once central configuration repo is in place:

- Initial node provisioning via PXE boot or disk image
- Nix configuration applied on first boot
- No Ansible roles or playbooks needed

### 4. Secrets Management Enhancement

Current: sops-nix with age keys derived from SSH host keys (working)

Potential improvements:

- Central secrets repository
- Automated secret rotation
- Key backup and recovery procedures

### 5. Monitoring and Alerting

- Nix generation tracking
- Configuration drift detection
- Automated health checks
- Alert on service failures

## Key Files and Locations

### On Each Node

```
/etc/nix-system/
├── configuration.nix          # Main Nix configuration
├── flake.nix                  # Flake definition
├── flake.lock                 # Locked dependencies
├── age-key.txt                # Private age key (sops)
└── age-key.pub                # Public age key (sops)

/etc/systemd/system/
├── k3s.service                # Symlink to Nix-managed unit (masters)
├── k3s-agent.service          # Symlink to Nix-managed unit (workers)
└── system-manager.target      # System-manager activation target

/nix/var/nix/gcroots/
└── system-manager-current     # Current generation GC root

/var/lib/system-manager/state/
└── system-manager-state.json  # System-manager state tracking
```

### In Repository

```
roles/nix-bootstrap/
├── defaults/main.yml
├── handlers/main.yml
├── tasks/
│   ├── main.yml
│   ├── install-nix.yml
│   ├── install-system-manager.yml
│   ├── setup-sops.yml
│   ├── deploy-config.yml
│   └── activate.yml
└── templates/
    ├── configuration.nix.j2   # Template for node config
    └── flake.nix.j2           # Template for flake

playbooks/
└── bootstrap-nix.yml          # One-time bootstrap playbook

docs/
├── nix-poc-rpi05.md           # Original POC documentation
├── NIX-BOOTSTRAP-SUMMARY.md   # Bootstrap implementation summary
└── NIX-MANAGEMENT-GUIDE.md    # This file
```

## Migration Lessons Learned

### Template Issues Fixed

1. **Duplicate `LimitNPROC`**: Removed duplicate, added `LimitCORE` instead
2. **Duplicate `--node-ip`**: Removed explicit parameter, let k3s derive from
   `--flannel-iface`
3. **Service Type**: Changed from `Type="notify"` to `Type="exec"`
4. **Small `/tmp`**: Set `TMPDIR=/var/tmp` in Nix installer

### Operational Patterns Discovered

1. **Disk space critical**: All nodes needed root filesystem expansion
2. **Old services persist**: Manual cleanup of old k3s services required
3. **Service timing**: Bootstrap playbook checks services too quickly
4. **Version tolerance**: Cluster tolerates mixed versions during migration

### Bootstrap Improvements Needed

- [ ] Pre-flight check for disk space (warn if root < 10GB)
- [ ] Check for all old k3s service variants
- [ ] Add retry logic for service verification
- [ ] Longer wait time after activation
- [ ] Automated old binary cleanup

## Idempotency Verification

✅ **Verified**: Re-running system-manager activation is fully idempotent.

Tested on:

- rpi06 (master)
- beelink-2 (worker)

Both nodes:

- Rebuilt configuration successfully
- Activated without errors
- Services remained active
- No configuration drift

## Conclusion

The cluster is now in a **stable, Nix-managed state** with all 7 nodes
successfully migrated. The system is:

- ✅ **Immutable**: Configuration defined in Nix expressions
- ✅ **Repeatable**: Same configuration produces same results
- ✅ **Idempotent**: Re-applying configuration is safe and has no side effects
- ✅ **Versioned**: System-manager maintains generations for rollback
- ✅ **Declarative**: Desired state defined in configuration files

Ansible is now only used for:

- One-time node bootstrap (when adding new nodes)
- Ad-hoc remote command execution (until central config repo exists)

All ongoing configuration management should be done via Nix and system-manager.
