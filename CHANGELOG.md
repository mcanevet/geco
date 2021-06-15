# Changelog

### [0.1.1](https://www.github.com/mcanevet/geco/compare/v0.1.0...v0.1.1) (2021-06-15)


### Bug Fixes

* use AirportItlwm v1.3.0 for now ([1be3414](https://www.github.com/mcanevet/geco/commit/1be341409cb7eab1a355a5acc0020d341acfd597))

## 0.1.0 (2021-06-15)


### Features

* add Drivers to Config.plist ([c720e1c](https://www.github.com/mcanevet/geco/commit/c720e1c84cc1954aa55adb13a17077e2cf3ed875))
* add Tools to Config.plist ([c9d5ca8](https://www.github.com/mcanevet/geco/commit/c9d5ca84d5a7139eae251c66dcab35a2df610099))
* apply Augeas transformations from profile ([b74de56](https://www.github.com/mcanevet/geco/commit/b74de56799a3c07bfc148faa627084d42f83e2e7))
* build and publish Docker image ([95c43d6](https://www.github.com/mcanevet/geco/commit/95c43d6b1fcbaf9e2c3a9a857aad38d24b6eae6b))
* **ci:** add commitsar lint test ([41e9af9](https://www.github.com/mcanevet/geco/commit/41e9af9352409f776b97ce96aca0ffc39496aadd))
* **ci:** add release-please action ([3b9f4ac](https://www.github.com/mcanevet/geco/commit/3b9f4ac3671fd73dd2c870191533d0528bdef848))
* **ci:** add workflow for pytest ([8251550](https://www.github.com/mcanevet/geco/commit/8251550c22be505272e145e413018da2e72125ec))
* **ci:** add yamllint check ([4190cac](https://www.github.com/mcanevet/geco/commit/4190cacfb0f18ae11d2abae591e9d439df3f1626))
* compile SSDTs ([96c1956](https://www.github.com/mcanevet/geco/commit/96c1956e9c6a280a378b4975ed79ffca5c1a04a2))
* configure Kernel section of Config.plist ([66cb641](https://www.github.com/mcanevet/geco/commit/66cb641a8ae02a5e3670ba2a238e3c251ec74e33))
* **core:** add mandatory profile argument ([2e85890](https://www.github.com/mcanevet/geco/commit/2e85890ee942b30b583cecda0b11e4ea152e8244))
* **core:** support verbose mode ([8d46f2b](https://www.github.com/mcanevet/geco/commit/8d46f2bb15f9f60120876b6f197b3a97823658f1))
* create EFI directory ([aec486f](https://www.github.com/mcanevet/geco/commit/aec486f8348741c84bf843940333d4cdb0eca213))
* **doc:** add README.md ([e9a0d93](https://www.github.com/mcanevet/geco/commit/e9a0d936d69a123be60109a0614461f369bdd0ff))
* download Kexts ([10eddf5](https://www.github.com/mcanevet/geco/commit/10eddf51ba8915df0fb39cdb9c924556b74981e4))
* download OCBinaryData ([097c067](https://www.github.com/mcanevet/geco/commit/097c06771f7cedfdad4d590fe5e006d5cfa0afb4))
* download OpenCore ([45e4902](https://www.github.com/mcanevet/geco/commit/45e4902116fd1804b7e8ab44c1029cc1e4f4439b))
* patch Config.plist using Augeas ([6ec8e07](https://www.github.com/mcanevet/geco/commit/6ec8e073461a9557276560f49c5f13d6b0517fb1))
* populate ACPI section in config.plist ([f10ada4](https://www.github.com/mcanevet/geco/commit/f10ada4cc5fa560db81dc2d0e8e54b61c7524b58))
* **profile:** add Profile class ([60350d1](https://www.github.com/mcanevet/geco/commit/60350d19abe2b70ac2b6f3dfe3df2f033201d10b))
* **profile:** load profile ([871944f](https://www.github.com/mcanevet/geco/commit/871944f00415611e84701abad80abf9bb27ff947))
* set comments in ACPI section ([1545419](https://www.github.com/mcanevet/geco/commit/1545419e26a92616d6568aa386528b920184e202))
* use macos-latest for github workflow ([ef171b1](https://www.github.com/mcanevet/geco/commit/ef171b11b90ce71699cbc4580a1c1d2dfe083595))
* verify checksum ([7e955c5](https://www.github.com/mcanevet/geco/commit/7e955c503d0df53e73c1f0c21e41616804bf551f))


### Bug Fixes

* AirportItlwm.kext source ([5ccf318](https://www.github.com/mcanevet/geco/commit/5ccf318d964fe7b0f1653db43d8bd15abbf2a0ed))
* AirportItlwm.kext URL ([af45d48](https://www.github.com/mcanevet/geco/commit/af45d48ec51c4a94e0bc252e4645e2bd0ec8db5a))
* AirportItlwm.kext URL ([e35c2c7](https://www.github.com/mcanevet/geco/commit/e35c2c742b32bbadcf4a5e2e9744164748113e28))
* also add Kext plugins ([d9595c3](https://www.github.com/mcanevet/geco/commit/d9595c304f59cf91e3e0156426057cd7445a456c))
* catch error when saving file with Augeas ([facf9d9](https://www.github.com/mcanevet/geco/commit/facf9d930f02a2733365e18ed294d67c908d51a6))
* don't prefix AML file with CWD ([460e3cf](https://www.github.com/mcanevet/geco/commit/460e3cf70bd1a49a4e4b1505aa43cc8629a6710f))
* don't prefix Augeas root with CWD ([212a2e5](https://www.github.com/mcanevet/geco/commit/212a2e504237c9a762fc72fd5baf47e7102b9815))
* emptry string are properly rendered ([c38db5d](https://www.github.com/mcanevet/geco/commit/c38db5d291a60fe6537446dbc3c7a747c9e48ca0))
* some Config.plist formatting ([7598ab6](https://www.github.com/mcanevet/geco/commit/7598ab6db771bb3082f03e6b4de6041627e5c8fc))
* use Augeas with noload and noautoload ([696c021](https://www.github.com/mcanevet/geco/commit/696c0217caaddd41daf9e04f7f991bd1c616bd8b))
* wrong OpenShell.efi location ([ffc4c3b](https://www.github.com/mcanevet/geco/commit/ffc4c3be5173982f2760fc922ba8ca7885e362b6))
