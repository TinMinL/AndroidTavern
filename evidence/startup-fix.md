# Preview 2：启动成功日志检测修复

## 证据与决定

范围：25d08db 基线的 ServerReadiness、对应单元测试，以及发出新 APK 所需的版本/安装身份。结构决定 Local Fix；执行决定 Local Fix Only。Android 业务逻辑修改限定 2 个文件、80 行以内；版本打包修改限定 app/build.gradle 与 scripts/build_preview.py，另记录本报告。不改酒馆内核、数据格式、迁移或插件。

已确认目标：应用自身 Node 服务就绪且 HTTP 能响应时进入原版页面。红线：不将其他进程/端口当成本应用，不清除或迁移用户数据。验收：真实上游日志格式的测试修前失败、修后通过，APK 构建与签名验证，再由用户确认手机进入首页。这些目标、红线和验收沿用原任务授权，构成 A0 开门回执。

路线：code-quality-workflow；已读共享沟通、gate-change-verify 与 library-usage。route-map 中该路线无额外领域指南；A0 文本和完整路由目录资源未能读取，按显式三项开门条件记录，不宣称完整路由器已执行。没有设计候选或全仓审查。

## 根因

固定上游 c6e0689 的 payload/sillytavern/src/server-main.js 在输出 `SillyTavern is listening on` 前调用 setWindowTitle。src/util.js 在非 Windows 平台写入 OSC 2 终端标题，以 ESC + 反斜线结束，且不带换行。

Android 的 BufferedReader.readLine 因此会读到“终端标题 + 启动成功文本”组成的同一行。旧 ServerReadiness 只移除 ANSI 颜色字符，随后要求 startsWith 启动文本，必然拒绝该格式。InstanceActivity 又把该标记作为发出 HTTP 探测的前提，导致即使 Node 已就绪仍等待 20 分钟后报超时。

用户截图与这一故障一致，但没有手机完整日志，不能据此排除其他设备问题。截图中的最后一条分隔线由加载页只取日志末行造成，不能当作完整诊断日志。

## 改动与验证

先去掉完整的 OSC 终端控制段（ESC-backslash 或 BEL 终止），再执行原颜色清理和精确端口检查。继续只观察自己启动的进程，继续要求 HTTP 成功，不跳过所有权检测。

新增 6 个用例：真实标题前缀、标题与颜色混用、BEL 结尾、错误端口、标题内容伪装成启动消息、未结束的标题。

基线验证：新增用例在旧匹配器上以 `AssertionError: real upstream OSC title prefix` 失败。修改后：`PASS: 25 host logic assertions`。本地通过 JDK 17 的 jdk.compiler 模块执行编译，未依赖缺失的 javac 启动文件。

回退：还原匹配器的这一改动即可；没有数据格式或存储变更。停止条件：如真机仍失败，收集实际日志重新诊断，不继续放宽就绪检测。

## 安装与剩余风险

旧公开 CI 包使用临时签名且没有保存私钥，无法覆盖升级。新公开包采用独立应用身份 com.sillytavern.localpilot.ci2，图标“酒馆试用2”，不卸载或覆盖旧包。测试前须在“酒馆 CI·管理”中 Stop 旧实例，避免端口 18080 冲突。新包不自动读取旧数据。

APK 编译成功不等于真机验收完成；Redmi 启动、酒馆助手/MVU、后台生成仍待手机验证。稳定发行签名方案、完整日志查看界面属于后续工作，本次不混入启动检测修复。
