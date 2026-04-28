import json
from dotenv import load_dotenv

load_dotenv(override=True)

from mcp.server.fastmcp import FastMCP
from gitlab_tools import handle_search_code

mcp = FastMCP("gitlab-mcp")

path = "config/project_definitions.json"

with open(path, "r", encoding="utf-8") as f:
    _PROJECTS = json.load(f)

project_id = _PROJECTS[6]["project_id"]


def main():
    print(project_id, type(project_id))
    handle_search_code("proxy", "create product", project_id)


if __name__ == "__main__":
    main()
    mcp.run(transport='stdio')
