# Nix Phase 1 Migration - Test Plan

**Configuration Version:** 2.0\
**Test Date:** 2026-02-16\
**Tester:** _____________

---

## Pre-Deployment Checklist

Before deploying Phase 1 to any node, verify:

- [ ] All 7 nodes currently operational and healthy
- [ ] Cluster status shows all nodes "Ready"
- [ ] No ongoing maintenance or critical workloads
- [ ] Backup of current configurations exists
- [ ] Access to node console/IPMI (if available)

## Test Node Selection

**Recommended:** `beelink-2` (172.18.2.22)

**Rationale:**

- ✅ Worker node (non-critical)
- ✅ Already migrated to Nix (v1.0)
- ✅ x86_64 architecture (easier to debug)
- ✅ Confirmed working after initial migration
- ✅ Not running critical infrastructure pods

**Alternatives:** `beelink-1`, `beelink-3`, `mini`

---

## Phase 1: Single Node Deployment

### Step 1: Pre-Deployment Snapshot

```bash
# On test node
ssh bwright@beelink-2.cloudydad.com

# Check current state
sudo systemctl status k3s-agent.service
sudo systemctl status system-manager.target
kubectl get nodes
kubectl get pods -A | grep beelink-2

# List current packages
which k3s kubectl htop iotop iftop mosh rg

# Check storage services (should not exist yet)
sudo systemctl status multipathd.service || echo "Not found (expected)"
sudo systemctl status iscsid.service || echo "Not found (expected)"

# Record current generation
nix profile history --profile /nix/var/nix/profiles/system-manager
```

**Record baseline:**

- Current generation number: __________
- K3s service status: __________
- Node status: __________
- Number of pods on node: __________

### Step 2: Deploy Phase 1 Configuration

```bash
# From control machine
cd ~/cloudydad-data-center
make bootstrap-nix NODE=beelink-2
```

**Expected output:**

```
TASK [nix-bootstrap : Deploy configuration.nix] ********************************
changed: [beelink-2]

TASK [nix-bootstrap : Activate Nix configuration] ******************************
changed: [beelink-2]

PLAY RECAP **********************************************************************
beelink-2                  : ok=X    changed=2    unreachable=0    failed=0
```

**Actual output:**

```
[PASTE OUTPUT HERE]
```

**Duration:** __________ minutes

### Step 3: Immediate Post-Deployment Verification

```bash
# On test node
ssh bwright@beelink-2.cloudydad.com

# 1. Check system-manager
sudo systemctl status system-manager.target
# Expected: active (exited)
# Actual: __________

# 2. Check storage services (NEW in Phase 1)
sudo systemctl status multipathd.service
# Expected: active (running)
# Actual: __________

sudo systemctl status iscsid.service
# Expected: active (running)
# Actual: __________

# 3. Check k3s service
sudo systemctl status k3s-agent.service
# Expected: active (running)
# Actual: __________

# 4. Check node status
kubectl get nodes | grep beelink-2
# Expected: Ready
# Actual: __________

# 5. Check pods on this node
kubectl get pods -A -o wide | grep beelink-2
# Expected: All Running
# Actual: __________

# 6. Verify new packages
which iftop mosh nvim rg dig lsscsi multipath
# Expected: All found
# Actual: __________

# 7. Check multipath.conf (NEW in Phase 1)
cat /etc/multipath.conf
# Expected: user_friendly_names yes, find_multipaths yes
# Actual: __________

# 8. Verify service dependencies
systemctl list-dependencies k3s-agent.service | grep -E "(multipath|iscsi)"
# Expected: Shows multipathd.service and iscsid.service
# Actual: __________

# 9. Check generation number
nix profile history --profile /nix/var/nix/profiles/system-manager
# Expected: New generation (higher number)
# Actual: __________
```

**Pass/Fail:** __________

### Step 4: Test Idempotency

```bash
# On test node
cd /etc/nix-system
sudo system-manager switch --flake .
```

**Expected behavior:**

- Completes in ~15 seconds
- No service restarts
- No "changed" messages (or minimal changes)

**Actual behavior:**

```
[PASTE OUTPUT HERE]
```

**Duration:** __________ seconds

**Pass/Fail:** __________

### Step 5: Test Rollback

```bash
# On test node
sudo system-manager switch --rollback
```

**Expected behavior:**

- Rolls back to previous generation
- K3s service remains active
- Node stays Ready

**Verification:**

```bash
sudo systemctl status k3s-agent.service
kubectl get nodes | grep beelink-2
nix profile history --profile /nix/var/nix/profiles/system-manager
```

**Pass/Fail:** __________

### Step 6: Re-Deploy Phase 1 (After Rollback)

```bash
# On test node
cd /etc/nix-system
sudo system-manager switch --flake .
```

**Expected behavior:**

- Switches forward to latest generation
- Storage services restart
- K3s remains stable

**Pass/Fail:** __________

---

## Phase 2: Soak Test (24 Hours)

Monitor the test node for 24 hours to verify stability.

### Monitoring Checklist

**Every 6 hours, check:**

#### Check 1 (Hour 0)

- [ ] Node status: __________
- [ ] K3s service: __________
- [ ] Storage services: __________
- [ ] Pod count: __________
- [ ] Any errors in journal: __________

