#!/usr/bin/env python3
"""Read-only: list CLAIMS.md rows still in prepped (Pass A crib → need Pass B).

Does not claim, edit, or lock anything in the translations checkout.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_CLAIMS = Path.home() / "SaneApps/clients/translations/docs/CLAIMS.md"
ROW = re.compile(
    r"^\|\s*(?P<id>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*(?P<rest>.*)\|\s*$"
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--claims",
        type=Path,
        default=DEFAULT_CLAIMS,
        help="Path to CLAIMS.md (read-only)",
    )
    ap.add_argument(
        "--status",
        default="prepped",
        help="Status to list (default: prepped)",
    )
    args = ap.parse_args()
    path: Path = args.claims
    if not path.is_file():
        print(f"BLOCKED: claims file missing: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        status = m.group("status").strip()
        if status != args.status:
            continue
        cid = m.group("id").strip()
        if cid in {"id", "---"} or cid.startswith("-"):
            continue
        rest = m.group("rest").strip()
        rows.append((cid, status, rest))
    print(f"# {args.status} claims needing next human/AI Pass B step")
    print(f"# source: {path}")
    print(f"# count: {len(rows)}")
    print()
    if not rows:
        print("(none)")
        return 0
    for cid, status, rest in rows:
        # rest typically: book | slice | owner | date | branch | note
        parts = [p.strip() for p in rest.split("|")]
        slice_ = parts[1] if len(parts) > 1 else rest
        note = parts[-1] if parts else ""
        print(f"- {cid}: {slice_} — {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
