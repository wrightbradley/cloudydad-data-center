# Troubleshooting: beelink-3 Recovery

**Node:** beelink-3 (172.18.2.23)\
**Role:** Worker\
**Architecture:** x86_64\
**OS:** Debian GNU/Linux 12 (bookworm)\
**Status:** NotReady, unresponsive\
**Issue Date:** February 16, 2026

---

## Issue Summary

beelink-3 became unresponsive after rebooting following successful Phase 1 Nix
deployment. The node does not respond to SSH or ping, and shows NotReady status
in the Kubernetes cluster.

## Timeline

1. **Phase 1 Deployment** - Successfully deployed Nix configuration v2.0
   - Configuration deployed without errors
   - All services active before reboot
   - Node identical to beelink-1 and beelink-2 (same hardware)

2. **Reboot** - Node rebooted to activate new configuration
   - Expected: Come back online in ~90 seconds
   - Actual: Node never became accessible

3. **Current State**
   - No SSH response (connection timeout)
   - No ping response (host unreachable)
   - Kubernetes shows: Status = Unknown, Reason = NodeStatusUnknown
   - Last contact: During Phase 1 deployment before reboot

## Investigation Steps

### Network Connectivity

```bash
# Ping test
ping -c 4 172.18.2.23
# Result: 100% packet loss

# SSH test
ssh bwright@beelink-3.cloudydad.com
# Result: Connection timeout

# Check from cluster
kubectl get node beelink-3 -o yaml
# Result: Status Unknown, Ready condition = Unknown
```

### Cluster Status

```bash
kubectl get nodes
# NAME          STATUS     ROLES    AGE    VERSION
# beelink-3     NotReady   <none>   426d   v1.32.11+k3s3

kubectl describe node beelink-3
# Conditions:
#   Ready            Unknown   ... NodeStatusUnknown
# Last heartbeat: [time of last successful contact]
```

## Likely Causes

Given that:

1. Phase 1 deployment was successful
2. Configuration was identical to working beelink-1 and beelink-2
3. No errors during deployment
4. Complete loss of network connectivity

**Most likely causes:**

1. **Hardware failure** - Power supply, motherboard, RAM
2. **Boot failure** - GRUB misconfiguration, corrupted initramfs
3. **Network hardware** - Failed NIC, disconnected cable
4. **Power issue** - Lost power during/after reboot, PSU failure

**Unlikely causes:**

- Nix configuration issue (would affect other beelinks)
- Systemd service failure (would still respond to ping/SSH)
- Kernel panic (would show on console)

## Recovery Steps

### Step 1: Physical Inspection

**Required:** Physical access to the node

1. **Check power and boot status**
   ```
   - Is the power light on?
   - Are there any beeps or error codes?
   - Do fans spin up?
   ```

2. **Check network connectivity**
   ```
   - Is network cable connected?
   - Do NIC LEDs show activity?
   - Try different cable/port
   ```

3. **Access console**
   ```
   - Connect monitor and keyboard
   - Check boot messages
   - Look for kernel panic or boot errors
   ```

### Step 2: Console Diagnostics

If console access is available:

1. **Check boot process**
   ```bash
   # Check GRUB menu appears
   # Watch for kernel panic messages
   # Check if systemd starts
   ```

2. **Emergency mode / single user mode**
   ```bash
   # At GRUB, press 'e' to edit boot entry
   # Add: systemd.unit=emergency.target
   # Boot and diagnose
   ```

3. **Check network configuration**
   ```bash
   # Once booted (any mode)
   ip addr show
   ip route show
   systemctl status NetworkManager
   journalctl -u NetworkManager
   ```

4. **Check Nix services**
   ```bash
   systemctl status system-manager.target
   systemctl status k3s-agent.service
   journalctl -xe
   ```

### Step 3: Recovery Options

#### Option A: Fix in place (if bootable)

```bash
# 1. Fix network if needed
sudo systemctl restart NetworkManager
sudo ip addr add 172.18.2.23/24 dev lan0  # or correct interface

# 2. Verify Nix configuration
cd /etc/nix-system
sudo system-manager switch --flake .

# 3. Verify services
sudo systemctl status k3s-agent multipathd iscsid

# 4. Rejoin cluster
sudo systemctl restart k3s-agent
kubectl get node beelink-3  # Should show Ready within 60 seconds
```

#### Option B: Rollback Nix configuration

```bash
# If Nix Phase 1 is suspected (unlikely)
sudo system-manager switch --rollback

# Verify
sudo systemctl status k3s-agent
```

