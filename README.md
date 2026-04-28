# gitlab-mcp

A GitLab MCP (Model Context Protocol) server that exposes GitLab functionality as tools for Claude.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Setup

1. Clone the repo and install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root:
   ```env
   GITLAB_TOKEN=your-personal-access-token
   GITLAB_URL=https://gitlab.com
   ```

## Usage with Claude Code

Add the following to your Claude Code MCP settings (`~/.claude/settings.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "gitlab-mcp": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/gitlab_mcp"
    }
  }
}
```

Claude Code will automatically start the server and make its tools available.

## Development

Run locally to test:
```bash
uv run python main.py
```
