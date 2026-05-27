import os
from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP
from gitlab_tools import handle_search_code, handle_get_file, handle_find_mr, handle_get_mr_diff, load_project_definitions

mcp = FastMCP("gitlab-mcp")


@mcp.tool()
def get_project_definitions() -> list:
    """Get all GitLab projects with their ids, source instances, and keywords. Call this first to identify which project_id and gl_name to use before searching."""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/project_definitions.json")
    return load_project_definitions(config_path)


@mcp.tool()
def search_code(gl_name: str, query: str, project_id: int) -> list:
    """Search for code across a GitLab project and return matching file snippets.

    Args:
        gl_name: GitLab instance to use — either 'proxy' or 'client', as returned by get_project_definitions.
        query: The search string to look for in source code. Use camelCase for client/frontend projects and snake_case for backend projects.
        project_id: The numeric GitLab project ID, as returned by get_project_definitions.
    """
    return handle_search_code(gl_name, query, project_id)


@mcp.tool()
def get_file(gl_name: str, project_id: int, file_path: str, ref: str = "dev") -> str:
    """Get the full content of a file from a GitLab project.

    Args:
        gl_name: GitLab instance to use — either 'proxy' or 'client', as returned by get_project_definitions.
        project_id: The numeric GitLab project ID, as returned by get_project_definitions.
        file_path: Full path to the file within the repository (e.g. 'src/api/leads.py').
        ref: Branch or commit ref to read the file from. Defaults to 'dev'.
    """
    return handle_get_file(gl_name, project_id, file_path, ref)


@mcp.tool()
def find_mr(gl_name: str, project_id: int, title: str) -> list:
    """Find merge requests by title and return their iid, title, and state.

    Args:
        gl_name: GitLab instance to use — either 'proxy' or 'client', as returned by get_project_definitions.
        project_id: The numeric GitLab project ID, as returned by get_project_definitions.
        title: Partial or full MR title to search for.
    """
    return handle_find_mr(gl_name, project_id, title)


@mcp.tool()
def get_mr_diff(gl_name: str, project_id: int, mr_iid: int) -> list:
    """Get the file changes and diffs for a merge request.

    Args:
        gl_name: GitLab instance to use — either 'proxy' or 'client', as returned by get_project_definitions.
        project_id: The numeric GitLab project ID, as returned by get_project_definitions.
        mr_iid: The internal ID (iid) of the merge request, as returned by find_mr.
    """
    return handle_get_mr_diff(gl_name, project_id, mr_iid)


def run():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    run()
