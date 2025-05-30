# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9] - 2025-05-05
## What's Changed

### <!-- 0 -->🚀 Features

- Configure karakeep archive settings  by @wrightbradley - ([d35042a](d35042a049547924a1e167540b3e68ccc5cf8017))
- Add ansible maintenance playbooks  by @wrightbradley - ([868f531](868f53197b82680020f4e6f05536cbf598c88b91))
- Add ollama  by @wrightbradley - ([d30aa6e](d30aa6edd363fd77d32667a6b7dade45971db220))
- Leverage ollama models  by @wrightbradley - ([4266889](4266889398b18045eb6f28cc76dafc946db86ce5))
- Add rsshub  by @wrightbradley - ([ce53f3d](ce53f3db4d2f83e8a38fd8f59cee935820f620e4))
- Upgrade authentik to 2025.4.0  by @wrightbradley - ([84ebc87](84ebc876828bddfd5e86a8d93c61f9c7a2cd7cc0))
- Upgrade immich to v1.132.3  by @wrightbradley - ([9ec1185](9ec118504d4258a2dcbc2a82c4bb77d8e753b507))

### <!-- 1 -->🐛 Bug Fixes

- Add karakeep secrets  by @wrightbradley - ([41a2b12](41a2b120b46cbd81bb999b8f0547b1e65a8643da))
- Migrate LB service to Ingress for karakeep  by @wrightbradley - ([20e985e](20e985e5e373cf66a71a8063c5b29d61dff2ee69))
- Helm repo url for bjw-s  by @wrightbradley - ([1106fff](1106fff78fd47a1204403c2180d037dd48d1562a))
- Provide nameservers for cert-manager  by @wrightbradley - ([e0ab838](e0ab838c72ff442fbe56a59fa987956621f54d53))

### <!-- 12 -->💼 Other

- Add scripts  by @wrightbradley - ([8968700](8968700715df30243ae34d2577da275f9de7d6b3))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Remove unused helm repos and apps  by @wrightbradley - ([6dd0658](6dd06587bcde137e7eec4a0b66fcb59095fbf5f0))
- Increase storage for vm-k8s-stack  by @wrightbradley - ([63560ce](63560ce2ffc7197007d2cf881db8afa2076cdcfa))
- Migrate to valkey redis for authentik  by @wrightbradley - ([a472d01](a472d01d0430a2705cd13c3fde5f5646c1dd7190))
- Improve resource reqs/limits  by @wrightbradley - ([41ff37e](41ff37ed3fefdd3d456b2e37c8b4871967245500))
- Remove homepage app  by @wrightbradley - ([d6fbdb9](d6fbdb9531dab73ded6f3b745b357ac74f6e2b5e))

### <!-- 9 -->🤖 CI

