# Troubleshooting: surfacebook LVM Boot Cascade

**Node:** surfacebook (172.18.2.2)\
**Role:** k3s master (laptop)\
**Architecture:** x86_64\
**OS:** Debian GNU/Linux 12 (bookworm)\
**Status:** Stable\
**Issue Date:** June 5–7, 2026

---

## Issue Summary

After 16+ days of uptime, rebooting the surfacebook produced a cascade of
`[DEPEND] Dependency failed` lines for every service ordering against
`local-fs.target`. All non-root LVM mounts (home, var, tmp, boot, boot/efi)
timed out simultaneously at the 90-second mark.

The root cause was **not** an LVM failure — it was a race between the Surface
Book's inherently slow NVMe drive initialization (~90s) and systemd's
`DefaultTimeoutStartSec=90s` mount-unit timeout. After an unclean shutdown, ext4
journal recovery on `/home` added a few extra seconds, pushing past the timeout
boundary and cascading all non-root mounts into `[DEPEND]` failure.

## Symptoms

Console output during the failed boot:

```
[DEPEND] Dependency failed for ...
[ TIME ] Timed out waiting for device dev-mapper-surfacebook--vg-home.device
[DEPEND] Dependency failed for home.mount - /home
```

All non-root mount and service units fail with `[DEPEND]` status.

## Root Cause

### Hardware: Slow NVMe Initialization

The Surface Book uses a **SAMSUNG MZFLW128HEGR** NVMe SSD (PCIe 3.0 x2). This
drive is inherently slow to initialize — the LVM root device
(`dev-mapper-surfacebook--vg-root.device`) consistently takes **~90 seconds** to
appear in userspace. This is visible in every boot:

```
systemd-analyze blame:
1min 31.570s systemd-udev-settle.service
1min 30.455s dev-mapper-surfacebook--vg-root.device
```

`systemd-udev-settle.service` (pulled in by `multipathd.service`) waits for all
pending udev events to be processed — effectively the same ~90s as the NVMe
drive initialization.

### Why It Fails After Unclean Shutdown

1. System boots, all mount-unit jobs are created at t=0 with the default 90s
   `JobTimeoutUSec`.
2. NVMe drive takes ~90s to initialize — during this time udev events are being
   processed and the `/dev/mapper/` LVM devices haven't appeared yet.
3. At ~90s, devices finally appear. `systemd-fsck@.service` runs ext4 journal
   recovery on each dirty filesystem.
4. After a clean shutdown, fsck completes in ~50ms — mounts succeed within the
   90s window.
5. After an unclean shutdown (e.g., 16+ days uptime + power loss), fsck journal
   recovery on `/home` takes extra seconds. Combined with the 90s NVMe delay,
   this pushes past the **90s mount-unit timeout**, causing all non-root mounts
   to fail with `[DEPEND]`.

### Why multipathd's udev-settle Is Protective

`multipathd.service` is the only consumer of `systemd-udev-settle.service`. This
service has `Before=sysinit.target`, creating a natural ordering barrier:

- Mount-unit jobs are created at boot start, timeout clock ticking.
- `systemd-udev-settle` blocks `sysinit.target` from completing.
- udev events process during this time (NVMe initializing).
- When udev-settle completes at ~90s, devices are available.
- Mount units complete within milliseconds — just inside the 90s window.

Without multipathd (and its udev-settle dependency), mount-unit jobs would still
be created at t=0 with a 90s timeout, but no barrier would exist. The outcome
would be the same race — or worse, since udev-settle provides synchronization.

### What Did NOT Work

**`x-systemd.automount` on `/var`**: This approach (first attempted fix) caused
a systemd ordering cycle that broke `udevd`, preventing ALL block devices from
appearing. The boot was unrecoverable until the initramfs was used to edit
fstab.

## Recovery Steps

### Step 1: Get a shell

Options:

1. **Boot with `break=mount`** (used successfully): Edit the kernel command
   line, append `break=mount`. Boot lands at an initramfs shell prompt.
2. **Single-user mode** (`single`): Root shell without requiring
   `local-fs.target`.
3. **Wait for maintenance prompt**: Only works if keyboard input is accepted
   (USB keyboard recommended for Surface Book).

### Step 2: Mount root and fix fstab

At the `break=mount` initramfs prompt:

```bash
# Create a mount point and check the device
mkdir -p /mnt
ls -la /dev/dm-*               # /dev/dm-0 -> ../dm-0 (symlink)
modprobe ext4                  # ensure ext4 module loaded
mount -t ext4 /dev/dm-0 /mnt   # mount root LV

# Fix fstab (remove the broken automount option)
sed -i 's/defaults,x-systemd.automount/defaults/' /mnt/etc/fstab
sync
umount /mnt
exit                           # continue boot
```

