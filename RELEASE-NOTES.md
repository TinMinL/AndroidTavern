# 发布记录

## 已发布：0.1.0-preview.2（启动修复）

[直接下载 APK](https://github.com/TinMinL/AndroidTavern/releases/download/v0.1.0-preview.2/SillyTavern-Pilot-0.1.0-preview.2-ci-arm64.apk)

修复终端标题控制段导致启动成功日志无法被识别的问题。25 项逻辑测试、24 个运行库校验、APK 编译与 v2/v3 签名验证通过，尚待真机复验。

文件 SHA-256：`61b7ec406e8b8268f8fb32e47939075fd6557ae40794e56a2cbc3549fec7453b`。

图标「酒馆试用2·1」，应用身份 `com.sillytavern.localpilot.ci2`。先停止旧「酒馆 CI」服务再运行新版；无需卸载旧版，不自动迁移数据。


## 已发布：0.1.0-preview.1-ci.2

[直接下载 APK](https://github.com/TinMinL/AndroidTavern/releases/download/v0.1.0-preview.1-ci.2/SillyTavern-Pilot-0.1.0-preview.1-ci-arm64.apk) · [Release](https://github.com/TinMinL/AndroidTavern/releases/tag/v0.1.0-preview.1-ci.2)

发布复用构建 39135974527 的 APK，哈希校验通过。文件大小 179271830 字节，SHA-256 为 `1951137e4b21d086df67708c4e3e0dbfd952618d71226f2aa75ebcc99a099b7c`。

应用身份为 `com.sillytavern.localpilot.ci`，使用该次构建的临时测试签名，尚待真机与扩展验收。后续其他 CI 构建不能保证覆盖升级。

## 原私有试用包：发布草稿（未上传）

首个 ARM64 试用版。原版 SillyTavern 1.18.0 前后端运行在手机本地，独立应用身份和端口，一键启动，保留文件导入导出及只读更新检查。

尚未通过真机安装、后台生成和酒馆助手/MVU 兼容验收；不包含进程死亡后的回复恢复、安全升级回退或 APK 自动更新。请先使用测试数据。

现有私有试用 APK（不是 CI 每次重新生成的包）：

- 文件名：`SillyTavern-Pilot-0.1.0-preview.1-arm64.apk`
- 文件大小：179271830 字节
- SHA-256：`c2b22f240cd5801bd9dcffc2f77fa06bd89cc0eeab6206b0d12327bcb31854f5`
- 签名证书 SHA-256：`ec437fe58c33c07d46cad47face3410d2ecac8e0436288396ae5023f0a737092`

## 上传现有文件

在 GitHub Releases 新建 `v0.1.0-preview.1`，勾选预发行版，把上述 APK 作为附件，并使用本说明。上传前核对文件哈希。**不要上传私有源码续接 ZIP，它包含测试签名密钥。**

原私有包仍未上传；公开 CI 包已通过 GitHub Actions 发布到 Releases。以上原私有包的文件名和哈希不适用于公开 CI 包。
