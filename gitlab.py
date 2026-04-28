
import os
import gitlab

_instances = {
    "proxy": gitlab.Gitlab(
        os.getenv("GITLAB_PROXY_URL", ""),
        private_token=os.getenv("GITLAB_PROXY_TOKEN", ""),
    ),
    "client": gitlab.Gitlab(
        os.getenv("GITLAB_CLIENT_URL", ""),
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