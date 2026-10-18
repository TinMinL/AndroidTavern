# 构建

需要 Linux、Git、Git LFS、Python 3.11+、JDK 17、Android SDK platform 34 / build-tools 34.0.0。Windows 可使用 Android Studio/Gradle 路径，但本次交付验证的是下方官方 SDK 直接构建路径。

```bash
git clone https://github.com/TinMinL/AndroidTavern.git
cd AndroidTavern
python3 scripts/prepare_runtime.py
python3 scripts/build_preview.py --sdk "$ANDROID_HOME" --jdk "$JAVA_HOME" --keystore /private/path/pilot-test.jks
```

首次准备需要下载约数百 MB 运行库，并联网访问固定上游及 Git LFS。脚本只在全部文件大小与 SHA-256 匹配后复制。也可以使用已完成 `git lfs pull` 的固定上游检出：

```bash
python3 scripts/prepare_runtime.py --source /path/to/pinned-upstream
python3 scripts/prepare_runtime.py --verify-only
```

输出：`build/pilot/SillyTavern-Pilot-0.1.0-preview.2-arm64.apk`。

## 签名

`build_preview.py` 只用于开发试用。若指定密钥不存在，会在该路径创建独立测试密钥；请放在仓库之外并妥善备份。脚本使用开发口令 `android` 与别名 `pilot-test`，不适合作为正式发行签名方案。公开源码中没有密钥文件。

新生成的密钥不能覆盖安装此前私有试用包。升级必须保留相同应用 ID 和签名，并提高版本号。不要为安装新签名而直接卸载含有聊天记录的旧包。

## GitHub Actions

`Android preview` 在 `main` 源码提交或手动触发后运行：固定运行库校验、25 项主机逻辑断言、SDK 构建、APK 签名验证，然后上传测试 APK 和 SHA-256。

CI 包改用 `com.sillytavern.localpilot.ci2`，图标为「酒馆试用2」，独立于已有私有试用版。每次运行使用临时测试密钥，因此不同运行的 CI 包不能直接覆盖升级；仅用于空白测试环境。临时密钥不会上传，CI 不会自动发布正式 Release。

CI 与原试用版仍使用相同本地端口；测试 CI 前，请先从原试用版管理页停止其服务，避免端口冲突。

Actions 成功不代表 Android 真机和扩展兼容性通过。正式发行前需建立持续保管的签名及更新流程。

## 本地逻辑验证

```bash
mkdir -p build/host-tests
javac -d build/host-tests app/src/main/java/com/sillytavern/app/ArchivePaths.java app/src/main/java/com/sillytavern/app/StableVersion.java app/src/main/java/com/sillytavern/app/ServerReadiness.java tests/HostLogicTest.java
java -cp build/host-tests com.sillytavern.app.HostLogicTest
```

Gradle 配置也保留在仓库；此前交付环境未完成 Gradle 依赖解析，不把它列作已验证构建路径。
