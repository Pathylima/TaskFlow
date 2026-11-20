"""Aplicação web TaskFlow para gerenciamento simples de tarefas."""
from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = BASE_DIR / "instance" / "tasks.json"
VALID_PRIORITIES = {"Baixa", "Média", "Alta"}
VALID_STATUSES = {"A Fazer", "Em Progresso", "Concluída"}


def load_tasks(data_file: str | Path) -> list[dict]:
    """Carrega tarefas do arquivo JSON; retorna lista vazia se ainda não existir."""
    path = Path(data_file)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(data_file: str | Path, tasks: list[dict]) -> None:
    """Salva a lista de tarefas em JSON, criando a pasta quando necessário."""
    path = Path(data_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
    app.config.update(DATA_FILE=os.environ.get("TASKFLOW_DATA_FILE", str(DEFAULT_DATA_FILE)))
    if test_config:
        app.config.update(test_config)

    def get_tasks() -> list[dict]:
        return load_tasks(app.config["DATA_FILE"])

    def persist(tasks: list[dict]) -> None:
        save_tasks(app.config["DATA_FILE"], tasks)

    @app.get("/")
    def index():
        tasks = get_tasks()
        status_filter = request.args.get("status", "")
        priority_filter = request.args.get("priority", "")
        if status_filter in VALID_STATUSES:
            tasks = [task for task in tasks if task["status"] == status_filter]
        if priority_filter in VALID_PRIORITIES:
            tasks = [task for task in tasks if task["priority"] == priority_filter]
        return render_template(
            "index.html", tasks=tasks, statuses=sorted(VALID_STATUSES),
            priorities=["Alta", "Média", "Baixa"],
            selected_status=status_filter, selected_priority=priority_filter,
        )

    @app.post("/tasks")
    def add_task():
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Média")
        if not title or len(title) > 100 or priority not in VALID_PRIORITIES:
            return "Título obrigatório (até 100 caracteres) e prioridade válida são necessários.", 400
        tasks = get_tasks()
        tasks.append({
            "id": str(uuid4()), "title": title, "description": description,
            "priority": priority, "status": "A Fazer",
        })
        persist(tasks)
        return redirect(url_for("index"))

    @app.post("/tasks/<task_id>/status")
    def update_status(task_id: str):
        status = request.form.get("status", "")
        if status not in VALID_STATUSES:
            return "Status inválido.", 400
        tasks = get_tasks()
        task = next((item for item in tasks if item["id"] == task_id), None)
        if task is None:
            return "Tarefa não encontrada.", 404
        task["status"] = status
        persist(tasks)
        return redirect(url_for("index"))

    @app.post("/tasks/<task_id>/edit")
    def edit_task(task_id: str):
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Média")
        if not title or len(title) > 100 or priority not in VALID_PRIORITIES:
            return "Título obrigatório (até 100 caracteres) e prioridade válida são necessários.", 400
        tasks = get_tasks()
        task = next((item for item in tasks if item["id"] == task_id), None)
        if task is None:
            return "Tarefa não encontrada.", 404
        task.update(title=title, description=description, priority=priority)
        persist(tasks)
        return redirect(url_for("index"))

    @app.post("/tasks/<task_id>/delete")
    def delete_task(task_id: str):
        tasks = get_tasks()
        updated = [task for task in tasks if task["id"] != task_id]
        if len(updated) == len(tasks):
            return "Tarefa não encontrada.", 404
        persist(updated)
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
