# gitlab-mcp

A custom Python MCP server that exposes GitLab functionality as tools for Claude Code.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Setup

1. Clone the repo:
   ```bash
   git clone https://gitlab.dev.dyl.com/ai/gitlab-mcp.git
   cd gitlab-mcp
   git checkout dev
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root:
   ```env
   GITLAB_PROXY_URL=https://gitlab.your-proxy.com
   GITLAB_PROXY_TOKEN=your-proxy-personal-access-token
   GITLAB_CLIENT_URL=https://gitlab.your-client.com
   GITLAB_CLIENT_TOKEN=your-client-personal-access-token
   ```
   See `.env.example` for the full list of required variables.

## Register with Claude Code

### Local setup (your own machine)

Run this command from your working directory, replacing the path with your local clone location:

```bash
claude mcp add gitlab-mcp \
  --transport stdio \
  --scope user \
  -- uv run --directory /path/to/gitlab-mcp python main.py
```

> **Note:** If Claude Code can't find `uv`, replace `uv` with its full path (`which uv`).

Credentials are read from the `.env` file in the project root. Environment variables set in the MCP config take precedence over `.env`.

> **Important:** MCP servers load once at session start. After any config or code change, restart Claude Code fully.

### Coworker setup (via git, no local clone needed)

Coworkers with access to the repo can run the server directly without cloning. Run this command, replacing the values with your actual credentials:

```bash
claude mcp add gitlab-mcp \
  --transport stdio \
  --scope user \
  -e GITLAB_PROXY_URL=https://your-proxy-gitlab.com \
  -e GITLAB_PROXY_TOKEN=your-proxy-token \
  -e GITLAB_CLIENT_URL=https://your-client-gitlab.com \
  -e GITLAB_CLIENT_TOKEN=your-client-token \
  -- uvx --from git+https://gitlab.dev.dyl.com/ai/gitlab-mcp.git@dev gitlab-mcp
```

`--scope user` registers the server globally in `~/.claude.json` so it loads in every project.

See `.env.example` for all required variables.

To get the latest changes after an update:
```bash
uv tool upgrade gitlab-mcp
```

## Verify Before Restarting Claude

Send the full MCP handshake manually to confirm the server responds with clean JSON:

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}\n{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n' \
  | uv run --directory /path/to/gitlab-mcp python main.py 2>/dev/null
```

You should see two clean JSON responses — one for `initialize`, one listing all tools. If you see plain text or nothing, there is a startup error.

Also check startup time — should be under ~1s:
```bash
time echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  | uv run --directory /path/to/gitlab-mcp python main.py 2>/dev/null
```

## Available Tools

| Tool | Description |
|---|---|
| `get_project_definitions` | Returns all configured GitLab projects with their IDs and instance names. Call this first to get `project_id` and `gl_name` before using other tools. |
| `search_code` | Searches source code across a project and returns matching file snippets. |
| `get_file` | Returns the full content of a file at a given path and branch ref. |
| `find_mr` | Finds merge requests by title and returns their iid, title, and state. |
| `get_mr_diff` | Returns file diffs for a given merge request. |

Both GitLab instances (`proxy` and `client`) are supported. `get_project_definitions` tells you which `gl_name` to use for each project.

## Config File Locations (Claude Code)

| File | Scope |
|---|---|
| `~/.claude.json` → `mcpServers` (top-level) | Global, every session — written by `--scope user` |
| `~/.claude.json` → `projects['/path'].mcpServers` | Per working directory only |
| `.mcp.json` in project root | Local project only |

> **Note:** `~/.claude/settings.json` has an `mcpServers` key but it is not loaded by Claude Code — use `claude mcp add --scope user` instead.
