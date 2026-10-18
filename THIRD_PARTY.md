# 上游与第三方说明

1. Android 包装层及原生运行库：doomedskull1011/SillyTavernAndroid，提交 `c6e0689e539935bd5dd89d7a569adeaf6317583b`。保留原始说明 UPSTREAM-README.md。该基线未单独明确包装层许可证，本项目不替原作者追加授权声明；正式分发前仍需确认其授权范围。
2. SillyTavern：官方 `51ad27fb86d39a3daca3adaa970375c9670c12df`（1.18.0），AGPL-3.0，全文见 LICENSE-SillyTavern.txt。固定上游 `payload/sillytavern/` 也保留可阅读的对应源码。
3. Node.js、Git、npm 及其依赖：使用固定上游提供的 Android 运行库。各组件遵循原有许可，不因包含于本项目而统一变更许可。`runtime/` 保留上游二进制处理脚本。正式发行前还需完善完整第三方许可清单和所需对应源码交付。

本项目当前是可检查源码、构建和验证的试用阶段。现有源码对照与二进制哈希检查不等于完成第三方许可证审计。
