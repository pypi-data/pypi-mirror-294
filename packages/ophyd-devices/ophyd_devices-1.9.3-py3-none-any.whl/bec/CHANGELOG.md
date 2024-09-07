# CHANGELOG

## v2.31.0 (2024-09-05)

### Feature

* feat(scan_report): added public files to scan item and report on the master file in scan report ([`adca248`](https://gitlab.psi.ch/bec/bec/-/commit/adca248dfd592b1cdbfa2cddf1a10c13ac11e176))

### Test

* test: added test for file events ([`b976fb4`](https://gitlab.psi.ch/bec/bec/-/commit/b976fb4a084910da5ae0a4fac32d1152b0f1cc04))

## v2.30.2 (2024-09-05)

### Fix

* fix: updated device_config of pseudo_signal1 ([`529663f`](https://gitlab.psi.ch/bec/bec/-/commit/529663f4fdef795c7863622ee01328bf3a1385a6))

### Refactor

* refactor: ScanItem attributes bec and callback made private ([`a70af8f`](https://gitlab.psi.ch/bec/bec/-/commit/a70af8f58cba31294a6b84bb1b45d62f2dcb4cc0))

* refactor: refactoring to make scan_manager optional kwarg ([`a5ccefa`](https://gitlab.psi.ch/bec/bec/-/commit/a5ccefa978aa2b3c79d7b4617614bbde689036a0))

### Test

* test: fix tests ([`46738ad`](https://gitlab.psi.ch/bec/bec/-/commit/46738ad259c9e99095067b67ffbacbaff83115ea))

## v2.30.1 (2024-09-05)

### Fix

* fix: fix hints for devices of type ophyd.signal ([`1b8b2c7`](https://gitlab.psi.ch/bec/bec/-/commit/1b8b2c7b490113e0b7acd3a070c9bec1c1626b4f))

* fix: bugfix in cont_line_scan; reworked device and signal mocks ([`c91dcf4`](https://gitlab.psi.ch/bec/bec/-/commit/c91dcf4d37bc1add18d2f0682af97358e4abdee6))

### Refactor

* refactor: reworked R/W info in device info; removed bug for devices with type Signal ([`d0ee4ec`](https://gitlab.psi.ch/bec/bec/-/commit/d0ee4ec5544dcc400568dc5311cea0e1d4074c8e))

## v2.30.0 (2024-09-04)

### Feature

* feat(logger): added option to disable modules; added retention and rotation; changed log format for stderr ([`868f40d`](https://gitlab.psi.ch/bec/bec/-/commit/868f40db8e1420dab7eaf3fed6eed2e8313ab539))

## v2.29.0 (2024-09-02)

### Ci

* ci: prefill variables for manual pipeline start ([`d4b4bf8`](https://gitlab.psi.ch/bec/bec/-/commit/d4b4bf816a73923a90d0e7d1d5158f0e26016e92))

### Feature

* feat(config): added support for adding and removing devices ([`070b041`](https://gitlab.psi.ch/bec/bec/-/commit/070b0417d80c56b69093c768d25238cb0465de36))

### Fix

* fix(device_manager): fixed init value for failed devices ([`61c4fb6`](https://gitlab.psi.ch/bec/bec/-/commit/61c4fb69cdc068bdc997a53b26fccc15f00217b1))

## v2.28.0 (2024-09-02)

### Feature

* feat(queue schedule): added endpoint and queue schedule methods ([`0c7e0eb`](https://gitlab.psi.ch/bec/bec/-/commit/0c7e0eb37f3d88e94bbb0ae0ee346b9736bc582c))

## v2.27.0 (2024-08-30)

### Documentation

* docs(stubs): improvements to the stubs doc strings ([`89b4353`](https://gitlab.psi.ch/bec/bec/-/commit/89b4353433c603398e8c87da36e6ebc7aa2fc47c))

* docs(stubs): minor improvements to the wait docstring ([`9db0c03`](https://gitlab.psi.ch/bec/bec/-/commit/9db0c03bec9aa2fa50e2ad727d0a43727c2db482))

### Feature

* feat(endpoint): added stop_all_devices endpoint ([`13beb51`](https://gitlab.psi.ch/bec/bec/-/commit/13beb51a520e9ef6569fff45807bd50d076ce787))

### Fix

* fix(ipython client): fixed magic command for resume ([`2289036`](https://gitlab.psi.ch/bec/bec/-/commit/228903628b3dd624a20bea48ccf65ec9ff1cc5ed))

* fix(queue): moved queue modifications to dedicated message for the device server ([`3e0e5cf`](https://gitlab.psi.ch/bec/bec/-/commit/3e0e5cf9a8ab477acdbeb85b703beb86207fec18))

### Refactor

* refactor(docs): new bec logo ([`4070521`](https://gitlab.psi.ch/bec/bec/-/commit/4070521e6c4b6b8ee6b29730fdefb5def2f5be22))

## v2.26.0 (2024-08-22)

### Feature

* feat(bec_lib): print all asap client messages during rpc ([`5de3235`](https://gitlab.psi.ch/bec/bec/-/commit/5de3235788f5bc573e2b1daa2c81c977e200e921))

## v2.25.1 (2024-08-22)

### Fix

* fix: try/expect CONSOLE logger changed order ([`ca36128`](https://gitlab.psi.ch/bec/bec/-/commit/ca3612816bcb1bd86bc2480724fad57ce9af9892))

## v2.25.0 (2024-08-22)

### Feature

* feat(server): added endpoint and handler to restart server through redis ([`9bde681`](https://gitlab.psi.ch/bec/bec/-/commit/9bde68138c5930c0f050ffd9ee6fcd21a294a488))

## v2.24.0 (2024-08-21)

### Feature

* feat(lmfit): added fallback to hinted signals; added oversampling option ([`b66b928`](https://gitlab.psi.ch/bec/bec/-/commit/b66b9286899a69ab8bc71ec2a65e16189e52cb07))

## v2.23.2 (2024-08-21)

### Fix

* fix(docs): scan gui config tutorial added to toc ([`343309f`](https://gitlab.psi.ch/bec/bec/-/commit/343309ff5e224227e15076fc94a124a4c76262b4))

## v2.23.1 (2024-08-19)

### Fix

* fix(serialization): added json decoder as fallback option for raw messages ([`5e7f630`](https://gitlab.psi.ch/bec/bec/-/commit/5e7f630ce7b2e7a3ff3337d966155e4b5f5cc7ff))

### Test

* test: wait for dap to finish ([`be0d589`](https://gitlab.psi.ch/bec/bec/-/commit/be0d589ae89cc663687402fd4c2fb0a738643f22))

## v2.23.0 (2024-08-17)

### Feature

* feat(client): added client event for updated devices ([`7573ce1`](https://gitlab.psi.ch/bec/bec/-/commit/7573ce1b52e47106dfa7ab8b814420aeb1d14591))

## v2.22.1 (2024-08-16)

### Fix

* fix: remove unused imports, add missing import ([`92b5e4a`](https://gitlab.psi.ch/bec/bec/-/commit/92b5e4a50b45ee9d960fcf9839500fc420b9e0be))

### Test

* test: add connector unregister test with &#39;patterns&#39; ([`7f93933`](https://gitlab.psi.ch/bec/bec/-/commit/7f93933847dd387847930fb81171ca29f1b2d3be))

## v2.22.0 (2024-08-16)

### Ci

* ci: use target branch instead of default pipeline branch for e2e tests ([`83e0097`](https://gitlab.psi.ch/bec/bec/-/commit/83e00970d1e5f105ee3e05bce6fd7376bd9698e4))

### Feature

* feat(device_server): gracefully handle timeouts

Failed config updates should only lead to config flush if the object initialization fails. If we simply can&#39;t connect to the signals, the device should be disabled. ([`ec5abd6`](https://gitlab.psi.ch/bec/bec/-/commit/ec5abd6dde4c71e41395ee6f532f27f24215e168))

### Fix

* fix: fixed bug in client fixture for loading configs ([`7636f4d`](https://gitlab.psi.ch/bec/bec/-/commit/7636f4d15a36a4f32a202643771e4b5d97ff5ae6))

* fix(client): handle deviceconfigerrors more gracefully in the console ([`433b831`](https://gitlab.psi.ch/bec/bec/-/commit/433b8313021eb89fd7135fa79504ba34270d12eb))

### Test

* test: fixed data access in dummy controller device ([`624c257`](https://gitlab.psi.ch/bec/bec/-/commit/624c25763fdef2a9ee913e5936311f421bd9b8d6))