#### Option C: Emergency Ansible restoration

```bash
# From control machine
cd ~/cloudydad-data-center
uvx --from ansible-core ansible-playbook \
  playbooks/site.yml \
  --tags system,k3s \
  --limit beelink-3

# This will:
# - Reinstall k3s via Ansible (old method)
# - Restore basic system configuration
# - Should bring node back online
```

#### Option D: Full reinstall

If hardware is OK but OS is corrupted:

1. Backup any critical data if accessible
2. Reinstall Debian 12 from USB
3. Run Ansible bootstrap:
   ```bash
   cd ~/cloudydad-data-center
   # Update inventory if needed
   make site NODE=beelink-3
   make bootstrap-nix NODE=beelink-3
   ```

### Step 4: Hardware Replacement

If hardware failure is confirmed:

1. **Replace failed component** (PSU, RAM, NIC, etc.)
2. **Test boot** before reinstalling OS
3. **Follow Option D** (Full reinstall) above

## Temporary Workaround

The cluster is fully operational with 6/7 nodes:

- 3/3 control plane nodes operational
- 3/4 worker nodes operational (beelink-1, beelink-2, mini)

**Impact:** Low - Sufficient worker capacity for current workloads

**Actions:**

- Monitor cluster resource usage
- Investigate beelink-3 when physical access available
- Consider removing from cluster if unrecoverable

## Prevention

To prevent similar issues in the future:

1. **Serial console access** - Configure IPMI/iLO/iDRAC if available
2. **Staged reboots** - One worker at a time, verify before continuing
3. **Monitoring** - Alert on node NotReady status
4. **Boot verification** - Check for successful boot messages before marking
   deployment complete

## Related Issues

- Phase 1 deployment succeeded on 6/7 nodes
- Other beelinks (beelink-1, beelink-2) working correctly with identical
  hardware/config
- rpi06 has multipathd issue but is operational (separate issue)

## Status Updates

**February 16, 2026 - 12:23 UTC** - Initial issue detected after Phase 1 reboot

- Node became unresponsive after Phase 1 Nix deployment reboot
- Could not SSH, no ping response
- Cluster showed node as NotReady

**February 16, 2026 - 13:54 UTC** - Node came back online after multiple reboots

- Node experienced 3 reboots between 12:23-13:54 (likely manual intervention)
- Successfully booted with Phase 1 Nix configuration
- All services active (k3s-agent, multipathd, iscsid)

**February 16, 2026 - 17:47 UTC** - Recovery and cleanup completed ✅

**Root Cause Analysis:**

- **NOT a Nix configuration issue** - Config v2.0 working correctly
- **NOT an OOM issue** - 16GB RAM, only 765MB used
- **Likely cause:** Unknown boot/hardware issue requiring manual reboot
- **Secondary issue:** /var partition at 83% (disk space pressure)

**Recovery Actions Taken:**

1. ✅ Verified Nix configuration v2.0 active and correct
2. ✅ Verified all Nix services running (k3s-agent, multipathd, iscsid)
3. ✅ Deleted 7 ghost pods stuck in Unknown/CreateContainerError state
4. ✅ Cleaned journalctl logs (freed 1.5GB)
5. ✅ Cleaned apt cache (minimal gain)
6. ✅ Disk space improved: /var 83% → 70% (5.0GB free)

**Current Status:**

- **Node:** Ready and operational
- **Uptime:** 3h 53m (since 13:54 UTC)
- **Services:** All active and healthy
- **Disk Space:** Root 51%, /var 70% (healthy)
- **Memory:** 765MB/16GB used (14GB available)
- **Load:** 0.56 0.22 0.11 (normal)

**Cluster Status:**

- 7/7 nodes now Ready and operational
- All control plane nodes healthy
- All worker nodes healthy
- Phase 1 deployment **100% successful**

---

**Lessons Learned:**

1. Multiple reboots after Phase 1 deployment may indicate boot issues unrelated
   to Nix
2. /var disk pressure (83%) should be addressed proactively
3. Ghost pods from failed nodes should be force-deleted after recovery
4. Journal log rotation should be configured more aggressively

**Preventative Measures:**

1. ✅ Implemented journalctl vacuum (7-day retention)
2. 📋 TODO: Configure automated journal size limits in systemd
3. 📋 TODO: Add monitoring alerts for /var >75%
4. 📋 TODO: Implement automated pod cleanup script
5. 📋 TODO: Consider adding serial console access for remote recovery
