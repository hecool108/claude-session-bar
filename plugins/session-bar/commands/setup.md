---
description: Enable (or update) the Session Bar status line in your user settings
---

Enable the Session Bar status line for the user. The script is copied to a stable location first, because the plugin's own directory changes with every plugin version and a path into it would break after an update.

1. The bundled script is `${CLAUDE_PLUGIN_ROOT}/bin/session-bar.py`. Copy it to `~/.claude/session-bar/session-bar.py` (create the directory if needed, overwrite an existing copy). Resolve `~` to an absolute path.
2. Read `~/.claude/settings.json`. If a `statusLine` entry already exists and its command does not already point at `~/.claude/session-bar/session-bar.py`, show it to the user and ask before replacing it. If it already points there, skip to step 4.
3. Otherwise merge this into the file, keeping every other key untouched:

```json
"statusLine": {
  "type": "command",
  "command": "python3 <absolute path of the copied script>",
  "refreshInterval": 30
}
```

4. Tell the user:
   - it takes effect on the next status-line refresh (send any message);
   - the plugin cannot enable this itself, because plugins are not allowed to set `statusLine`;
   - after updating the plugin, run `/session-bar:setup` again to refresh the copied script.
