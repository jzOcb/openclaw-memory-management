## 🔴 Core Principles (5 Rules Only)

These are the only Iron Rules. Everything else is in `memory/lessons/*.jsonl` (searchable).

1. **真钱 = 正确性 > 速度** — 涉及交易/支付时，用完全相同的已测试代码，更多检查不是更少
2. **外部操作先问** — 发邮件、发推、公开发帖前必须确认
3. **自动化两套系统** — 禁用/检查自动化时，查 system crontab + OpenClaw cron
4. **进程隔离** — 长期运行的bot用 `setsid + managed-process.sh`，否则会被session cleanup杀掉
5. **平台规则优先** — 新交易/新平台，先读结算规则，验证数据源

*所有具体教训在 `memory/lessons/` 里，用 `memory_search` 召回。*
