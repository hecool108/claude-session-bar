#!/usr/bin/env python3
"""Claude Code status line: make the session name impossible to miss.

Reads the status-line JSON on stdin and prints two rows:
  row 1: ✳ <session name>  ·  <project dir>
  row 2: <model> · ctx <bar> NN% · $cost · 5h NN% · 7d NN%
Never raises: any failure degrades to a shorter line.
"""
import json
import os
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"


def title_from_transcript(path):
    """Fallback: last ai-title entry in the transcript."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 400_000))
            tail = f.read().decode("utf-8", "ignore")
    except OSError:
        return None
    name = None
    for line in tail.splitlines():
        if '"ai-title"' not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        name = e.get("aiTitle") or name
    return name


def color_for(pct):
    return GREEN if pct < 60 else YELLOW if pct < 85 else RED


def main():
    try:
        d = json.load(sys.stdin)
    except ValueError:
        d = {}

    cwd = d.get("cwd") or (d.get("workspace") or {}).get("current_dir") or ""
    proj = os.path.basename(cwd.rstrip("/")) or "~"
    name = d.get("session_name") or title_from_transcript(d.get("transcript_path") or "")
    sid = (d.get("session_id") or "")[:8]

    head = f"{BOLD}{CYAN}✳ {name or '(unnamed session)'}{RESET}"
    tail = f"{DIM}{proj}" + (f" · {sid}" if not name and sid else "") + RESET
    print(f"{head}  {tail}")

    parts = []
    model = (d.get("model") or {}).get("display_name")
    if model:
        parts.append(model)

    pct = (d.get("context_window") or {}).get("used_percentage")
    if isinstance(pct, (int, float)):
        filled = min(10, int(pct / 10))
        bar = "█" * filled + "░" * (10 - filled)
        parts.append(f"ctx {color_for(pct)}{bar} {pct:.0f}%{RESET}")

    cost = (d.get("cost") or {}).get("total_cost_usd")
    if isinstance(cost, (int, float)):
        parts.append(f"${cost:.2f}")

    rl = d.get("rate_limits") or {}
    for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
        p = (rl.get(key) or {}).get("used_percentage")
        if isinstance(p, (int, float)):
            parts.append(f"{label} {color_for(p)}{p:.0f}%{RESET}")

    if parts:
        print(" · ".join(parts))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
