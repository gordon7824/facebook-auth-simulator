# Facebook iOS 注册/登录链路模拟器

> 仅用于离线研究、抓包数据解析和本地状态机测试，不连接 Facebook 生产接口，不实现账号注册、登录自动化、令牌复用或绕过 App Attestation / Integrity / 风控机制。

## 项目目标

使用 Python 对脱敏的 `fb_traffic.jsonl` 进行：

- 请求顺序和 `friendly_name` 统计
- CAA 注册状态机的离线重建
- `server_params.reg_info` 字段累积分析
- 登录与 DBL 会话事件建模
- RSA 公钥格式和加密流程的本地单元测试（使用测试密钥）
- 敏感字段脱敏和安全日志输出

## 安全边界

本项目不会：

- 调用 Facebook 私有接口或生产端点
- 自动创建/登录真实账号
- 处理真实密码、OAuth token、nonce、APNs token 或 App Attestation 凭据
- 绕过设备完整性、checkpoint、会话风控或服务条款限制

请仅使用自己拥有或明确获授权的、已脱敏的抓包数据，并遵守适用法律、隐私政策和 Facebook 服务条款。

## 建议结构

```text
facebook-auth-simulator/
├── src/fb_simulator/
│   ├── models.py          # 脱敏事件与状态模型
│   ├── parser.py          # JSONL 离线解析器
│   ├── state_machine.py   # 本地 CAA 状态机
│   ├── redaction.py       # 敏感字段脱敏
│   └── reports.py         # 顺序和字段报告
├── tests/
├── examples/
├── requirements.txt
└── README.md
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# 对脱敏抓包做离线分析
python -m fb_simulator.parser ./data/fb_traffic.redacted.jsonl

# 运行测试
pytest -q
```

## 数据要求

输入文件必须是 JSONL，并且应先删除或替换以下字段：密码、Cookie、OAuth token、nonce、手机号、设备标识、用户 ID、App Attestation 数据和任何可重放凭据。

示例事件：

```json
{"timestamp":"2026-09-30T13:09:02Z","friendly_name":"caa.reg.welcome","current_step":null,"server_params":{"reg_info":{"first_name":"<redacted>"}}}
```

## 说明

`pwd_key_fetch` 的 RSA 公钥格式可以在本地测试中建模，但本项目不提供向真实服务提交加密密码的代码。真实应用应优先使用 Facebook 官方 SDK/Graph API 及其公开授权流程。

## 许可证

MIT License
