#!/bin/bash
# Ensure cmctl is installed
if ! command -v cmctl &>/dev/null; then
  echo "cmctl could not be found. Please install cmctl and configure it with your Kubernetes cluster."
  exit 1
fi
# Retrieve all certificates in all namespaces
CERTIFICATES=$(kubectl get certificates --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"|"}{.metadata.name}{"\n"}{end}')
# Check if any certificates are found
if [ -z "$CERTIFICATES" ]; then
  echo "No certificates found in the cluster."
  exit 1
fi
# Iterate over each certificate and renew it
while IFS="|" read -r NAMESPACE CERT_NAME; do
  echo "Renewing certificate: $CERT_NAME in namespace: $NAMESPACE"
  cmctl renew "$CERT_NAME" -n "$NAMESPACE"
done <<<"$CERTIFICATES"
echo "Renewal process completed for all certificates."
