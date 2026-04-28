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

## Usage with Claude Code

Add the following to your Claude Code MCP settings (`~/.claude/settings.json` or project `.claude/settings.json`), replacing the values with your own GitLab URLs and personal access tokens:

```json
{
  "mcpServers": {
    "gitlab-mcp": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/gitlab_mcp",
      "env": {
        "GITLAB_PROXY_URL": "https://gitlab.your-proxy.com",
        "GITLAB_PROXY_TOKEN": "your-proxy-personal-access-token",
        "GITLAB_CLIENT_URL": "https://gitlab.your-client.com",
        "GITLAB_CLIENT_TOKEN": "your-client-personal-access-token"
      }
    }
  }
}
```

Claude Code will automatically start the server and make its tools available.

## Local Development

Create a `.env` file in the project root and run:
```env
GITLAB_PROXY_URL=https://gitlab.your-proxy.com
GITLAB_PROXY_TOKEN=your-proxy-personal-access-token
GITLAB_CLIENT_URL=https://gitlab.your-client.com
GITLAB_CLIENT_TOKEN=your-client-personal-access-token
```
```bash
uv run python main.py
```

## Development

Run locally to test:
```bash
uv run python main.py
```
