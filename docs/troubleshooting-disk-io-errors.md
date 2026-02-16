# Runbook: Disk I/O Errors on Kubernetes Node

## Overview

This runbook addresses disk failures and I/O errors detected by
node-problem-detector on Kubernetes nodes, specifically for EXT4 filesystem
errors and Buffer I/O errors.

## Detection

**Alert Names:**

- `NodeProblemIOError` - Buffer I/O errors detected
- `NodeProblemExt4Error` - EXT4 filesystem errors detected

**Symptoms:**

- Node-problem-detector reports errors in kernel logs
- Prometheus alerts firing with `severity: warning`
- Kernel messages show "Buffer I/O error on dev sdX"
- EXT4-fs errors in system logs

## Initial Diagnosis

### 1. Identify Affected Node and Disks

```bash
# Check node events for disk errors
kubectl describe node <node-name> | grep -A 50 "Events:"

# Look for patterns like:
# - Warning  IOError    Xs   kernel-monitor  Buffer I/O error on dev sdb
# - Warning  Ext4Error  Xs   kernel-monitor  EXT4-fs error (device sdb)
```

### 2. Check Node Status

```bash
# Verify node is still Ready
kubectl get node <node-name> -o yaml | grep -A 20 "conditions:"

# Check for disk pressure or other issues
kubectl top node <node-name>
```

### 3. Identify Affected Workloads

```bash
# List all pods on the affected node
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name>

# Check if any PVCs are bound to local storage on this node
kubectl get pvc --all-namespaces -o wide | grep <node-name>

# For iSCSI/CSI storage, check volume attachments
kubectl get volumeattachment | grep <node-name>
```

## Classification of Disk Errors

### Type A: Local Disk Failure (Direct Attached Storage)

**Indicators:**

- Errors on devices like sda, sdb, nvme0n1
- local-path-provisioner or hostPath volumes affected
- Node has DiskPressure condition

### Type B: iSCSI/Network Storage Issues

**Indicators:**

- democratic-csi-iscsi-node pod running on node
- Storage class is `truenas-iscsi-csi` or similar
- Errors may indicate network connectivity or TrueNAS issues
- Multiple nodes may report similar errors

### Type C: Transient/Recoverable Errors

**Indicators:**

- Single isolated error event
- No ongoing error stream
- Filesystem remounts successfully
- Node conditions remain healthy

## Remediation Steps

### For Type A (Local Disk Failure)

**Immediate Actions:**

1. **Cordon the node** to prevent new workloads:
   ```bash
   kubectl cordon <node-name>
   ```

2. **Drain critical workloads** (if disk is failing):
   ```bash
   kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
   ```

3. **Physical node access** - SSH to the node and check disk health:
   ```bash
   # Check SMART status
   sudo smartctl -a /dev/sdX

   # Check filesystem
   sudo fsck -n /dev/sdX  # Read-only check first

   # Check dmesg for ongoing errors
   sudo dmesg | grep -i "error\|fail\|sdX"
   ```

4. **Backup data** if disk is recoverable but failing

5. **Replace disk** and restore from backup

### For Type B (iSCSI/Network Storage)

**Immediate Actions:**

1. **Check CSI node pod logs**:
   ```bash
   kubectl logs -n storage democratic-csi-iscsi-node-<pod-id> -c csi-driver
   ```

2. **Verify TrueNAS/iSCSI target health**:
   - Access TrueNAS web UI
   - Check pool status for degradation
   - Verify network connectivity between node and TrueNAS

3. **Check multipath status** (if configured):
   ```bash
   kubectl debug node/<node-name> -it --image=busybox -- multipath -ll
   ```

4. **Restart CSI node pod** to reconnect:
   ```bash
   kubectl delete pod -n storage democratic-csi-iscsi-node-<pod-id>
   ```

### For Type C (Transient Errors)

**Actions:**

1. **Monitor only** - If errors are isolated and node is healthy:
   - Watch for repeated occurrences
   - Check if errors correlate with high load

2. **Run filesystem check** during maintenance window:
   ```bash
   # Schedule maintenance and unmount filesystem
   sudo fsck -y /dev/sdX
   ```

## Verification

### Confirm Resolution

```bash
# Check node events are no longer showing errors
kubectl describe node <node-name> | tail -30

# Verify all pods are running normally
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name>

# Check node conditions are healthy
kubectl get node <node-name> -o jsonpath='{.status.conditions}'

# Monitor alerts in Grafana - should resolve within 5-10 minutes
```

### Post-Incident Actions

1. **Document the incident** with:
   - Root cause
   - Affected workloads
   - Resolution steps taken

2. **Review monitoring thresholds** if false positives occur

3. **Consider disk replacements** for hardware failures

4. **Update this runbook** with lessons learned

## Prevention

### For Local Storage

- Use RAID configurations for redundancy
- Monitor SMART data proactively
- Implement disk health monitoring (node-exporter with textfile collector)

### For iSCSI Storage

- Configure multipath for redundancy
- Monitor TrueNAS pool health
- Ensure redundant network paths
- Set up alerting on TrueNAS itself

## Escalation

**Escalate to:**

- Infrastructure team if hardware replacement needed
- Storage team if iSCSI/TrueNAS issues persist
- Vendor support if under warranty

**When to escalate:**

- Data loss occurred or imminent
- Multiple disks failing simultaneously
- Node remains NotReady after remediation
- Errors persist after disk replacement

## References

- [Node Problem Detector Documentation](https://github.com/kubernetes/node-problem-detector)
- [Kubernetes Node Conditions](https://kubernetes.io/docs/concepts/architecture/nodes/#condition)
- [TrueNAS Documentation](https://www.truenas.com/docs/)
- [Democratic CSI Documentation](https://github.com/democratic-csi/democratic-csi)
