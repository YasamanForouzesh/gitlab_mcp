
import os
import gitlab
import json

_instances = {
    "proxy": gitlab.Gitlab(
        url=os.getenv("GITLAB_PROXY_URL", ""), 
        private_token=os.getenv("GITLAB_PROXY_TOKEN", "")),
    "client": gitlab.Gitlab(
        url=os.getenv("GITLAB_CLIENT_URL", ""),
        private_token=os.getenv("GITLAB_CLIENT_TOKEN", ""),
    ),
}


for _name, _gl_instance in _instances.items():
    try:
        _gl_instance.auth()
        print(f"[gitlab] connected: {_name} ({_gl_instance.url})")
    except Exception as e:
        print(f"[gitlab] failed to connect: {_name} ({_gl_instance.url}) — {e}")


def _gl(name: str) -> gitlab.Gitlab:
    if name not in _instances:
        raise ValueError(f"Unknown GitLab instance name: {name}")
    return _instances[name]


def _clean_results(results: list) -> list:
    grouped = {}
    for r in results:
        path = r["path"]
        snippet = r["data"].strip()
        if path in grouped:
            grouped[path].append(snippet)
        else:
            grouped[path] = [snippet]
    return [
        {"filename": path, "data": "\n...\n".join(snippets)}
        for path, snippets in grouped.items()
    ]


def handle_search_code(gl_name: str, query: str, project_id: int):
    gl = _gl(gl_name)
    search_kwargs = {"scope": "blobs", "search": query, "get_all": True}
    target = gl.projects.get(project_id)
    results = target.search(**search_kwargs)
    return _clean_results(results)
    
def handle_get_file(gl_name: str, project_id: int, file_path: str, ref: str = "dev"):
    gl = _gl(gl_name)
    project = gl.projects.get(project_id)
    file = project.files.get(file_path, ref=ref)
    return file.decode().decode("utf-8")


def handle_find_mr(gl_name: str, project_id: int, title: str):
    project = _gl(gl_name).projects.get(project_id)
    mrs = project.mergerequests.list(search=title, state="all")
    return [{"iid": mr.iid, "title": mr.title, "state": mr.state} for mr in mrs]


def handle_get_mr_diff(gl_name: str, project_id: int, mr_iid: int):
    project = _gl(gl_name).projects.get(project_id)
    mr = project.mergerequests.get(mr_iid)
    diffs = mr.diffs.list()
    result = []
    for diff in diffs:
        for change in diff.diffs:
            result.append({
                "filename": change["new_path"],
                "diff": change["diff"],
            })
    return result

def load_project_definitions(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

