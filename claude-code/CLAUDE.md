# Memory Management for Claude Code

## Memory Structure

Use a three-layer memory system to manage context efficiently.

### Layer 1: Hot Memory (always in context)

Keep a `MEMORY.md` file ≤200 lines with priority tags:

```markdown
## Core [P0]
- [P0] User timezone: US Eastern
- [P0] Prefers direct communication

## Active Projects [P1]
- [P1][2026-02-10] Project A - current focus
- [P1][2026-02-05] Project B - ongoing

## Temporary [P2]
- [P2][2026-02-08] Debug note - cron timezone issue
```

**Priority levels:**
- **P0** — Core identity, never delete
- **P1** — Active projects, review after 90 days
- **P2** — Temporary notes, archive after 30 days

### Layer 2: Cold Memory (searchable)

Store detailed lessons in `memory/lessons/` as JSONL:

```json
{"date": "2026-02-10", "category": "api", "title": "Auth issue", "problem": "Token expired silently", "solution": "Add refresh logic", "tags": ["auth"]}
```

Archive expired content to `memory/archive/`.

### Layer 3: Raw Logs

Daily notes in `memory/YYYY-MM-DD.md` — reference only, not loaded.

## Rules (keep ≤5 in main config)

1. Real money operations: correctness > speed
2. External actions (email/post): confirm first
3. Check both automation systems when disabling
4. Long processes need proper isolation
5. New platforms: read rules before acting

Other lessons → `lessons/*.jsonl`, search when needed.

## Maintenance

Weekly: review MEMORY.md, archive expired P1/P2, extract lessons from daily logs.

If MEMORY.md exceeds 200 lines, prioritize:
1. Keep all P0
2. Keep recent P1 (last 90 days)
3. Archive old P2 and P1
4. Move specifics to lessons/
