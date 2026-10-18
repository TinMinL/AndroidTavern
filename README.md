# AndroidTavern · 酒馆 Android 试用版

把原版 SillyTavern 前端与 Node.js 后端一起装进 Android：点击桌面图标即可启动，不必每次输入 Termux 指令，也不必另开浏览器。

**当前版本：0.1.0-preview.2，ARM64，Android 7.0 及以上。已构建 APK，尚待真机验收。**

## 下载与试用

- **[直接下载 APK（约 179 MB）](https://github.com/TinMinL/AndroidTavern/releases/download/v0.1.0-preview.2/SillyTavern-Pilot-0.1.0-preview.2-ci-arm64.apk)**：下载后打开安装，无需解压 ZIP。
- [版本说明](https://github.com/TinMinL/AndroidTavern/releases/tag/v0.1.0-preview.2)：本次是启动检测修复版，桌面图标为「酒馆试用2·1」。
- **旧版卡在准备中？** 先到旧「酒馆 CI·管理」点 Stop，再安装并打开新版。无需卸载旧版；新版独立存储，不自动迁移旧数据。修复详情见 [启动故障记录](evidence/startup-fix.md)。
- [安装和测试说明](TRYOUT.md)：首次启动、导入、扩展及切后台测试顺序。
- [自动构建](https://github.com/TinMinL/AndroidTavern/actions)：成功运行后可在 Artifacts 下载 CI 测试包，需要登录 GitHub。CI 包与已有试用包使用不同应用 ID，避免覆盖已有试用数据。
- [当前进度](NEXT.md) · [构建说明](BUILDING.md) · [反馈问题](https://github.com/TinMinL/AndroidTavern/issues)

## 保留原版环境

应用内使用 Android WebView 展示原版界面，原版 Node.js 服务在本机运行。前端仍是 Web 技术；没有重写成 Tauri/Rust 服务，也不承诺仅换成 APK 就降低内存占用。

SillyTavern 固定为 **1.18.0**。预设、角色卡、世界书、正则和扩展继续走原版的数据格式与接口。保留接口不等于全部插件已经验证，酒馆助手、MVU 及外部程序依赖仍需要逐项真机测试。

| 能力 | 本版状态 |
|---|---|
| 点击图标启动内置服务和界面 | 已实现，等待真机验证 |
| 前台服务、唤醒锁、返回时保留页面 | 已接入；后台生成与锁屏稳定性未验收 |
| 原版导入导出、备份 ZIP 导入 | 已接入；部分主机数据往返测试通过 |
| 检查酒馆更新 | 只检查版本，不执行替换 |
| 扩展安装及更新 | 保留原版入口，兼容性待测 |
| 系统结束进程后恢复回复 | 尚未实现 |
| 酒馆安全升级、回退、APK 自动更新 | 尚未实现 |

原私有试用包身份为 `com.sillytavern.localpilot`，本次公开 CI 包为 `com.sillytavern.localpilot.ci2`；首个实例都使用端口 `18080`，请先停止另一版本的服务再启动。数据在应用私有目录；不会自动迁移 Termux 数据。**卸载会删除本应用的数据，请先导出备份。**

## 源码导航

- `app/src/main/java/com/sillytavern/app/`：启动、WebView、服务、导入导出、更新检查。
- `scripts/prepare_runtime.py`：从固定上游提交取得 24 个运行库文件，检查 SHA-256 和大小。
- `scripts/build_preview.py`：通过官方 Android SDK 编译、打包、测试签名。
- `tests/`：JVM 逻辑断言及酒馆主机数据往返测试。
- `evidence/`：此前交付 APK 的验证记录，不能替代真机验收。
- `runtime/binaries.lock.json`：固定二进制依赖，避免在新仓库重复存储大型 LFS 文件。

本仓库直接提供修改后的 Android 源码。酒馆源码及大型运行库沿用固定上游版本，构建前由脚本取得。未包含签名密钥、聊天数据、角色卡或 API 密钥。

## 来源与许可

Android 包装层基于 [doomedskull1011/SillyTavernAndroid](https://github.com/doomedskull1011/SillyTavernAndroid/tree/c6e0689e539935bd5dd89d7a569adeaf6317583b)，固定提交 `c6e0689e539935bd5dd89d7a569adeaf6317583b`。原始说明保留在 [UPSTREAM-README.md](UPSTREAM-README.md)，其中功能和下载链接描述的是上游项目，不是本试用版。

SillyTavern 官方源码为 [1.18.0 / 51ad27f](https://github.com/SillyTavern/SillyTavern/tree/51ad27fb86d39a3daca3adaa970375c9670c12df)，许可原文见 [LICENSE-SillyTavern.txt](LICENSE-SillyTavern.txt)。本次未修改酒馆内核。包装层和运行库来源说明见 [THIRD_PARTY.md](THIRD_PARTY.md)。
