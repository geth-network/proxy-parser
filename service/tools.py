import importlib
from datetime import datetime

from settings.dev import settings


def collect_tasks():
    module = importlib.import_module(settings.tasks_module)
    tasks = []
    for name in list(module.__dict__):
        elem = getattr(module, name)
        if hasattr(elem, "is_task") and elem.is_task:
            tasks.append(elem())
    found_tasks_log = f"Found tasks in [{settings.tasks_module}]:\n"
    for task in tasks:
        found_tasks_log += f"  |- {task.__qualname__}\n"
    print(f"[{datetime.now()}] {found_tasks_log}")
    return tasks