The root LV may appear as `/dev/dm-0` or via the LVM name path
`/dev/surfacebook-vg/root`.

### Step 3: Apply hardening via Ansible

The `system` role in `playbooks/system.yml` codifies all hardening, gated by the
`laptop` group in `inventory/cloudydad/hosts.ini`:

```bash
ansible-playbook playbooks/system.yml --limit surfacebook --check  # dry run
ansible-playbook playbooks/system.yml --limit surfacebook          # apply
```

Or scoped to just the laptop tasks:

```bash
ansible-playbook playbooks/system.yml --limit surfacebook --tags laptop
```

## Diagnosis (read-only commands)

```bash
# Boot timing
systemd-analyze blame                              # identify slow units
systemd-analyze critical-chain local-fs.target     # mount dependency chain
systemd-analyze time                               # firmware/loader/kernel split

# Check the multipathd/udev-settle relationship
systemctl show sysinit.target --property=After,Before
systemctl list-dependencies systemd-udev-settle.service

# LVM health
lvm lvs
pvs
lsblk -o NAME,TYPE,SIZE,MODEL,ROTA

# Check NVMe power management (known issue with Samsung drives)
cat /sys/module/nvme_core/parameters/default_ps_max_latency_us
#    100000 = can enter deep power states (up to 100ms exit latency)
#       0   = disable deep power states (may improve init time)

# Previous boot fsck evidence
journalctl -b -1 | grep -iE "recovering journal|fsck"

# Current systemd timeout defaults
systemctl show --property=DefaultTimeoutStartSec
```

## Prevention / Hardening

The Ansible role `roles/system/tasks/laptop.yml` applies four independent
measures:

### 1. `nofail` on non-critical mounts

`/home`, `/tmp`, `/boot`, `/boot/efi` have `nofail` appended to their fstab
options. A slow fsck on these cannot block the boot.

`/var` is **not** given `nofail` — it remains strict because k3s and system
services depend on `/var` being available. It uses a timeout extension instead
(see #4).

### 2. `x-systemd.device-timeout=180s` on `/var`

The `/var` mount unit's job timeout for waiting on its LVM device is extended
from 90s to 180s. This covers the worst case:

- 90s NVMe initialization
-
  - 30s ext4 journal recovery on `/var` (after unclean shutdown)
-
  - Safety margin

The mount remains strict (no `nofail`, no `automount`) — it just has more time.

### 3. `systemd-fsck@.service` timeout extended to 5 minutes

Applies systemd-wide to all filesystem checks at boot:

```
[Service]
TimeoutStartSec=5min
```

File:
`roles/system/files/etc/systemd/system/systemd-fsck@.service.d/timeout.conf`

### 4. Mount-point directory creation

The `/boot/efi` mount-point directory does not exist on a fresh Debian LVM
install. The role creates all non-root mount-point directories to prevent mount
failures even when the device appears.

## Files Changed

| File                                                                         | Description                                                                           |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `roles/system/tasks/laptop.yml`                                              | fstab hardening (nofail loop, device-timeout for /var, mount-point dirs, fsck dropin) |
| `roles/system/files/etc/systemd/system/systemd-fsck@.service.d/timeout.conf` | 5-min fsck timeout dropin                                                             |
| `inventory/cloudydad/hosts.ini`                                              | Defines `[laptop]` group (surfacebook)                                                |

## What We Learned

- **The NVMe drive is the bottleneck**: ~90s initialization is a hardware
  characteristic of the Surface Book's SAMSUNG MZFLW128HEGR SSD. Cannot be
  eliminated, only accommodated.
- **multipathd's udev-settle is protective**: Disabling it would remove the
  synchronization barrier, not speed up device initialization.
- **`x-systemd.automount` causes ordering cycles**: Do not use on `/var` or any
  filesystem that system services depend on.
- **`nofail` is safe for non-critical mounts**: `/home`, `/tmp`, `/boot`,
  `/boot/efi` can be lazy-mounted without affecting system services.
- **`x-systemd.device-timeout=` is the correct tool for critical mounts**:
  Extends only the device-wait phase without changing mount strictness.
- **The iSCSI disk (`/dev/sda`)** is a Democratic CSI volume used by k3s.
  open-iscsi must remain enabled.

## Status

- **June 5, 2026 17:38 UTC** — Initial diagnosis, `nofail` + fsck timeout
  applied manually
- **June 5, 2026** — `x-systemd.automount` on `/var` applied (BROKEN — caused
  ordering cycle, recovered via initramfs)
- **June 7, 2026** — Root cause fully understood: 90s NVMe init + 90s timeout
  race. Final fix: `nofail` + `device-timeout=180s` + fsck dropin. All hardening
  codified in Ansible. Doc updated.
