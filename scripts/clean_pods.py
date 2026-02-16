#!/usr/bin/env python3

import subprocess
import json
import sys


def delete_problematic_pods():
    """Delete Evicted, CrashLoopBackOff, Error, and restarted pods."""
    # Get all pods in JSON format
    cmd = ["kubectl", "get", "pods", "-o", "json", "-A"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting pods: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    deleted_count = 0

    for item in data.get("items", []):
        metadata = item.get("metadata", {})
        namespace = metadata.get("namespace", "")
        pod_name = metadata.get("name", "")

        # Skip cloudnative-pg pods (like in original script)
        if "cloudnative-pg" in namespace:
            continue

        # Get pod status
        status = item.get("status", {})
        phase = status.get("phase", "")
        reason = status.get("reason", "")
        container_statuses = status.get("containerStatuses", [])
        conditions = status.get("conditions", [])

        # Check for restart count
        restart_count = 0
        if container_statuses:
            restart_count = container_statuses[0].get("restartCount", 0)

        should_delete = False
        delete_reason = ""

        # Check pod phase and reason (for evicted pods)
        if phase == "Failed" and reason == "Evicted":
            should_delete = True
            delete_reason = "Evicted"

        # Check container statuses for problematic states
        if not should_delete:
            for container_status in container_statuses:
                state = container_status.get("state", {})
                if "waiting" in state:
                    reason = state["waiting"].get("reason", "")
                    if reason in [
                        "Evicted",
                        "CrashLoopBackOff",
                        "Error",
                        "ImagePullBackOff",
                        "ContainerStatusUnknown",
                    ]:
                        should_delete = True
                        delete_reason = reason
                        break
                elif "terminated" in state:
                    reason = state["terminated"].get("reason", "")
                    if reason in ["Completed", "ContainerStatusUnknown"]:
                        should_delete = True
                        delete_reason = reason
                        break

        # Check pod conditions for additional reasons
        if not should_delete:
            for condition in conditions:
                if (
                    condition.get("type") == "Ready"
                    and condition.get("status") == "False"
                ):
                    condition_reason = condition.get("reason", "")
                    if condition_reason in ["ContainersNotReady", "PodFailed"]:
                        # Check if this is a problematic pod based on message
                        message = condition.get("message", "").lower()
                        if "evicted" in message or "diskpressure" in message:
                            should_delete = True
                            delete_reason = "Evicted"
                            break

        # Delete pods that have been restarted (restartCount > 0)
        if not should_delete and restart_count > 0:
            should_delete = True
            delete_reason = f"restarted ({restart_count} times)"

        if should_delete:
            try:
                delete_cmd = ["kubectl", "delete", "pod", pod_name, "-n", namespace]
                subprocess.run(delete_cmd, check=True)
                print(
                    f"Deleted pod {pod_name} in namespace {namespace} (reason: {delete_reason})"
                )
                deleted_count += 1
            except subprocess.CalledProcessError as e:
                print(f"Failed to delete pod {pod_name}: {e}")

    if deleted_count == 0:
        print(
            "No problematic pods (Evicted, CrashLoopBackOff, Error, restarted, etc.) found to delete."
        )
    else:
        print(f"Successfully deleted {deleted_count} problematic pods.")


if __name__ == "__main__":
    delete_problematic_pods()
