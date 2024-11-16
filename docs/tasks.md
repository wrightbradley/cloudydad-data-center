# Tasks

## Raspberry Pis

- Configure Users and Groups
- Configure OpenSSH Server
- Configure Boot Parameters

### Notes

```bash
kubectl create secret generic democratic-csi-secret-values --from-file=values.yaml --dry-run=client -o yaml > secret.yaml

kubeseal --controller-namespace sealed-secrets -f secret.yaml -w sealed-democratic-csi-secrets.yaml

kubectl patch storageclass truenas-iscsi-csi -p '{"metadata": {"annotations": {"storageclass.kubernetes.io/is-default-class": "true"}}}'
storageclass.storage.k8s.io/truenas-iscsi-csi patched

kubectl patch storageclass local-path -p '{"metadata": {"annotations": {"storageclass.kubernetes.io/is-default-class": "false"}}}'
storageclass.storage.k8s.io/local-path patched
```