- Update and run pre-commit  by @wrightbradley in [#196](https://github.com/wrightbradley/cloudydad-data-center/pull/196) - ([4e46cea](4e46cea2d963a9113ba2fbb2c8c97c9792ac28d4))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.8...0.1.9

## [0.1.8] - 2025-04-14
## What's Changed

### <!-- 1 -->🐛 Bug Fixes

- Enable karakeep app  by @wrightbradley in [#193](https://github.com/wrightbradley/cloudydad-data-center/pull/193) - ([93d503e](93d503e4ba8c29c168336d8da09ce87cd3e0fce7))

### <!-- 7 -->📚 Documentation

- Release 0.1.8 [skip ci]  by @github-actions[bot] - ([28d6156](28d6156ba71b85810e0ac030938184954bd24a6b))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Migrate config .github/renovate.json5  by @renovate[bot] in [#173](https://github.com/wrightbradley/cloudydad-data-center/pull/173) - ([28bef16](28bef167c0cf6cd139da519fb969bc311122e321))

### <!-- 9 -->🤖 CI

- Configure renovate and release behavior  by @wrightbradley in [#157](https://github.com/wrightbradley/cloudydad-data-center/pull/157) - ([b432786](b432786257bbd60553358d97f3ae822e23efb2a8))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.7...0.1.8

## [0.1.7] - 2025-04-13
## What's Changed

### <!-- 0 -->🚀 Features

- Add authentik  by @wrightbradley - ([8cbdf92](8cbdf9210cd7543de9a9aec42f5a3b38204293a2))
- Add support for configuring routes for different networks for tailscale  by @wrightbradley - ([e1fd52e](e1fd52e9a20f545a57f1136f562732bbe25851f8))
- Add cloudflared tunnel for authentik  by @wrightbradley - ([a6df512](a6df512faa7fd3527b18255fd06e3af82838922b))
- Configure authentik oauth for grafana  by @wrightbradley - ([cd24fb5](cd24fb5fb7e19d29fb582efdeb804f561f642556))
- Add system-upgrade-controller  by @wrightbradley - ([6b5c14b](6b5c14b3060564cd8498174026e3644b43219b4e))
- Improve reliability of authentik  by @wrightbradley - ([081c01e](081c01eeba8f8fdcd24c676fde2ace409d9d2a01))
- Add valkey  by @wrightbradley - ([9eb4d98](9eb4d98eeda71626239d582ad32288d24f74693b))
- Add immich  by @wrightbradley - ([9d73918](9d739185b663f75b7a5161b5a207c75067cef590))
- Upgrade vm-k8s-stack to 0.33.2  by @wrightbradley - ([058ec10](058ec10c40dc7fb79e9deff7166d7656357b2868))
- Add bjw-s helm repo  by @wrightbradley - ([1644c26](1644c2672102c902d4117fcefe7ef07885c6eba4))
- Add homepage  by @wrightbradley - ([50d46a3](50d46a3e60235a82027461929ff830ca18867c1b))
- Add wakapi  by @wrightbradley - ([89fd355](89fd355c8644937e10090796cbd10b582f1961f0))
- Configure wakatime redirect  by @wrightbradley - ([8f67d24](8f67d2495ffa96031ad61cb1e8cb7b221b20d0c0))
- Add invidious  by @wrightbradley - ([df98de5](df98de507f44db3b49d80872c6c8d477fb048b6a))
- Add signoz  by @wrightbradley - ([5e88c6e](5e88c6e820268893394f373e7cb35314492c50e0))
- Add update playbook  by @wrightbradley - ([5717d72](5717d72aae6c43ffc8fd5fa7f8959c8655b1507e))
- Upgrade to k3s 1.32  by @wrightbradley - ([1cc3bab](1cc3bab0f8af62e0151da6a007f006fd8956e9d4))
- Add tags for k3s-service file changes  by @wrightbradley - ([b7d26eb](b7d26eb621a9021e06a6ff378f2c5db01bc4f2d9))
- Add karakeep  by @wrightbradley - ([38f9ec6](38f9ec685d25193eed2890f8a6229154425a6d55))

### <!-- 1 -->🐛 Bug Fixes

- Disable scraping of services built into k3s  by @wrightbradley - ([f040e76](f040e76581c4f2bab8f0821dd568db7a137a641b))
- Deprecated apis for flux resources  by @wrightbradley - ([9d5bb3c](9d5bb3cc2e44e2f3d5a6f52fd635c8bd1dddeb54))
- Add basic auth for metrics scrape for uptime-kuma  by @wrightbradley - ([2889310](28893109131d98b94f0db26bf6dca2605e2377f5))
- Schedule uptime-kuma on rpi07 node for stability  by @wrightbradley - ([b880084](b8800847577a85715173f2d5b3e12b1ca2b65f96))
- Allow csi nodes to be scheduled on master nodes  by @wrightbradley - ([7756a49](7756a49a9985282865b6318b02f89b8cae7c56c3))
- Root username for postgres  by @wrightbradley - ([2e4c24a](2e4c24af2034197a6d43e7b6fa952fd32259fa12))
- Disable tailscale as it interferes more than it helps  by @wrightbradley - ([befc35a](befc35ae99264f868ef7d8d16fa1028dc9de7b47))
- Increase storage for postgres cluster  by @wrightbradley - ([3ab1945](3ab1945a0bdcf16c0f55268037903b4d62a392e2))
- Adjust memory limits for democratic-csi  by @wrightbradley - ([5923a23](5923a231385db3959ec5910f5e91de507fc879a3))
- Increase storage for victoria-metrics  by @wrightbradley - ([ca74109](ca7410931d647caf99c3095eb5a1e28285560a4b))
- Increase storage for cloudnative-pg cluster  by @wrightbradley - ([6e8f826](6e8f826814ea2dc81054400a2ba83171d6773883))
- Network configuration  by @wrightbradley - ([7c241df](7c241dfa5638e837934826582c479e73be8e8167))
- Set memory limits for democratic-csi  by @wrightbradley - ([67cf3e3](67cf3e3c77652b1e6fda247370bfc7997589a79e))
- Tune reserved resources for k3s  by @wrightbradley - ([95bc8f9](95bc8f922fcfb2b0e03743d1201d95b21c36356d))
- Add v to GH Action tags  by @wrightbradley in [#100](https://github.com/wrightbradley/cloudydad-data-center/pull/100) - ([410d11a](410d11ada2c6e669825cba72093f9bf03fb49d2b))
- Add v to GitHub Actions tags  by @wrightbradley in [#137](https://github.com/wrightbradley/cloudydad-data-center/pull/137) - ([7a34fc3](7a34fc3b27f90b2853650e96595f606aba6e88d6))

### <!-- 12 -->💼 Other

- Add renovate.json  by @renovate[bot] in [#95](https://github.com/wrightbradley/cloudydad-data-center/pull/95) - ([c49bf1e](c49bf1e0542ca6eae6381a4620799cae4e2a0cb8))

### <!-- 4 -->⚡ Performance

- Tune resource requests and limits based on krr recommendations  by @wrightbradley - ([add225c](add225cc819044ab6471a803ac8aefb825e398e1))
- Reduce resource usage by immich  by @wrightbradley - ([35dff70](35dff7026568b39dbb30971d39a8a044b887d3df))
- Reduce resources for trivy  by @wrightbradley - ([032b6eb](032b6eb4a93d7bbf850b83aa811231c5e90a3f85))
- Tune resources to avoid oom events  by @wrightbradley - ([a30d310](a30d31051c7bdacd4a0f5ac3b53baedde9b558cf))

### <!-- 5 -->🎨 Styling

- Address lint issues  by @wrightbradley - ([c7c2c5d](c7c2c5dcf6b9ceddeca72612e9a2acb7bd2f4a8c))

### <!-- 7 -->📚 Documentation

- Release 0.1.6 [skip ci]  by @github-actions[bot] - ([dcd356e](dcd356e35356936cf5a11126d574dd6ca545c7f4))
- Release 0.1.7 [skip ci]  by @github-actions[bot] - ([e4f89bf](e4f89bfc73fd56c647d8459963bad68c7c0e26e6))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Update remote address for remote host  by @wrightbradley - ([65436be](65436bed9d991c22c5c12ab5e44d2ce22112ee80))
- Disable unused apps  by @wrightbradley - ([d648a1b](d648a1b15c7f9d18951fb8ac06c062a6f7c93fee))
- Disable trivy-operator  by @wrightbradley - ([bde4398](bde439804e4d3fd2079f52d33cef4f5442d7ebbf))
- Reduce vm-k8s-stack operator to 1 replica  by @wrightbradley - ([ebb634b](ebb634bfef05f2579da1125b82b5ae06c77ad0fc))
- Increase memory for cloudnative-pg  by @wrightbradley - ([cb76bfb](cb76bfb45d15bbb1d56f28a81b9cf359923c7598))
- Disable signoz temporarily  by @wrightbradley - ([60d0885](60d08852c7b7d3140df5dee8c864b16fb3ddb746))

### <!-- 9 -->🤖 CI

- Improve config for renovate management  by @wrightbradley in [#96](https://github.com/wrightbradley/cloudydad-data-center/pull/96) - ([762342a](762342a55eccf245c4655fe08ed16b97266e0d5a))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.6...0.1.7

## [0.1.6] - 2024-12-23
## What's Changed

### <!-- 0 -->🚀 Features

- Add tailscale setup on hosts  by @wrightbradley - ([721a160](721a1600aa34e1f80b994e700e2e78c1c5e5df4c))
- Add rpi remote hosts  by @wrightbradley in [#85](https://github.com/wrightbradley/cloudydad-data-center/pull/85) - ([aec046b](aec046b8d2c563902b8a8ea9f40263d1e4276f10))

### <!-- 7 -->📚 Documentation

- Release 0.1.6 [skip ci]  by @github-actions[bot] - ([a4ef96a](a4ef96a37f2ce065b2557593e8ddc16d11ae39b9))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.5...0.1.6

## [0.1.5] - 2024-12-23
## What's Changed

### <!-- 0 -->🚀 Features

- Configure default tls for traefik ingress with wildcard  by @wrightbradley - ([7742756](7742756b7d9e53bf9f86170b462a23d4391f6282))
- Add flux dashboards  by @wrightbradley in [#83](https://github.com/wrightbradley/cloudydad-data-center/pull/83) - ([0d04648](0d046487aeebaf6209d40c676e9802d99c60c61b))

### <!-- 7 -->📚 Documentation

- Release 0.1.5 [skip ci]  by @github-actions[bot] - ([168137c](168137c6bb4b66362275e8dcd14430d11c9f33a4))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.4...0.1.5

## [0.1.4] - 2024-12-22
## What's Changed

### <!-- 0 -->🚀 Features

- Configure default tls for traefik ingress with wildcard  by @wrightbradley - ([5fdcbd5](5fdcbd5d677593feef686f5590e2e2d35176cf4a))
- Upgrade vm-k8s-stack to 0.33.0  by @wrightbradley in [#82](https://github.com/wrightbradley/cloudydad-data-center/pull/82) - ([3aa9a33](3aa9a336debc9cd36defaf43933f7a638bcbcd52))

### <!-- 4 -->⚡ Performance

- Set cpu/mem reqs/limits for vm-k8s-stack  by @wrightbradley - ([6a45a96](6a45a96ed5b7078b058667f4a158f6893c7613b6))

### <!-- 7 -->📚 Documentation

- Release 0.1.3  by @github-actions[bot] - ([54c15c0](54c15c038824150034bba6ec43d01b378616242a))
- Release 0.1.4 [skip ci]  by @github-actions[bot] - ([10437fc](10437fc7c8df2bfa9db85fd9a04ab260af6016a3))

### <!-- 9 -->🤖 CI

- Improve release automation  by @wrightbradley - ([6e6d4dc](6e6d4dcac57adea6d633a37ca7e570a713671538))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.3...0.1.4

## [0.1.3] - 2024-12-20
## What's Changed

### <!-- 7 -->📚 Documentation

- Release 0.1.2  by @github-actions[bot] - ([cbc0e1e](cbc0e1e99c641e3151d3f3a2f8d8467be8d3931b))

### <!-- 9 -->🤖 CI

- Add gitleaks action  by @wrightbradley in [#81](https://github.com/wrightbradley/cloudydad-data-center/pull/81) - ([4a28b22](4a28b22dc34b0ac4af17b29f14b97a3de17cd5cb))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.2...0.1.3

## [0.1.2] - 2024-12-20
## What's Changed

### <!-- 7 -->📚 Documentation

- Release 0.1.2  by @github-actions[bot] - ([68ca50e](68ca50ef579e4d736e114ef7a3e7496722d790f4))

### <!-- 9 -->🤖 CI

- Merge changelog and release workflows  by @wrightbradley in [#78](https://github.com/wrightbradley/cloudydad-data-center/pull/78) - ([12122b4](12122b4d4682484b94a3c6fce6bebc0dd605fcc4))
- Release workflows  by @wrightbradley in [#79](https://github.com/wrightbradley/cloudydad-data-center/pull/79) - ([c660252](c660252c7c77709c7321eeae1958aa8c48bd3f0e))
- Optimize release workflows  by @wrightbradley in [#80](https://github.com/wrightbradley/cloudydad-data-center/pull/80) - ([eff918c](eff918cc8061a00cb26ba091b3a2af1640c48430))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.1...0.1.2

## [0.1.1] - 2024-12-20
## What's Changed

### <!-- 7 -->📚 Documentation

- Release 0.1.1  by @github-actions[bot] - ([3432708](34327083812118990353ea0363ed0f197923e727))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Update dependency versions  by @wrightbradley - ([240a772](240a772e1d004d494ea946a11c442692f90c6c6a))

### <!-- 9 -->🤖 CI

- Improve changelog workflow  by @wrightbradley in [#77](https://github.com/wrightbradley/cloudydad-data-center/pull/77) - ([8843a0e](8843a0ecd098215f7e67a06d989d9cacfb66d5e8))


**Full Changelog**: https://github.com/wrightbradley/cloudydad-data-center/compare/0.1.0...0.1.1

## [0.1.0] - 2024-12-20
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
- Upgrade democratic-csi  by @wrightbradley - ([2de2e72](2de2e727f2e08e86040de87be38234c0085c4cd9))
- Upgrade traefik  by @wrightbradley - ([d4b4633](d4b46335fd3b47e53a6e54aaab95be4672acce1c))
- Add Loki  by @wrightbradley - ([d46c0c1](d46c0c1213a240bbbcf49db45a66a0d4b892e217))
- Add Mimir  by @wrightbradley - ([d894e4f](d894e4f8f9d77577ca4efbfa53ebdbce45899043))
- Add VictoriaMetrics Metrics/Logs  by @wrightbradley - ([42cfe60](42cfe60305778ba36b67a7ffad0fd1af459d877e))
- Add scaffolding for LGTM stack  by @wrightbradley - ([b73a2bc](b73a2bcf7340dd5345a8a5fa6f8512010eeae51d))
- Fully replace kube-proxy with cilium  by @wrightbradley - ([8f5737c](8f5737ccdfd4064ecd9ab33bc4e6c4952ca86b2e))
- Add Grafana  by @wrightbradley - ([b6636fa](b6636fada32e5b364d6292404e9d3cd2d263e1d9))
- Add k8s-monitoring  by @wrightbradley - ([f058417](f058417a1d9ac6dfefc25acbd92d853975599222))
- K3s-ansible updates  by @wrightbradley - ([b306a6e](b306a6e70c6055bdce2a6da24d57bed2bd702a67))
- Configure observability  by @wrightbradley - ([596788d](596788d72ba5c8a20886f7dfda735def3f3d57e4))
- Rebuild cluster  by @wrightbradley - ([6c4d9f2](6c4d9f23feb41ad076b2ddcc55c8382da0305f68))
- Configure kubernetes dashboards  by @wrightbradley - ([25e13cc](25e13cc028cc3358e604eee579087bdf5d3af892))
- Add coredns  by @wrightbradley - ([2a1e4a0](2a1e4a06fa1399e4cbb773763bbbea32f703b7e5))
- Add goldilocks  by @wrightbradley - ([b1c1287](b1c1287a32569f13dea811e51ef4cf7d0106ded7))
- Enable goldilocks monitoring on namespaces  by @wrightbradley - ([63fe516](63fe516850e762baf2406d63584f9c86043bd821))
- Configure resources based on goldilocks  by @wrightbradley - ([0085ca9](0085ca973ef6e51ac67b9e9460c6782fd73f61d2))
- Upgrade vm-logs grafana plugin  by @wrightbradley - ([5ea09f4](5ea09f4b171d5f91ac9520ff67dc8375a6f6b508))
- Add node-problem-detector  by @wrightbradley - ([1a62b0e](1a62b0e4e03032565c95f1eb441b640de083fd9e))
- Add vm-alert  by @wrightbradley - ([7e71218](7e71218526a3e784715a6c84d2a1750dba866a73))
- Add alertmanager datasource  by @wrightbradley - ([a4c8e09](a4c8e095097e52368e21c6083898af4ecfacbfa5))
- Configure traefik dashboard access  by @wrightbradley - ([c8da7fd](c8da7fd1754042c63e3da436aa2459c08d57a489))
- Add alert rules  by @wrightbradley - ([b0240c4](b0240c4299c9caf56ed0382cbed9cde68ccb0c0c))
- Configure access logs with traefik  by @wrightbradley - ([a99f7ef](a99f7ef5690b40684de9a5ebee8699f2c6690a30))
- Add vm-k8s-stack for monitoring  by @wrightbradley - ([6c252f9](6c252f9e4088d575ba5e0a65f2fc4baeb572b14e))
- Add cert-manager  by @wrightbradley - ([ec00a1f](ec00a1f1a976dcfd755602646d9b5d3af2e8066b))
- Add otel-collector for logs/events monitoring  by @wrightbradley - ([c0e5f6e](c0e5f6e14cd9daa95ebf1eb7adc2faf027b3c708))
- Replace old raspberry pis with beelink devices  by @wrightbradley - ([cf0c451](cf0c4512682eabd245a17a39172191be243482e9))
- Add monitoring for traefik  by @wrightbradley - ([3e38283](3e38283b9f635c78b4910f84e281be705d631828))
- Add tls for ingress routes  by @wrightbradley - ([bea6c2f](bea6c2f95e7402d30610544466392b5d16ab60ba))
- Tune grafana settings  by @wrightbradley - ([47daa8e](47daa8e4181d14c1fb660e0faf157c4a8e376c13))
- Add trivy-operator  by @wrightbradley - ([a1effae](a1effaef7caf308b8f874174913df93112b1347d))
- Add cloudnative-pg  by @wrightbradley - ([f8c46ec](f8c46ec04133896d79cc79a93bd7db1efd59b3e8))
- Configure gitleaks and update pre-commit-config versions  by @wrightbradley - ([917f18f](917f18f19676b5e321c9999dbed07bffe567216c))
- Remove cloud-init from ubuntu systems after install  by @wrightbradley - ([16e5636](16e56366dc726b6a25a202591914fc1a08aab1f2))
- Remove ubuntu from setup  by @wrightbradley - ([2011f53](2011f53519777ead736fc620b0adeaffc8b5b128))
- Adjust packages and inventory  by @wrightbradley - ([7050209](705020920e688a5844ff10529f0c4f5f861e4346))
- Secure system users  by @wrightbradley - ([5142c18](5142c18e02d21f3f917ca0a70146795a42f48cf0))
- Dynamically set proper interface for k3s cluster  by @wrightbradley - ([fc8c8e2](fc8c8e2a5ae210126c150b3f48d6c4700d2bed95))
- Only taint master nodes for raspberry pi devices  by @wrightbradley - ([cd2d596](cd2d596f2e4fea38b9a496837154d48ff7449333))
- Pin helm release versions  by @wrightbradley - ([285a292](285a2922091f73adcedf3fd4fee8dc1d6b49cfc3))
- Configure laptop lid settings  by @wrightbradley - ([05381cc](05381cc97ed32ce82010e8ee0e6a2d5687bc7aa8))
- Create common postgres database  by @wrightbradley - ([a7da8d5](a7da8d5cc38e558522e251f580905667874621a5))
- Configure grafana to use postgres backend  by @wrightbradley - ([cf603db](cf603db2edd523b195e03a66da1dfac177764f8b))
- Increase grafana replicas for HA  by @wrightbradley - ([33c201d](33c201dc9b48934d2e997feb190c2060ddedbfcb))
- Setup Grafana Oncall  by @wrightbradley - ([72afd23](72afd234492829ea0a250891d5bfd27467aa2fb8))
- Allow management of alerts for prometheus in grafana  by @wrightbradley - ([ba90f43](ba90f4332ab1e69c32b3ae09190f4f4a7027a260))
- Add node-problem-detector dashboard  by @wrightbradley - ([48024b2](48024b2dcbf25990f164a2dca3d4edb55469f648))
- Add scheduled backup for cloudnative-pg  by @wrightbradley - ([e803c57](e803c57d40c6b79be77b179fadff4b6e57562391))
- Add custom alertmanager config  by @wrightbradley - ([9fb9829](9fb982999864f9ed24ac191717944466e95f53dd))
- Add uptime-kuma  by @wrightbradley - ([0e680cf](0e680cf1eae550a7768a81d804d4e195184d5a02))
- Create wildcard certificate  by @wrightbradley - ([1ba11fe](1ba11feb27102505eb7b2bb651bccea8ca2bb932))
- Add gatus  by @wrightbradley - ([4775dc2](4775dc246ed9882a323b0f5e3d3fec3787ab486c))
- Use uptime-kuma beta  by @wrightbradley - ([f661193](f6611938e78685d911e5e1a60db4a20a90f56f01))

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
- Cilium bgp configuration  by @wrightbradley - ([144a600](144a60026f878254ffc11000709cbab0902491a8))
- Specify traefik as ingressclass  by @wrightbradley - ([96e8df1](96e8df13cd0466568d84181306dded2ae1721ceb))
- Vm ingress and hosts  by @wrightbradley - ([c648495](c648495f582db3b4fe9bf724aeef1a30d8edce5f))
- Truenas initiator id  by @wrightbradley - ([79fcb89](79fcb895c4dd1ff22faf39f5bb339e9ee6dca792))
- Grafana unsigned plugins  by @wrightbradley - ([bc95795](bc95795c3bad619b4558d95c3f841794248c4ff0))
- Disable persistence for grafana  by @wrightbradley - ([e80cdd4](e80cdd41280d1c395c773e96243c069d9e985bef))
- Timezone configuration  by @wrightbradley - ([32ca6fc](32ca6fc054fe910ef5b2a090fc9343fbd7b9669a))
- Re-encrypt secrets after cluster rebuild  by @wrightbradley - ([6126102](6126102d3bfeefec42c17694d508bb1006e8430a))
- Remove local-path storageclass as default  by @wrightbradley - ([f531d0c](f531d0c47416da4cffd9ee8555607a28ab9b370d))
- Install crds for cert-manager  by @wrightbradley - ([c32966d](c32966d4f56977c9c7ebcd16b0e919318beb230e))
- Correct portal initiator group id  by @wrightbradley - ([6e57bc9](6e57bc96bdc895a8f3ed51a115732057c5f7a837))
- Update truenas iscsi  by @wrightbradley - ([316f9bf](316f9bf7ad1b0c14f2b21db93eeafb9854c49ae4))
- Grafana alpine dns resolution  by @wrightbradley - ([e3a3e7b](e3a3e7baaab475982b5c05421e73b761ac472340))
- VM naming  by @wrightbradley - ([3f2093a](3f2093ab985dfcadc5f948ce39eed28590498b35))
- Cpu throttling on goldilocks  by @wrightbradley - ([5c2ee61](5c2ee619e65581849c8d5da88d4de60db4d6e661))
- Cpu throttling for otel-collector  by @wrightbradley - ([a303957](a3039576428b7ce232e2bbd7052df1794f1929cc))
- Cpu throttling for vm-logs  by @wrightbradley - ([1373d11](1373d11da0df0f21fa32a8dfcf7935a53fb479e8))
- Nodeselector issues with trivy nodecollector  by @wrightbradley - ([a2edb36](a2edb36364e7b68ee4c3531da5f03d2f47e44e8c))

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
- Disable coredns  by @wrightbradley - ([ce3ead2](ce3ead229b2f0e957ff5c33490068e1f00e82968))
- Setup wakatime  by @wrightbradley - ([8d5df38](8d5df38d586913cef0a1ffe094995c550135941c))
- Don't deploy kube-vip  by @wrightbradley - ([860c7c5](860c7c565cc4065c58de5d419569ee08596161a1))
- Update changelog  by @github-actions[bot] - ([ea7aae8](ea7aae8f9364c65d43328bc1fa1048a64983fcf9))

### <!-- 2 -->🚜 Refactor

- Flux directory structure  by @wrightbradley in [#14](https://github.com/wrightbradley/cloudydad-data-center/pull/14) - ([987a29a](987a29a7b317c8c751cd03eb94f8e9e422edec99))
- Podinfo names  by @wrightbradley in [#16](https://github.com/wrightbradley/cloudydad-data-center/pull/16) - ([4936aba](4936abad160cb737312f9e5cf8a9cf1a720ecebb))
- Apps directory structure  by @wrightbradley in [#17](https://github.com/wrightbradley/cloudydad-data-center/pull/17) - ([e7cf490](e7cf490c5b7b668e9681ee7c479f98e54b4719e3))

### <!-- 5 -->🎨 Styling

- Run linters  by @wrightbradley - ([59f2dbb](59f2dbbd57ccd0f9845f767a6b39ec719cf00f17))
- Update ingress names for vm-logs and vm-metrics  by @wrightbradley - ([e8cf251](e8cf251944bdf226ee2e48f7abe7a6fe7757ed84))
- Run pre-commit linting  by @wrightbradley - ([8f2a250](8f2a2503281055909c33ad736c68c33bd961c3c8))
- Run pre-commit  by @wrightbradley - ([a75227c](a75227ce48f531049653ef710aae6c75cbebee9c))

### <!-- 7 -->📚 Documentation

- Update democratic-csi  by @wrightbradley - ([90f1292](90f1292147a642d698145e48b69f9d9e94797afc))
- Update CHANGELOG.md  by @github-actions[bot] - ([efbdd87](efbdd873fec2afef89abba5571e3ef51b214ca6e))

### <!-- 8 -->🧹 Miscellaneous Tasks

- Disable debug logging for the trueNAS CSI driver  by @wrightbradley - ([8086132](8086132630ad6c6f1c9c074d7749c8a8cf19ec6a))
- Remove vm-metrics, k8s-monitoring, vm-alert  by @wrightbradley - ([ab8c6c5](ab8c6c5da57abee7c7e72b6b6583f4a0656fa09b))
- Add git-cliff changelog config  by @wrightbradley - ([daeecc4](daeecc4cbe93f43dcf5dbcb4fa35000f76cad547))
- Disable Grafana oncall  by @wrightbradley - ([ec5eefb](ec5eefb69e19fcdea20c9065aee11d9c4b29afae))
- Removed unused apps  by @wrightbradley - ([fc52e2c](fc52e2c2c8c14523809381b559ec4a0ff67a19e6))
- Update changelog  by @wrightbradley - ([503e7db](503e7dbfde3d2242ea4cbdad4b789101678e66c7))
- Remove molecule  by @wrightbradley - ([300d573](300d573dd4f225d83c2773e2abde58ad44b4dc80))

### <!-- 9 -->🤖 CI

- Improve conditional workflow executions  by @wrightbradley in [#6](https://github.com/wrightbradley/cloudydad-data-center/pull/6) - ([2768673](2768673d8a982d1b801b51791a77b4706f9704e3))
- Configure github ci and release  by @wrightbradley in [#67](https://github.com/wrightbradley/cloudydad-data-center/pull/67) - ([a71a139](a71a139edc520310b4cd670d5718b50296edb91d))
- Improve release and changelog automation  by @wrightbradley in [#75](https://github.com/wrightbradley/cloudydad-data-center/pull/75) - ([9a9736e](9a9736ed26d19b318ad32a44609028760c2ce57c))
- Use git-cliff action for getting version  by @wrightbradley in [#76](https://github.com/wrightbradley/cloudydad-data-center/pull/76) - ([b70f49f](b70f49f147f1a74045f4620f498b82921eaf7186))


## New Contributors
* @github-actions[bot] made their first contribution
* @wrightbradley made their first contribution in [#76](https://github.com/wrightbradley/cloudydad-data-center/pull/76)
* @dependabot[bot] made their first contribution in [#18](https://github.com/wrightbradley/cloudydad-data-center/pull/18)
* @ made their first contribution

<!-- generated by git-cliff -->
