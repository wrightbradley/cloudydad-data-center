#!/bin/bash

# kubectl get pods -o wide -A | grep -v cloudnative-pg | grep ago | awk '{print $1, $2}' | while read namespace pod; do kubectl delete pod "$pod" -n "$namespace"; done
kubectl get pods -o wide -A | grep -v cloudnative-pg | grep -v '1/1' | grep -v '2/2' | grep -v '3/3' | grep -v '4/4' | awk '{print $1, $2}' | while read namespace pod; do kubectl delete pod "$pod" -n "$namespace"; done
