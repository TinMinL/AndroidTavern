# GitHub 接入状态

目标：`https://github.com/TinMinL/AndroidTavern`。

2026-10-18：账号最初只完成用户授权，没有安装 GitHub App；提交返回 `403 Resource not accessible by integration`。将 ChatGPT Codex Connector 安装到 TinMinL 并授权本仓库后，README 写入已成功。

## 源码与构建

源码在仓库根目录，构建流程见 `.github/workflows/android-preview.yml`。最新执行结果以仓库 Actions 页面为准；编译通过不代表真机验收。

此前已完成 Python 语法检查和 24 项实际运行库哈希与大小校验。原交付 APK 的 19 项 JVM 测试记录在 evidence/，CI 会再次运行这些断言。

现有 APK 的 Release 附件还未上传，步骤与校验值见 RELEASE-NOTES.md。公开源码包不包含任何签名密钥；私有续接包不得上传。
