#!/bin/bash

kubectl get pods -o wide -A | grep -v cloudnative-pg | grep ago | awk '{print $1, $2}' | while read namespace pod; do kubectl delete pod "$pod" -n "$namespace"; done
