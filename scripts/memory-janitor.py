#!/usr/bin/env python3
"""
Memory Janitor - Auto-archive expired memories

Based on @ohxiyu's memory management system:
- P0: Core identity, never expire
- P1: Active projects, 90-day TTL
- P2: Temporary, 30-day TTL

Usage:
  python3 memory-janitor.py              # Run archival
  python3 memory-janitor.py --dry-run    # Preview only
  python3 memory-janitor.py --stats      # Show statistics

Changelog:
  v2 (2026-02-10): Added atomic write, MAX_LINES warning, dedup archive, line-start regex
"""

import re
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
ARCHIVE_DIR = WORKSPACE / "memory/archive"
MAX_LINES = 200
P1_TTL_DAYS = 90
P2_TTL_DAYS = 30

# Pattern: Lines starting with "- [P0]" or "- [P1][2026-02-10]" etc.
# Must be at line start (after optional whitespace) to avoid matching inline references
PRIORITY_PATTERN = re.compile(r'^\s*-\s*\[P([012])\](?:\[(\d{4}-\d{2}-\d{2})\])?')

def parse_line(line):
    """Extract priority and date from a line. Only matches bullet points at line start."""
    match = PRIORITY_PATTERN.match(line)
    if match:
        priority = int(match.group(1))
        date_str = match.group(2)
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                date = None
        else:
            date = None
        return priority, date
    return None, None

def should_archive(priority, date, today):
    """Determine if a line should be archived based on priority and age."""
    if priority == 0:
        return False  # P0 never expires
    if date is None:
        return False  # No date = keep (can't determine age)
    
    age_days = (today - date).days
    
    if priority == 2 and age_days > P2_TTL_DAYS:
        return True
    if priority == 1 and age_days > P1_TTL_DAYS:
        return True
    
    return False

def atomic_write(path: Path, content: str):
    """Write content to file atomically using temp file + rename."""
    # Create temp file in same directory (required for atomic rename)
    fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix='.janitor-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        os.replace(temp_path, path)  # Atomic on POSIX
    except:
        # Clean up temp file on failure
        try:
            os.unlink(temp_path)
        except:
            pass
        raise

def load_existing_archive(archive_file: Path) -> set:
    """Load existing archived lines to prevent duplicates."""
    if not archive_file.exists():
        return set()
    return set(archive_file.read_text().splitlines())

def run_janitor(dry_run=False, stats_only=False):
    """Main janitor logic."""
    if not MEMORY_FILE.exists():
        print(f"❌ Memory file not found: {MEMORY_FILE}")
        return 1
    
    today = datetime.now().date()
    lines = MEMORY_FILE.read_text().splitlines()
    
    # Statistics
    counts = {0: 0, 1: 0, 2: 0, None: 0}
    to_archive = []
    to_keep = []
    
    for line in lines:
        priority, date = parse_line(line)
        
        if priority is not None:
            counts[priority] += 1
        else:
            counts[None] += 1
        
        if should_archive(priority, date, today):
            to_archive.append(line)
        else:
            to_keep.append(line)
    
    # Stats output
    print("📊 Memory Statistics:")
    print(f"  Total lines: {len(lines)}")
    print(f"  P0 (permanent): {counts[0]}")
    print(f"  P1 (90-day): {counts[1]}")
    print(f"  P2 (30-day): {counts[2]}")
    print(f"  Untagged: {counts[None]}")
    print(f"  To archive: {len(to_archive)}")
    print(f"  To keep: {len(to_keep)}")
    
    # MAX_LINES warning
    if len(to_keep) > MAX_LINES:
        print(f"\n⚠️  WARNING: {len(to_keep)} lines exceeds MAX_LINES ({MAX_LINES})")
        print(f"    Consider reviewing P0 entries or converting some to P1/P2")
    
    if stats_only:
        return 0
    
    if not to_archive:
        print("✅ Nothing to archive")
        return 0
    
    # Show what will be archived
    print(f"\n📦 Will archive {len(to_archive)} lines:")
    for line in to_archive[:10]:
        print(f"  - {line[:60]}...")
    if len(to_archive) > 10:
        print(f"  ... and {len(to_archive) - 10} more")
    
    if dry_run:
        print("\n🔍 DRY RUN - no changes made")
        return 0
    
    # Perform archival
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_file = ARCHIVE_DIR / f"auto-{today.isoformat()}.md"
    
    # Load existing archive to prevent duplicates
    existing = load_existing_archive(archive_file)
    new_to_archive = [line for line in to_archive if line not in existing]
    
    if new_to_archive:
        # Build archive content (full file, not append)
        archive_header = f"# Auto-archived {today.isoformat()}\n\n"
        all_archived = list(existing) + new_to_archive
        # Filter out header lines from previous runs
        content_lines = [l for l in all_archived if not l.startswith("# Auto-archived")]
        archive_content = archive_header + "\n".join(content_lines) + "\n"
        
        atomic_write(archive_file, archive_content)
        print(f"\n✅ Archived {len(new_to_archive)} new lines to {archive_file}")
        if len(to_archive) > len(new_to_archive):
            print(f"   ({len(to_archive) - len(new_to_archive)} were already archived)")
    else:
        print(f"\n✅ All {len(to_archive)} lines already in archive, skipping")
    
    # Write back kept lines (atomic)
    kept_content = "\n".join(to_keep) + "\n"
    atomic_write(MEMORY_FILE, kept_content)
    
    print(f"✅ Memory file now has {len(to_keep)} lines")
    
    return 0

def main():
    args = sys.argv[1:]
    
    dry_run = "--dry-run" in args
    stats_only = "--stats" in args
    
    return run_janitor(dry_run=dry_run, stats_only=stats_only)

if __name__ == "__main__":
    sys.exit(main())
