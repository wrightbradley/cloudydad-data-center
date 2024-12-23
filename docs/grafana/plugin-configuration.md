# Grafana Plugin Configuration

```yaml
# https://kubernetes.io/docs/concepts/configuration/configmap/
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-plugin
  labels:
    grafana_plugin: enabled
data:
  example-plugin.yaml: |
    apiVersion: 1
    apps:
      # <string> the type of app, plugin identifier. Required
      - type: raintank-worldping-app
        # <int> Org ID. Default to 1, unless org_name is specified
        org_id: 1
        # <string> Org name. Overrides org_id unless org_id not specified
        org_name: Main Org.
        # <bool> disable the app. Default to false.
        disabled: false
        # <map> fields that will be converted to json and stored in jsonData. Custom per app.
        jsonData:
          # key/value pairs of string to object
          key: value
        # <map> fields that will be converted to json, encrypted and stored in secureJsonData. Custom per app.
        secureJsonData:
          # key/value pairs of string to string
          key: value
```
