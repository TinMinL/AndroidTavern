# 当前状态

版本：0.1.0-preview.2（已构建并发布，待真机复验）。

已确认故障：旧就绪检测漏掉原版 setWindowTitle 写在成功日志前的 OSC 控制段，导致就绪标记始终为假，并在 20 分钟后超时。新增用例在旧代码上复现失败，修正后 25 项 JVM 断言通过。

已验证：GitHub 构建 39142494691 成功；24 个运行库文件校验通过；APK v2/v3 签名通过。APK 源码提交 79f4b352357a33aa86407035f148982be51c29f2。

直接下载：https://github.com/TinMinL/AndroidTavern/releases/download/v0.1.0-preview.2/SillyTavern-Pilot-0.1.0-preview.2-ci-arm64.apk

新包身份 com.sillytavern.localpilot.ci2，图标「酒馆试用2·1」。旧 CI 使用未保留的临时密钥，无法覆盖升级，因此采用并排安装保留旧数据；测试前先停止旧服务，避免端口 18080 冲突。

下一步：用户在 Redmi 上验证新包是否进入酒馆首页；若仍失败，收集实际日志重新诊断，不盲目延长超时。随后才验证角色卡、酒馆助手/MVU、切后台与锁屏生成。

待完成：可靠后台生成、进程死亡恢复、安全升级回退、固定发行签名、APK 自动更新及完整日志查看界面。未读取或修改用户 Termux 数据，未调用模型服务。
