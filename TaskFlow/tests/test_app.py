"""Testes automatizados das rotas principais do TaskFlow."""
import json

import pytest

from src.app import create_app


@pytest.fixture()
def client(tmp_path):
    data_file = tmp_path / "tasks.json"
    app = create_app({"TESTING": True, "DATA_FILE": str(data_file)})
    with app.test_client() as test_client:
        yield test_client


def add_task(client, title="Separar pedidos", description="Pedidos prioritários", priority="Alta"):
    return client.post("/tasks", data={
        "title": title, "description": description, "priority": priority,
    }, follow_redirects=True)


def read_tasks(data_file):
    return json.loads(data_file.read_text(encoding="utf-8"))


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_create_task_and_persist(client, tmp_path):
    response = add_task(client)
    assert response.status_code == 200
    assert b"Separar pedidos" in response.data
    tasks = read_tasks(tmp_path / "tasks.json")
    assert len(tasks) == 1
    assert tasks[0]["priority"] == "Alta"
    assert tasks[0]["status"] == "A Fazer"


def test_title_is_required(client):
    response = client.post("/tasks", data={"title": "   ", "priority": "Média"})
    assert response.status_code == 400


def test_invalid_priority_is_rejected(client):
    response = client.post("/tasks", data={"title": "Tarefa", "priority": "Urgente"})
    assert response.status_code == 400


def test_update_status(client, tmp_path):
    add_task(client)
    task = read_tasks(tmp_path / "tasks.json")[0]
    response = client.post(f"/tasks/{task['id']}/status", data={"status": "Em Progresso"})
    assert response.status_code == 302
    assert read_tasks(tmp_path / "tasks.json")[0]["status"] == "Em Progresso"


def test_edit_task(client, tmp_path):
    add_task(client)
    task = read_tasks(tmp_path / "tasks.json")[0]
    response = client.post(f"/tasks/{task['id']}/edit", data={
        "title": "Pedidos conferidos", "description": "Conferência concluída", "priority": "Baixa",
    })
    assert response.status_code == 302
    edited = read_tasks(tmp_path / "tasks.json")[0]
    assert edited["title"] == "Pedidos conferidos"
    assert edited["priority"] == "Baixa"


def test_delete_task(client, tmp_path):
    add_task(client)
    task = read_tasks(tmp_path / "tasks.json")[0]
    response = client.post(f"/tasks/{task['id']}/delete")
    assert response.status_code == 302
    assert read_tasks(tmp_path / "tasks.json") == []


def test_filter_by_priority(client):
    add_task(client, title="Pedido urgente", priority="Alta")
    add_task(client, title="Organizar arquivos", priority="Baixa")
    response = client.get("/?priority=Alta")
    assert b"Pedido urgente" in response.data
    assert b"Organizar arquivos" not in response.data
