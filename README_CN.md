# OpenClaw Memory Management System

[English](README.md)


AI Agent 记忆越多反而越蠢？这套系统帮你管理 OpenClaw 记忆，Token 降 78%。

基于 [@ohxiyu](https://x.com/ohxiyu) 的 P0/P1/P2 方案落地实现。

## 效果

```
Before（优化前）          After（优化后）
├── 行数：427 行          ├── 行数：96 行  (-77%)
├── Tokens：6,618         ├── Tokens：1,488  (-78%)
├── 维护：手动            ├── 维护：自动 cron
├── Iron Rules：17 条散落  ├── Iron Rules：5 条集中
└── 教训召回：全文扫描     └── 教训召回：语义搜索
```

## 三层记忆架构

```
MEMORY.md (热记忆)         ← 每次加载，≤200 行
├── [P0] 核心身份          ← 永不过期
├── [P1][date] 活跃项目    ← 90天TTL
└── [P2][date] 临时        ← 30天TTL

memory/lessons/*.jsonl    ← 结构化教训，语义搜索召回
memory/archive/           ← 过期内容，可搜索不加载
memory/YYYY-MM-DD.md      ← 每日原始日志
```

## 快速开始

### 1. 复制模板文件

```bash
cp templates/MEMORY.md ~/.openclaw/workspace/MEMORY.md
cp scripts/memory-janitor.py ~/.openclaw/workspace/scripts/
mkdir -p ~/.openclaw/workspace/memory/{archive,lessons}
```

### 2. 设置自动归档 cron

```bash
# 每天 4 AM UTC 自动归档
(crontab -l 2>/dev/null; echo "0 4 * * * python3 ~/.openclaw/workspace/scripts/memory-janitor.py >> ~/.openclaw/workspace/logs/memory-janitor.log 2>&1") | crontab -
```

### 3. 手动运行测试

```bash
# 预览模式（不修改文件）
python3 scripts/memory-janitor.py --dry-run

# 查看统计
python3 scripts/memory-janitor.py --stats

# 执行归档
python3 scripts/memory-janitor.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/memory-janitor.py` | 自动归档脚本，P2>30天/P1>90天 → archive |
| `templates/MEMORY.md` | 热记忆模板，带 P0/P1/P2 格式示例 |
| `templates/AGENTS-rules.md` | 5 条核心原则示例 |
| `templates/lessons.jsonl` | 结构化教训格式示例 |

## P0/P1/P2 优先级说明

每条记忆格式：`- [P优先级][日期] 内容`

- **P0** — 核心身份，永不过期。例：用户偏好、安全红线
- **P1** — 活跃项目，90 天过期。例：当前项目、近期策略
- **P2** — 临时内容，30 天过期。例：调试记录、一次性事件

```markdown
- [P0] 用户偏好中文回复
- [P1][2026-02-07] TaxForge v1.4.0 发布
- [P2][2026-02-05] 调试了 cron 时区问题
```

## 核心原则（推荐放 AGENTS.md）

只保留 5 条，其他教训存 `lessons/*.jsonl` 用语义搜索召回：

1. **真钱 = 正确性 > 速度** — 涉及交易/支付时，用完全相同的已测试代码
2. **外部操作先问** — 发邮件、发推、公开发帖前必须确认
3. **自动化两套系统** — 禁用/检查自动化时，查 system crontab + OpenClaw cron
4. **进程隔离** — 长期运行的 bot 用 setsid，否则会被 session cleanup 杀掉
5. **平台规则优先** — 新交易/新平台，先读结算规则

## 致谢

- [@ohxiyu](https://x.com/ohxiyu) — P0/P1/P2 优先级方案原创
- [OpenClaw](https://github.com/openclaw/openclaw) — AI Agent 平台

## License

MIT

## Skills / Integration

### OpenClaw Skill

Copy to your skills directory:
```bash
cp -r skills/memory-management ~/.openclaw/skills/
# or
cp -r skills/memory-management ~/clawd/skills/
```

### Claude Code

**Option 1:** Add CLAUDE.md to your project root:
```bash
cp claude-code/CLAUDE.md ~/your-project/CLAUDE.md
```

**Option 2:** Add as a rule:
```bash
mkdir -p ~/your-project/.claude/rules
cp claude-code/.claude/rules/memory-management.md ~/your-project/.claude/rules/
```

