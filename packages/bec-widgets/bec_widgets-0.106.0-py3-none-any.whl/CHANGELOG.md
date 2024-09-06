# CHANGELOG

## v0.106.0 (2024-09-05)

### Feature

* feat(plot_base): toggle to switch outer axes for plotting widgets ([`06d7741`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/06d7741622aea8556208cd17cae521c37333f8b6))

### Refactor

* refactor: use DAPComboBox in curve_dialog selection ([`998a745`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/998a7451335b1b35c3e18691d3bab8d882e2d30b))

### Test

* test: fix tests ([`6b15abc`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/6b15abcc73170cb49292741a619a08ee615e6250))

## v0.105.0 (2024-09-04)

### Feature

* feat: add dap_combobox ([`cc691d4`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/cc691d4039bde710e78f362d2f0e712f9e8f196f))

### Refactor

* refactor: cleanup and renaming of slot/signals ([`0fd5cee`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/0fd5cee77611b6645326eaefa68455ea8de26597))

* refactor(logger): changed prints to logger calls ([`3a5d7d0`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/3a5d7d07966ab9b38ba33bda0bed38c30f500c66))

## v0.104.0 (2024-09-04)

### Documentation

* docs(scan_control): docs extended ([`730e25f`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/730e25fd3a8be156603005982bfd2a2c2b16dff1))

### Feature

* feat(scan_control): scan control remember the previously set parameters and shares kwarg settings across scans ([`d28f9b0`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/d28f9b04c45385179353cc247221ec821dcaa29b))

### Fix

* fix(scan_control): SafeSlot applied to run_scan to avoid faulty scan requests ([`9047916`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/90479167fb5cae393c884e71a80fcfdb48a76427))

* fix(scan_control): scan parameters can be loaded from the last executed scan from redis ([`ec3bc8b`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/ec3bc8b5194c680b847d3306c41eef4638ccfcc7))

* fix(toggle): state can be determined with the widget initialisation ([`2cd9c7f`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/2cd9c7f5854f158468e53b5b29ec31b1ff1e00e6))

### Refactor

* refactor(scan_control): scan control layout adjusted ([`85dcbda`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/85dcbdaa88fe77aeea7012bfc16f10c4f873f75e))

* refactor(scan_control): basic pydantic config added ([`fe8dc55`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/fe8dc55eb102c51c34bf9606690914da53b5ac02))

### Test

* test(scan_control): tests extended for getting kwargs between scan switching and getting parameters from redis ([`b07e677`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/b07e67715c9284e9bf36056ba4ba8068f60cbaf3))

* test(conftest): only run cleanup checks if test passed ([`26920f8`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/26920f8482bdb35ece46df37232af50ab9cab463))

## v0.103.0 (2024-09-04)

### Ci

* ci: prefill variables for manual pipeline start ([`158c19e`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/158c19eda771562a325fd59405f9fd4cb9a17ed6))

### Feature

* feat(vscode): open vscode on a free port ([`52da835`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/52da835803f2453096a8b7df23bee5fdf93ae2bb))

* feat(website): added method to wait until the webpage is loaded ([`9be19d4`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/9be19d4abebad08c5fc6bea936dd97475fe8f628))

### Fix

* fix(theme): fixed segfault for webengineview for auto updates ([`9866075`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/9866075100577948755b563dc7b7dc4cdc60d040))

### Test

* test(webview): fixed tests after refactoring ([`d5eb30c`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/d5eb30cd7df4cb0dc3275dd362768afc211eaf2d))

* test(vscode): popen call does not have to be the only one ([`39f98ec`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/39f98ec223ba8b59e478ac788c08c59ffe886b4e))

## v0.102.0 (2024-09-04)

### Documentation

* docs(buttons): buttons section of docs split to appearance and queue buttons ([`047aa26`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/047aa26a60220c826cc1375cf81daf11d1f3ab5c))

* docs(tests): added tests tutorial for widget ([`18d8561`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/18d8561c965d149a7662085f7dbe2a39a8c4a475))

### Feature

* feat(queue): BECQueue controls extended with Resume, Stop, Abort, Reset buttons ([`0d7c10e`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/0d7c10e670e4937787e1afaa19ca8259ac752486))

### Fix

* fix(queue_reset_button): queue reset has to be confirmed with msgBox ([`9dd43aa`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/9dd43aa1fd3991368002605df4389a7a7271011b))

### Refactor

* refactor(tests): positioner box test changed to use create_widget fixture ([`df5eff3`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/df5eff3147c79ff0278e6a5a09c8f73d5236aed3))

## v0.101.0 (2024-09-02)

### Feature

* feat: add Dap dialog widget ([`9781b77`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/9781b77de27b2810fbb1047a61b1832dd186db01))

### Refactor

* refactor: add docs, cleanup ([`61ecf49`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/61ecf491e52bfbfa0d5a84764a9095310659043d))

## v0.100.0 (2024-09-01)

### Documentation

* docs(becwidget): improvements to the bec widget base class docs; fixed type hint import for sphinx ([`99d5e8e`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/99d5e8e71c7f89a53d7967126f4056dde005534c))

### Feature

* feat(theme): added theme handler to bec widget base class; added tests ([`7fb938a`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/7fb938a8506685278ee5eeb6fe9a03f74b713cf8))

### Fix

* fix(pyqt slot): removed slot decorator to avoid problems with pyqt6 ([`6c1f89a`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/6c1f89ad39b7240ab1d1c1123422b99ae195bf01))

## v0.99.15 (2024-08-31)

### Fix

* fix(theme): update pg axes on theme update ([`af23e74`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/af23e74f71152f4abc319ab7b45e65deefde3519))

* fix(positioner_box): fixed positioner box dialog; added test; closes #332 ([`0bf1cf9`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/0bf1cf9b8ab2f9171d5ff63d4e3672eb93e9a5fa))

## v0.99.14 (2024-08-30)

### Fix

* fix(color_button): signal and slot added for selecting color and for emitting color after change ([`99a98de`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/99a98de8a3b7a83d71e4b567e865ac6f5c62a754))

* fix(color_button): inheritance changed to QWidget ([`3c0e501`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/3c0e501c56227d4d98ff0ac2186ff5065bff8d7a))

## v0.99.13 (2024-08-30)

### Documentation

* docs: minor updates to the widget tutorial ([`ec9c8f2`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/ec9c8f29633364c45ebd998a5411d428c1ce488d))

* docs(widget tutorial): step by step guide added ([`b32ced8`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/b32ced85fff628a9e1303a781630cdae3865238e))

### Fix

* fix(dark mode button): fixed dark mode button state for external updates, including auto ([`a3110d9`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/a3110d98147295dcb1f9353f9aaf5461cba9232a))

## v0.99.12 (2024-08-29)

### Fix

* fix(toolbar): widget action added ([`2efd487`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/2efd48736cbe04e84533f7933c552ea8274e2162))

* fix(reset_button): reset button added ([`6ed1efc`](https://gitlab.psi.ch/bec/bec_widgets/-/commit/6ed1efc6af193908f70aa37fb73157d2ca6a62f4))
