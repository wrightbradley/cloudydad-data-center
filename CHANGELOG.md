# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## What's Changed

### <!-- 0 -->🚀 Features

- Add .env.sample file  by @wrightbradley - ([0b6863c](0b6863c116427efde8d7fc27c448030b4a88fe82))
- Initial set up of FluxCD with Terraform  by @wrightbradley - ([4b8937f](4b8937ffd1ec7fb0d96bc5361ab3de171b44429b))
- Configure flux to deploy sealed-secrets  by @wrightbradley - ([73e2a5d](73e2a5d159e77fb02d3320e9c517cc2ca64ad189))
- Configure democratic-csi for cluster storage  by @wrightbradley - ([a47198f](a47198f07c93ae1090f6760915bfa0704b10ce17))
- Add support for snapshot-controller  by @wrightbradley in [#8](https://github.com/wrightbradley/cloudydad-data-center/pull/8) - ([11f9871](11f9871a945f8c11dc433793f8e092c6bb2401a4))
- Add traefik  by @wrightbradley in [#27](https://github.com/wrightbradley/cloudydad-data-center/pull/27) - ([c7154d0](c7154d08026462ef9cf79f93ed3817f06460bc06))
- Add cilium and kube-vip helm charts  by @wrightbradley in [#30](https://github.com/wrightbradley/cloudydad-data-center/pull/30) - ([37edd37](37edd37f762dc5e98df4f9b763ac174127b6792b))
- Add whoami and configure traefik  by @wrightbradley in [#32](https://github.com/wrightbradley/cloudydad-data-center/pull/32) - ([d1d8dc1](d1d8dc11eef652ada7380d23a190fba6853ecb06))
- Configure cilium to use kube-vip and point to proper kubeconfig  by @wrightbradley - ([37649ea](37649eaec3d44b1c90c367444ad22fed8e8129ee))
- Configure kube-vip to use the eth0  by @wrightbradley - ([6967e27](6967e27a8f3a106ce3307c0d0a678e44df98e318))
- Enable bgp for cilium  by @wrightbradley in [#33](https://github.com/wrightbradley/cloudydad-data-center/pull/33) - ([8c69227](8c69227d2c46aee731173bf885877dfeae9c1c91))
- Migrate to new cilium bgp solution  by @wrightbradley in [#35](https://github.com/wrightbradley/cloudydad-data-center/pull/35) - ([e3c7d63](e3c7d637bcf0dc9caf804ee37a6d041cd20afe4f))
- Cilium configuration changes  by @wrightbradley in [#37](https://github.com/wrightbradley/cloudydad-data-center/pull/37) - ([23cef48](23cef482c33f1a241bef35fc9155c964f683f37c))
- Use label for ip pool matching  by @wrightbradley in [#39](https://github.com/wrightbradley/cloudydad-data-center/pull/39) - ([709823e](709823ee50e4eae61f09b4293ebf0938ea549e58))
- Add selector for traefik ingress controller  by @wrightbradley in [#41](https://github.com/wrightbradley/cloudydad-data-center/pull/41) - ([ce6b55c](ce6b55cbde9a148d5d813abcad3bb7f1450a9171))
- Traefik configuration  by @wrightbradley in [#44](https://github.com/wrightbradley/cloudydad-data-center/pull/44) - ([c2fd44a](c2fd44a58f52b038c92c76cdadf4054df4b4506d))
- Cilium configuration  by @wrightbradley in [#46](https://github.com/wrightbradley/cloudydad-data-center/pull/46) - ([ebc7f54](ebc7f541f87d38e1a23d75e23b8921e99aaa61bd))
- Add l2 announcement policy  by @wrightbradley in [#47](https://github.com/wrightbradley/cloudydad-data-center/pull/47) - ([04b4693](04b4693df5b29f61eae124944bfb074c7378d237))
- Upgrade democratic-csi  - ([20db23b](20db23b21b728e9d9a143d986f8254c3885502e5))
- Upgrade traefik  - ([542b06c](542b06c3e4142859b98765684ed537c6716b1142))
- Add Loki  - ([05f247e](05f247e0e6695f914de3e1190fb694d8efb42aac))
- Add Mimir  - ([6baa7a2](6baa7a29749db4530de7f5df8b8cf199903a0246))
- Add VictoriaMetrics Metrics/Logs  - ([ce8f463](ce8f4631331c595ad794941580e8b8bb01eea933))
- Add scaffolding for LGTM stack  - ([55da49c](55da49ca5c2d70c0a3b477a332aaf05a184ae331))
- Fully replace kube-proxy with cilium  - ([b3847ab](b3847ab6d229207d1e2f66a5a63911352fff2fd3))
- Add Grafana  - ([09336fc](09336fc2320233fb3e1bca0f0d1c0fc0ac553de0))
- Add k8s-monitoring  - ([b958e0b](b958e0ba879cd8de3d8917b8e7dd2d902b509f76))
- K3s-ansible updates  - ([7de576b](7de576b9c77d758f0c5014b694b512117233b9d4))
- Configure observability  - ([c02ccd9](c02ccd921f1fd91a92c92961c6a14b9207010fa9))
- Rebuild cluster  - ([3f4be49](3f4be498d906ebf329a632963bb8bc869347adc5))
- Configure kubernetes dashboards  - ([10703fe](10703fe9facca82d6adcf0c1055d3750f9189948))
- Add coredns  - ([f0fb67d](f0fb67d2ea6f345231d1418fdb5becd8f446639e))
- Add goldilocks  - ([a237c6b](a237c6b31a1454ba49478f1607b2e333d7d804b3))
- Enable goldilocks monitoring on namespaces  - ([f6846a7](f6846a7c2c12fb72f19d24d6484d2b507e1dc105))
- Configure resources based on goldilocks  - ([8ebe228](8ebe228499e4e25aac7cf477a91b81d3c81f19d9))
- Upgrade vm-logs grafana plugin  - ([01aa591](01aa5915df0d08e882305541f8ab6e1d4c824f3f))
- Add node-problem-detector  - ([8fac193](8fac193794b84fa8a20ec76e92185db284e694d9))
- Add vm-alert  - ([ba87f37](ba87f37160c45ef87fef57438abbf65bdec7289e))
- Add alertmanager datasource  - ([f8211be](f8211be8a45deca6dc025af850572b1e9efc4a3b))
- Configure traefik dashboard access  - ([7f720ed](7f720ed2fbe490c6ea618ad02827ac0b66d8a3fd))
- Add alert rules  - ([1f7f421](1f7f4218926591f3e6d1a306f59d08c361213f19))
- Configure access logs with traefik  - ([6021f00](6021f00efde3e3cb9ba8bd70ebf6792a13a16483))
- Add vm-k8s-stack for monitoring  - ([a0d72cd](a0d72cdb0dd927f92f4bc551567ee96238424010))
- Add cert-manager  - ([0ffa9e1](0ffa9e1f13f31cfec4bb59cb5f2ff64dcee4ca78))
- Add otel-collector for logs/events monitoring  - ([ba20a55](ba20a55731da3e7d9d572de39d93416dab2a195b))
- Replace old raspberry pis with beelink devices  - ([683126f](683126f82d805d4f7b1c64f1c8f0280ecb31f3ac))
- Add monitoring for traefik  - ([e58dfd5](e58dfd50d33ee6e61d46467c6488e559df1c9495))
- Add tls for ingress routes  - ([17373e1](17373e15ad17191508b6bd4164d27cc8abcfaf65))
- Tune grafana settings  - ([1a95183](1a9518380462977824d72ddc7f9c4355064b9ac8))
- Add trivy-operator  - ([3053944](30539442e268f764a6400b19732512e5dd981bf7))
- Add cloudnative-pg  - ([fb718c6](fb718c638400e8799b18877825696bf35b5ea014))
- Configure gitleaks and update pre-commit-config versions  - ([e0f63b2](e0f63b2d5a127efc048734e36ccf2cdc88055d2f))
- Remove cloud-init from ubuntu systems after install  - ([d34f49f](d34f49fa2466084475891993f715d70d466d5080))
- Remove ubuntu from setup  - ([2e5e141](2e5e1415f512c4d4176208bfa09f17a8c7016530))
- Adjust packages and inventory  - ([2a91be0](2a91be04fedf6aa6ef3359b7cf5c4df2704fe695))
- Secure system users  - ([c79f3f7](c79f3f740803b8d9eb308b5a0cc9f7661d12238d))
- Dynamically set proper interface for k3s cluster  - ([1fe488a](1fe488ac2f27700b2e8456c783699bb4255e28d8))
- Only taint master nodes for raspberry pi devices  - ([6306f89](6306f894d37bb042dcc9f173f85c93d076af2745))
- Pin helm release versions  - ([36531bf](36531bfd2921ed5982f4adaff08cab2c4916a2c5))
- Configure laptop lid settings  - ([51a95af](51a95af0c6c46caf0e7b2376945325cc1a133447))
- Create common postgres database  - ([a00765d](a00765d138a6141ad311ba96cd69ad8d2ad6b26c))
- Configure grafana to use postgres backend  - ([4fb7dc8](4fb7dc8cc4aadb3e4e9db462d83b073f11bdddfb))
- Increase grafana replicas for HA  - ([04a9c64](04a9c64d9166b1a7a8cb0df41d8801f0d9b52dd5))
- Setup Grafana Oncall  - ([c54a7a6](c54a7a66441dddbc181cd3b8d36c33c096fafcf6))
- Allow management of alerts for prometheus in grafana  - ([687bd50](687bd50b9c1109b87c913a5a29e6d20ba48e3484))
- Add node-problem-detector dashboard  - ([ec784f8](ec784f87f497f75c484cfdf957f35ccaf5a6c09d))
- Add scheduled backup for cloudnative-pg  - ([6c8390e](6c8390ef9ae45904ad0ffab19a9f44bf22d971e5))
- Add custom alertmanager config  - ([7a013f6](7a013f677aa50c52f04a562c1de97216fd3b85a8))
- Add uptime-kuma  - ([7969591](7969591b48e7eafc3ea1dd37862a86f7df23f163))
- Create wildcard certificate  - ([3b967e4](3b967e4829974eebfbc4d791829a7dd93576a7f7))
- Add gatus  - ([6164ed2](6164ed27107cb8e44d13eed09b771262dd5a1501))
- Use uptime-kuma beta  - ([dd16230](dd162301f1e368462763e8a5a6a05f660e4579c5))

### <!-- 1 -->🐛 Bug Fixes

- Deploy sealed-secrets to the proper namespace  by @wrightbradley in [#5](https://github.com/wrightbradley/cloudydad-data-center/pull/5) - ([478283f](478283ff419275ac45eb04f6a769c25fd5dab9fd))
- Ensure storage services are enabled and started  by @wrightbradley - ([a37e87d](a37e87d9ea1e1b6ae6f2b5ed5611a871c3d52062))
- Fluxcd apps dependency  by @wrightbradley in [#7](https://github.com/wrightbradley/cloudydad-data-center/pull/7) - ([ea0d306](ea0d306021b3d495dad2085109b883953021a000))
- Disable snapshot-controller validating webhook  by @wrightbradley - ([2d96b69](2d96b694edd9c7eefdf895e02711c5cd3991a6e1))
- Do not taint master nodes  by @wrightbradley in [#9](https://github.com/wrightbradley/cloudydad-data-center/pull/9) - ([a3647a1](a3647a1b5cbee5f3f62dbd2feb2eaa1b90d8f4ed))
- Turn on debug for iscsi driver  by @wrightbradley in [#10](https://github.com/wrightbradley/cloudydad-data-center/pull/10) - ([d7c0586](d7c0586d437ad0c9a999401b2c8c91d9a911d1e6))
- Update truenas iscsi portal id  by @wrightbradley in [#11](https://github.com/wrightbradley/cloudydad-data-center/pull/11) - ([26c8e88](26c8e887e135fe539096b39a0215acbf67668628))
- Update truenas iscsi initiator portal id  by @wrightbradley in [#12](https://github.com/wrightbradley/cloudydad-data-center/pull/12) - ([a37999c](a37999c10927c8013c7dfa2b5cd517cd43f88eb3))
- Kustomize paths  by @wrightbradley in [#15](https://github.com/wrightbradley/cloudydad-data-center/pull/15) - ([d38ba9d](d38ba9d63cd40ffb1a787f5ce1756db240487880))
- Flux directory structure  by @wrightbradley in [#19](https://github.com/wrightbradley/cloudydad-data-center/pull/19) - ([4d383f2](4d383f23ce956362ba1d2e24c321267cb45c998d))
- Gotk-sync repo path  by @wrightbradley in [#20](https://github.com/wrightbradley/cloudydad-data-center/pull/20) - ([30f6340](30f6340abc9837327e1326f214792e86b894ccc7))
- Kustomization resource reference  by @wrightbradley in [#21](https://github.com/wrightbradley/cloudydad-data-center/pull/21) - ([5f5210c](5f5210c5af4adfed6920aa8555ce78ed0db7f1e6))
- Bad exclusion that prevented cluster from being applied  by @wrightbradley in [#23](https://github.com/wrightbradley/cloudydad-data-center/pull/23) - ([5510292](5510292ab7b0f6c36d57862867927b18044d12d0))
- Incorrect file reference in kustomization  by @wrightbradley in [#24](https://github.com/wrightbradley/cloudydad-data-center/pull/24) - ([b84b644](b84b644ad024bb8915344c0b2c240e48b1819724))
- Add sealed-secrets in kustomization  by @wrightbradley in [#25](https://github.com/wrightbradley/cloudydad-data-center/pull/25) - ([7a54194](7a54194945de64ceb8152be4df6a3067ecc743ba))
- Annoying dangling escape char  by @wrightbradley in [#28](https://github.com/wrightbradley/cloudydad-data-center/pull/28) - ([db8c2f3](db8c2f34d4efc98618bddbcd2d844293a1b37a3c))
- Reference configmap values in helm release for traefik  by @wrightbradley in [#29](https://github.com/wrightbradley/cloudydad-data-center/pull/29) - ([e2fbe9f](e2fbe9f33364dc9585525414cfef02e82db1667a))
- Helm chart release version for kube-vip  by @wrightbradley in [#31](https://github.com/wrightbradley/cloudydad-data-center/pull/31) - ([65b9ff6](65b9ff658b51805e07d87d08ba208ca360ed7db8))
- Remove kube config path definition  by @wrightbradley in [#34](https://github.com/wrightbradley/cloudydad-data-center/pull/34) - ([7dbc689](7dbc6893f81cd738b7af17fdd3ec0125fe1d471b))
- Try same asn  by @wrightbradley in [#36](https://github.com/wrightbradley/cloudydad-data-center/pull/36) - ([7ed8a60](7ed8a60c0fc03c4f01b8923b74f999109a8ff9f7))
- Try same asn again  by @wrightbradley in [#38](https://github.com/wrightbradley/cloudydad-data-center/pull/38) - ([1217f5d](1217f5d73a2d7397a643f9ec8fd94c32119d35cd))
- Incorrect yaml structure  by @wrightbradley in [#40](https://github.com/wrightbradley/cloudydad-data-center/pull/40) - ([cdb84a5](cdb84a5719f479f67b8401837cef1bac5abfcc7a))
- Set ipam backend mode correctly  by @wrightbradley in [#48](https://github.com/wrightbradley/cloudydad-data-center/pull/48) - ([6bdd69f](6bdd69f8935d8db8394855346d7686c6308c1556))
- Cilium ipam backend  by @wrightbradley in [#49](https://github.com/wrightbradley/cloudydad-data-center/pull/49) - ([9e327ff](9e327ff5a5cd0ce93bf05ce2fb2900d1ff904c1a))
- Cilium bgp configuration  - ([92625eb](92625eb896a9c4c6706cee9e9fd32c2503f918ac))
- Specify traefik as ingressclass  - ([345a27f](345a27ff96c5936e5b7aeac87d9122293e07fcf8))
- Vm ingress and hosts  - ([bd938c4](bd938c4eb494e1389c7957652c6d86ac09778f57))
- Truenas initiator id  - ([2475d27](2475d27b41aa3d228951df21cbfe55f7d5c52144))
- Grafana unsigned plugins  - ([1bc3909](1bc3909e9c27797bb945481ea6fbf7b084a14c6b))
- Disable persistence for grafana  - ([79dd856](79dd856c4cdd1dca72a74f50f8cfccf82840d107))
- Timezone configuration  - ([e867335](e867335b6fd2501043dfa3324acb4c334779b0a2))
- Re-encrypt secrets after cluster rebuild  - ([9d1b5c1](9d1b5c12b9dcc6fbd44ad286b0a2e6734f524e33))
- Remove local-path storageclass as default  - ([fd5874e](fd5874e4a0e5a4c024f6682929681903105198ae))
- Install crds for cert-manager  - ([b3eb3e9](b3eb3e968d60a561aeded011bb2b4e4767c2be5e))
- Correct portal initiator group id  - ([59aaa3a](59aaa3ad3ec96a59f4bb3cb31fc455f11a792ecc))
- Update truenas iscsi  - ([83cc440](83cc440d36599a06b5182a2773da49fafbd9efcc))
- Grafana alpine dns resolution  - ([4c52a94](4c52a94335e6b7d3f9ddc3377a59b2e5e5b6615d))
- VM naming  - ([a469e3d](a469e3d4b6191d55a982d506dfc5362065b1d148))
- Cpu throttling on goldilocks  - ([34b6387](34b638704b9d31ab713ff31787ecc04923009a85))
- Cpu throttling for otel-collector  - ([a6349bd](a6349bd5dad6b803d4d23dc42d387e0838faa92d))
- Cpu throttling for vm-logs  - ([386a367](386a3672b0b480cdf6ab72de9ef3b01e1bf57c58))
- Nodeselector issues with trivy nodecollector  - ([60d9832](60d98322c2e1a0bbcc3a542968ce05c1def8c12c))

### <!-- 10 -->◀️ Revert

- Revert "Add Flux sync manifests"  by @wrightbradley in [#22](https://github.com/wrightbradley/cloudydad-data-center/pull/22) - ([632c728](632c728e1b4c49519a44c93a045e2fb0ed39234a))
- Revert "Add Flux v2.3.0 component manifests"  by @wrightbradley - ([df6d98a](df6d98a7ed3e992f87ff3661b23da37bfeb4cde5))
- Revert "Add Flux sync manifests"  by @wrightbradley in [#26](https://github.com/wrightbradley/cloudydad-data-center/pull/26) - ([6ec5dc3](6ec5dc3a532366f3d6c062e678278734b5b70c70))

### <!-- 12 -->💼 Other

- Initial commit  by @wrightbradley - ([c91571c](c91571c21e3f4f937f8508e89cc0257272f9e55c))
- Add Flux v2.3.0 component manifests  - ([cc4e647](cc4e647284436af017106a6bd6d77717970a351a))
- Add Flux sync manifests  - ([14cf75d](14cf75da19702b33354abe6f0a0ae04f73275093))
- Restrict permissions on kubeconfig file  by @wrightbradley - ([e8be705](e8be705cbf3cab8c15d26c3586553be1c01c9cc4))
- Bump actions/setup-python from 2 to 5  by @dependabot[bot] in [#3](https://github.com/wrightbradley/cloudydad-data-center/pull/3) - ([63667e6](63667e6122722b975cbc2974ba839b318f7c5484))
- Bump zgosalvez/github-actions-ensure-sha-pinned-actions  by @dependabot[bot] in [#1](https://github.com/wrightbradley/cloudydad-data-center/pull/1) - ([a79c218](a79c21873da00373f8cd1b8b1998139f31c75c4e))
- Disable coredns  - ([33abb51](33abb51779cbf1f4ddd6d56a93a981ea0ee79d11))
- Setup wakatime  - ([9c23e6d](9c23e6dac27281951a38d9be53e504ecadc8597a))
- Don't deploy kube-vip  - ([e26c38a](e26c38a351259febc5112dcb9e8575be8eef8388))

### <!-- 2 -->🚜 Refactor

- Flux directory structure  by @wrightbradley in [#14](https://github.com/wrightbradley/cloudydad-data-center/pull/14) - ([987a29a](987a29a7b317c8c751cd03eb94f8e9e422edec99))
- Podinfo names  by @wrightbradley in [#16](https://github.com/wrightbradley/cloudydad-data-center/pull/16) - ([4936aba](4936abad160cb737312f9e5cf8a9cf1a720ecebb))
- Apps directory structure  by @wrightbradley in [#17](https://github.com/wrightbradley/cloudydad-data-center/pull/17) - ([e7cf490](e7cf490c5b7b668e9681ee7c479f98e54b4719e3))

### <!-- 5 -->🎨 Styling

- Run linters  by @wrightbradley - ([59f2dbb](59f2dbbd57ccd0f9845f767a6b39ec719cf00f17))
- Update ingress names for vm-logs and vm-metrics  - ([6e095be](6e095beab7171c24d1696146f04d06a31b8f3859))
- Run pre-commit linting  - ([735ee41](735ee41abc86b1f48e35ddcf141a8885904b91c3))
- Run pre-commit  - ([b16b303](b16b3032ad4fed06d6e2cc654da303fb2dafb43e))

### <!-- 7 -->📚 Documentation

- Update democratic-csi  - ([f56e2df](f56e2df7acc6ff4668873f36d54c8581a8ac875f))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Disable debug logging for the trueNAS CSI driver  by @wrightbradley - ([8086132](8086132630ad6c6f1c9c074d7749c8a8cf19ec6a))
- Remove vm-metrics, k8s-monitoring, vm-alert  - ([648c902](648c90242f553467a29ff49cca71f501b737c86d))
- Add git-cliff changelog config  - ([5bd9080](5bd9080fa6c75dd8445c5e9ee389f1373cf1a186))
- Disable Grafana oncall  - ([d54de39](d54de391774d0cbb54450deef4865faa9178fe72))
- Removed unused apps  - ([9b16978](9b169782b8f104953f96ed0e03642cc6f28ed300))

### <!-- 9 -->🤖 CI

- Improve conditional workflow executions  by @wrightbradley in [#6](https://github.com/wrightbradley/cloudydad-data-center/pull/6) - ([2768673](2768673d8a982d1b801b51791a77b4706f9704e3))


## New Contributors
* @wrightbradley made their first contribution in [#49](https://github.com/wrightbradley/cloudydad-data-center/pull/49)
* @dependabot[bot] made their first contribution in [#18](https://github.com/wrightbradley/cloudydad-data-center/pull/18)
* @ made their first contribution

<!-- generated by git-cliff -->
