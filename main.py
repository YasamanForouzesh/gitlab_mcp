import json
from dotenv import load_dotenv

load_dotenv(override=True)

from mcp.server.fastmcp import FastMCP
from gitlab_tools import handle_search_code, handle_get_file, handle_find_mr, handle_get_mr_diff, load_project_definitions

mcp = FastMCP("gitlab-mcp")

path = "config/project_definitions.json"

with open(path, "r", encoding="utf-8") as f:
    _PROJECTS = json.load(f)

project_id = _PROJECTS[6]["project_id"]


# @mcp.tool()
# def get_project_definitions() -> list:
#     """Get all GitLab projects with their ids, source instances, and keywords. Call this first to identify which project_id and gl_name to use before searching."""
#     return load_project_definitions("config/project_definitions.json")


# @mcp.tool()
# def search_code(gl_name: str, query: str, project_id: int) -> list:
#     """Search for code across a GitLab project and return matching file snippets."""
#     return handle_search_code(gl_name, query, project_id)


# @mcp.tool()
# def get_file(gl_name: str, project_id: int, file_path: str, ref: str = "dev") -> str:
#     """Get the full content of a file from a GitLab project."""
#     return handle_get_file(gl_name, project_id, file_path, ref)


# @mcp.tool()
# def find_mr(gl_name: str, project_id: int, title: str) -> list:
#     """Find merge requests by title and return their iid, title, and state."""
#     return handle_find_mr(gl_name, project_id, title)


# @mcp.tool()
# def get_mr_diff(gl_name: str, project_id: int, mr_iid: int) -> list:
#     """Get the file changes and diffs for a merge request."""
#     return handle_get_mr_diff(gl_name, project_id, mr_iid)


def main():
    print(project_id, type(project_id))
    result = handle_search_code("client", "createUser", 4)
    print(json.dumps(result, indent=2))
    file_path = result[0]["filename"]
    data = handle_get_file("client", 4, file_path)
    print(data)

if __name__ == "__main__":
    main()
    mcp.run(transport='stdio')
