# Memory Management Rules

## Format for MEMORY.md

Use priority tags with dates:
- `[P0]` — permanent (identity, preferences)
- `[P1][YYYY-MM-DD]` — 90-day TTL (projects)
- `[P2][YYYY-MM-DD]` — 30-day TTL (temporary)

## Size Limits

- MEMORY.md: ≤200 lines
- Core principles: ≤5 rules
- Everything else: searchable archives

## Weekly Maintenance

1. Archive P2 older than 30 days
2. Archive P1 older than 90 days  
3. Extract lessons from daily logs
4. Never delete P0

## Lesson Storage

Use `memory/lessons/*.jsonl`:
```json
{"date": "...", "title": "...", "problem": "...", "solution": "...", "tags": [...]}
```

Search lessons before repeating mistakes.
