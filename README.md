# OpenClaw Memory Management System

[中文版](README_CN.md)

Does your AI Agent get dumber as it remembers more? This system helps you manage OpenClaw memory efficiently, reducing token usage by 78%.

Based on [@ohxiyu](https://x.com/ohxiyu)'s P0/P1/P2 priority system.

## Results

```
Before                        After
├── Lines: 427                ├── Lines: 96  (-77%)
├── Tokens: 6,618             ├── Tokens: 1,488  (-78%)
├── Maintenance: Manual       ├── Maintenance: Auto cron
├── Iron Rules: 17 scattered  ├── Iron Rules: 5 centralized
└── Lesson recall: Full scan  └── Lesson recall: Semantic search
```

## Three-Layer Memory Architecture

```
MEMORY.md (Hot Memory)        ← Loaded every session, ≤200 lines
├── [P0] Core identity        ← Never expires
├── [P1][date] Active project ← 90-day TTL
└── [P2][date] Temporary      ← 30-day TTL

memory/lessons/*.jsonl        ← Structured lessons, semantic search
memory/archive/               ← Expired content, searchable but not loaded
memory/YYYY-MM-DD.md          ← Daily raw logs
```

## Quick Start

### 1. Copy template files

```bash
cp templates/MEMORY.md ~/.openclaw/workspace/MEMORY.md
cp scripts/memory-janitor.py ~/.openclaw/workspace/scripts/
mkdir -p ~/.openclaw/workspace/memory/{archive,lessons}
```

### 2. Set up auto-archive cron

```bash
# Daily at 4 AM UTC
(crontab -l 2>/dev/null; echo "0 4 * * * python3 ~/.openclaw/workspace/scripts/memory-janitor.py >> ~/.openclaw/workspace/logs/memory-janitor.log 2>&1") | crontab -
```

### 3. Test manually

```bash
# Preview mode (no changes)
python3 scripts/memory-janitor.py --dry-run

# Show statistics
python3 scripts/memory-janitor.py --stats

# Run archival
python3 scripts/memory-janitor.py
```

## Files

| File | Description |
|------|-------------|
| `scripts/memory-janitor.py` | Auto-archive script, P2>30d/P1>90d → archive |
| `templates/MEMORY.md` | Hot memory template with P0/P1/P2 format |
| `templates/AGENTS-rules.md` | 5 core principles example |
| `templates/lessons.jsonl` | Structured lesson format |

## P0/P1/P2 Priority System

Format: `- [Priority][Date] Content`

- **P0** — Core identity, never expires. e.g., user preferences, safety rules
- **P1** — Active projects, 90-day TTL. e.g., current projects, recent strategies
- **P2** — Temporary, 30-day TTL. e.g., debug notes, one-time events

```markdown
- [P0] User prefers Chinese responses
- [P1][2026-02-07] TaxForge v1.4.0 released
- [P2][2026-02-05] Debugged cron timezone issue
```

## Core Principles (for AGENTS.md)

Keep only 5 rules. Store other lessons in `lessons/*.jsonl` for semantic search:

1. **Real money = correctness > speed** — Use identical tested code for transactions
2. **Confirm before external actions** — Ask before sending emails, tweets, public posts
3. **Two automation systems** — Check both system crontab + OpenClaw cron
4. **Process isolation** — Long-running bots need setsid, or they get killed by session cleanup
5. **Platform rules first** — Read settlement rules before trading on new platforms

## Skills / Integration

### OpenClaw Skill

```bash
cp -r skills/memory-management ~/.openclaw/skills/
# or
cp -r skills/memory-management ~/clawd/skills/
```

### Claude Code

**Option 1:** Add CLAUDE.md to project root:
```bash
cp claude-code/CLAUDE.md ~/your-project/CLAUDE.md
```

**Option 2:** Add as a rule:
```bash
mkdir -p ~/your-project/.claude/rules
cp claude-code/.claude/rules/memory-management.md ~/your-project/.claude/rules/
```

## Credits

- [@ohxiyu](https://x.com/ohxiyu) — Original P0/P1/P2 priority system
- [OpenClaw](https://github.com/openclaw/openclaw) — AI Agent platform

## License

MIT
