# Session Bar

A Claude Code status line that keeps the **session name** in view, so you can recognise a session the moment you switch to its terminal tab — even when you have many tabs open and the tab titles are truncated.

```
✳ Refactor billing API  kaggle-competition
Sonnet 5.5 · ctx ████░░░░░░ 49% · $1.23 · 5h 72% · 7d 90%
```

- **Line 1**: session name (bold cyan) and project directory (dim).
- **Line 2**: model · context bar (green < 60%, yellow < 85%, red above) · cost · 5-hour / 7-day rate limits.
- Session name comes from `/rename`, falling back to the AI-generated title in the transcript, then to the short session id.
- Pure Python 3 standard library, no dependencies. Bad or empty input never crashes it; it degrades to shorter output.

## Install

```
claude plugin marketplace add hecool108/claude-session-bar
claude plugin install session-bar@session-bar-marketplace
```

Then, inside Claude Code, run this **once**:

```
/session-bar:setup
```

Plugins are not allowed to enable a status line themselves, so this command does it for you: it copies the script to `~/.claude/session-bar/session-bar.py` and writes the `statusLine` entry into your `~/.claude/settings.json` (it asks before replacing an existing one). The script is copied to a stable path so the status line keeps working when the plugin's own directory changes on update. The bar appears at the next refresh — send any message.

**After updating the plugin, run `/session-bar:setup` again** to refresh the copied script.

## Notes

- The 5h / 7d rate-limit figures are only reported for Pro/Max subscribers; they are hidden otherwise.
- After `/rename`, the bar may not change until the next refresh. Send a message or wait for the 30 s refresh interval.
- Requires `python3` on your `PATH` (macOS ships one with the Xcode Command Line Tools). On Windows, install Python 3 and make sure `python3` resolves.

## Uninstall

Remove the `statusLine` key from `~/.claude/settings.json`, delete `~/.claude/session-bar/`, then:

```
claude plugin uninstall session-bar@session-bar-marketplace
```

## License

MIT