#### Check 2 (Hour 6)

- [ ] Node status: __________
- [ ] K3s service: __________
- [ ] Storage services: __________
- [ ] Pod count: __________
- [ ] Any errors in journal: __________

#### Check 3 (Hour 12)

- [ ] Node status: __________
- [ ] K3s service: __________
- [ ] Storage services: __________
- [ ] Pod count: __________
- [ ] Any errors in journal: __________

#### Check 4 (Hour 18)

- [ ] Node status: __________
- [ ] K3s service: __________
- [ ] Storage services: __________
- [ ] Pod count: __________
- [ ] Any errors in journal: __________

#### Check 5 (Hour 24)

- [ ] Node status: __________
- [ ] K3s service: __________
- [ ] Storage services: __________
- [ ] Pod count: __________
- [ ] Any errors in journal: __________

### Soak Test Commands

```bash
# Check node health
kubectl get nodes beelink-2 -o wide

# Check services
ssh bwright@beelink-2.cloudydad.com "sudo systemctl status k3s-agent multipathd iscsid"

# Check for errors
ssh bwright@beelink-2.cloudydad.com "sudo journalctl --since '1 hour ago' --priority err"

# Check resource usage
ssh bwright@beelink-2.cloudydad.com "htop -d 50" # Press q to quit
```

**Soak Test Result:** Pass / Fail

**Issues Found:** ___________________________________

---

## Phase 3: Deploy to Additional Worker Nodes

After successful soak test on beelink-2, deploy to remaining workers one at a
time.

### Deployment Order

1. **beelink-1** (172.18.2.21)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________

2. **beelink-3** (172.18.2.23)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________

3. **mini** (172.18.2.1)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________

### Deployment Commands

```bash
# Deploy to single node
make bootstrap-nix NODE=beelink-1
make bootstrap-nix NODE=beelink-3
make bootstrap-nix NODE=mini
```

**Wait 30 minutes between deployments** to monitor for issues.

---

## Phase 4: Deploy to Master Nodes

After all workers are stable, deploy to masters one at a time.

### Deployment Order

**CRITICAL:** Deploy to masters one at a time with 1-hour soak between each.

1. **rpi06** (172.18.2.16)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________
   - Wait 1 hour: [ ]

2. **rpi07** (172.18.2.17)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________
   - Wait 1 hour: [ ]

3. **surfacebook** (172.18.2.2)
   - Deployed: [ ] Date/Time: __________
   - Status: [ ] Pass / [ ] Fail
   - Notes: ___________________________________

### Master Node Verification

After each master deployment, verify:

```bash
# Check etcd health
kubectl get --raw=/healthz
kubectl get cs

# Check API server responsiveness
kubectl get nodes
kubectl get pods -A

# Check master services
ssh bwright@<master-node> "sudo systemctl status k3s multipathd iscsid"
```

---

## Phase 5: Final Cluster Verification

After all nodes deployed, perform comprehensive cluster check.

### Final Verification Checklist

```bash
# All nodes Ready
kubectl get nodes -o wide
# Expected: All 7 nodes Ready, k3s v1.32.11+k3s3
# Actual: __________

# All pods Running
kubectl get pods -A
# Expected: All Running (except completed jobs)
# Actual: __________

# Check storage classes (uses storage services)
kubectl get sc
# Expected: All available
# Actual: __________

# Check PVCs (uses storage services)
kubectl get pvc -A
# Expected: All Bound
# Actual: __________

# Verify storage services on all nodes
ansible all:!rpi05 -m shell -a "systemctl is-active multipathd iscsid" -b
# Expected: active, active (all nodes)
# Actual: __________

# Check Nix generations on all nodes
ansible all:!rpi05 -m shell -a "nix profile history --profile /nix/var/nix/profiles/system-manager | tail -1" -b
# Expected: Latest generation on all nodes
# Actual: __________

# Verify multipath.conf on all nodes
ansible all:!rpi05 -m shell -a "cat /etc/multipath.conf" -b
# Expected: user_friendly_names yes, find_multipaths yes
# Actual: __________
```

**Final Result:** Pass / Fail

---

## Rollback Plan (If Needed)

If Phase 1 causes critical issues:

### Option 1: Rollback Single Node

```bash
ssh bwright@<node-hostname>
sudo system-manager switch --rollback
sudo systemctl status k3s-agent.service  # or k3s.service for masters
```

### Option 2: Rollback All Nodes

```bash
cd ~/cloudydad-data-center
ansible all:!rpi05 -m shell -a "cd /etc/nix-system && system-manager switch --rollback" -b
```

### Option 3: Re-deploy v1.0 Configuration

```bash
cd ~/cloudydad-data-center
git checkout 136c7771  # v1.0 config
make bootstrap-nix NODE=<hostname>
git checkout develop
```

---

## Sign-Off

**Test Completed By:** _______________\
**Date:** _______________\
**Overall Result:** Pass / Fail

**Approval for Production:**

- [ ] All test phases passed
- [ ] No critical issues found
- [ ] Cluster stable for 24+ hours
- [ ] Documentation updated

**Notes:**

---

---

---

**Approved By:** _______________\
**Date:** _______________
