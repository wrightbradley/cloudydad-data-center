#!/bin/bash

set -euo pipefail

API_VIP="172.18.255.253"
MASTERS=("172.18.2.2" "172.18.2.16" "172.18.2.17")
PORT="6443"
ITERATIONS="${1:-100}"
CONCURRENT="${2:-10}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

results_dir=$(mktemp -d)
trap "rm -rf $results_dir" EXIT

echo "=========================================="
echo "K3s API Server Stress Test"
echo "=========================================="
echo "VIP: $API_VIP"
echo "Masters: ${MASTERS[*]}"
echo "Iterations: $ITERATIONS"
echo "Concurrent requests: $CONCURRENT"
echo ""

test_tcp_port() {
  local host=$1
  local port=$2
  local timeout=2

  if timeout "$timeout" bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
    return 0
  else
    return 1
  fi
}

test_healthz() {
  local host=$1
  local start end duration

  start=$(date +%s%N)
  if curl -k -s -o /dev/null -w "%{http_code}" --connect-timeout 2 --max-time 5 "https://$host:$PORT/healthz" 2>/dev/null | grep -q "200\|401"; then
    end=$(date +%s%N)
    duration=$(((end - start) / 1000000))
    echo "0 $duration"
    return 0
  else
    echo "1 0"
    return 1
  fi
}

run_healthz_test() {
  local host=$1
  local count=$2
  local success=0
  local fail=0
  local total_time=0

  for ((i = 1; i <= count; i++)); do
    read -r rc duration < <(test_healthz "$host")
    if [[ $rc -eq 0 ]]; then
      ((success++))
      ((total_time += duration))
    else
      ((fail++))
    fi
    printf "\r${host}: Test $i/$count - Success: $success, Fail: $fail"
  done
  echo ""

  local avg_time=0
  if [[ $success -gt 0 ]]; then
    avg_time=$((total_time / success))
  fi

  echo "$host:$success:$fail:$avg_time" >>"$results_dir/healthz_results"
}

run_tcp_test() {
  local host=$1
  local count=$2
  local success=0
  local fail=0

  for ((i = 1; i <= count; i++)); do
    if test_tcp_port "$host" "$PORT"; then
      ((success++))
    else
      ((fail++))
    fi
    printf "\r${host}: Test $i/$count - Success: $success, Fail: $fail"
  done
  echo ""

  echo "$host:$success:$fail" >>"$results_dir/tcp_results"
}

echo "=========================================="
echo "Phase 1: TCP Port Connectivity Test"
echo "=========================================="

echo -e "${YELLOW}Testing TCP port $PORT connectivity...${NC}"
echo ""

for host in "$API_VIP" "${MASTERS[@]}"; do
  run_tcp_test "$host" "$ITERATIONS" &
done
wait

echo ""
echo "TCP Port Test Results:"
echo "----------------------"
while IFS=: read -r host success fail; do
  total=$((success + fail))
  pct=$((success * 100 / total))
  if [[ $fail -eq 0 ]]; then
    echo -e "${GREEN}$host${NC}: $success/$total (${pct}%)"
  else
    echo -e "${RED}$host${NC}: $success/$total (${pct}%) - FAILED: $fail"
  fi
done <"$results_dir/tcp_results" | sort

echo ""
echo "=========================================="
echo "Phase 2: HTTPS /healthz Endpoint Test"
echo "=========================================="

echo -e "${YELLOW}Testing /healthz endpoint...${NC}"
echo ""

for host in "$API_VIP" "${MASTERS[@]}"; do
  run_healthz_test "$host" "$ITERATIONS" &
done
wait

echo ""
echo "Healthz Test Results:"
echo "---------------------"
printf "%-18s %10s %10s %10s %10s\n" "Host" "Success" "Fail" "Success%" "Avg(ms)"
printf "%-18s %10s %10s %10s %10s\n" "----" "-------" "----" "--------" "--------"
while IFS=: read -r host success fail avg_time; do
  total=$((success + fail))
  pct=$((success * 100 / total))
  if [[ $fail -eq 0 ]]; then
    printf "${GREEN}%-18s${NC} %10d %10d %9d%% %10d\n" "$host" "$success" "$fail" "$pct" "$avg_time"
  else
    printf "${RED}%-18s${NC} %10d %10d %9d%% %10d\n" "$host" "$success" "$fail" "$pct" "$avg_time"
  fi
done <"$results_dir/healthz_results" | sort

echo ""
echo "=========================================="
echo "Phase 3: Concurrent Connection Test"
echo "=========================================="

echo -e "${YELLOW}Testing $CONCURRENT concurrent connections to VIP...${NC}"

concurrent_success=0
concurrent_fail=0

for host in "$API_VIP"; do
  echo "Spawning $CONCURRENT parallel requests..."

  for ((i = 1; i <= ITERATIONS; i++)); do
    (
      if curl -k -s -o /dev/null -w "%{http_code}" --connect-timeout 2 --max-time 5 "https://$host:$PORT/healthz" 2>/dev/null | grep -q "200\|401"; then
        echo "success" >>"$results_dir/concurrent_results"
      else
        echo "fail" >>"$results_dir/concurrent_results"
      fi
    ) &

    if ((i % CONCURRENT == 0)); then
      wait
    fi
  done
  wait
done

concurrent_success=$(grep -c "success" "$results_dir/concurrent_results" 2>/dev/null || echo 0)
concurrent_fail=$(grep -c "fail" "$results_dir/concurrent_results" 2>/dev/null || echo 0)
concurrent_total=$((concurrent_success + concurrent_fail))
concurrent_pct=$((concurrent_success * 100 / concurrent_total))

echo ""
echo "Concurrent Test Results:"
echo "------------------------"
if [[ $concurrent_fail -eq 0 ]]; then
  echo -e "${GREEN}VIP $API_VIP${NC}: $concurrent_success/$concurrent_total (${concurrent_pct}%)"
else
  echo -e "${RED}VIP $API_VIP${NC}: $concurrent_success/$concurrent_total (${concurrent_pct}%) - FAILED: $concurrent_fail"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="

vip_tcp_fail=$(grep "^$API_VIP:" "$results_dir/tcp_results" | cut -d: -f3)
vip_healthz_fail=$(grep "^$API_VIP:" "$results_dir/healthz_results" | cut -d: -f3)

if [[ $vip_tcp_fail -gt 0 ]] || [[ $vip_healthz_fail -gt 0 ]] || [[ $concurrent_fail -gt 0 ]]; then
  echo -e "${RED}ISSUES DETECTED${NC}"
  echo ""
  echo "Recommendations:"
  [[ $vip_tcp_fail -gt 0 ]] && echo "  - TCP connectivity issues: Check HAProxy backend health and firewall rules"
  [[ $vip_healthz_fail -gt 0 ]] && echo "  - HTTPS issues: Check k3s API server status and certificates"
  [[ $concurrent_fail -gt 0 ]] && echo "  - Concurrent issues: Check HAProxy max connections and timeouts"
  echo ""
  echo "  Run on k3s masters:"
  echo "    ss -tlnp | grep 6443"
  echo "    systemctl status k3s"
  echo ""
  echo "  Check on OPNsense HAProxy:"
  echo "    - Backend server status"
  echo "    - Health check configuration"
  echo "    - Connection limits and timeouts"
else
  echo -e "${GREEN}All tests passed!${NC}"
  echo "API servers are healthy and reachable."
fi
