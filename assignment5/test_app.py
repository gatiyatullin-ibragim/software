import io
import json

from app import InMemoryTaskStorage, TaskApplication


def request(application, method, path, payload=None, raw_body=None):
    if raw_body is None:
        if payload is None:
            body = b""
        else:
            body = json.dumps(payload).encode("utf-8")
    else:
        body = raw_body

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": io.BytesIO(body),
    }
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    body_chunks = application(environ, start_response)
    response_body = b"".join(body_chunks)
    return (
        int(captured["status"].split(" ", 1)[0]),
        json.loads(response_body) if response_body else None,
    )


def test_create_list_and_delete_acceptance_criteria():
    application = TaskApplication(InMemoryTaskStorage())

    status, created = request(application, "POST", "/tasks", {"title": "Ship"})
    assert status == 201
    assert created["title"] == "Ship"
    assert created["id"] == 1

    status, listed = request(application, "GET", "/tasks")
    assert status == 200
    assert listed == [created]

    status, deleted = request(application, "DELETE", "/tasks/1")
    assert status == 200
    assert deleted == created

    status, listed = request(application, "GET", "/tasks")
    assert status == 200
    assert listed == []


def test_invalid_json_does_not_mutate_store():
    storage = InMemoryTaskStorage()
    application = TaskApplication(storage)

    status, payload = request(application, "POST", "/tasks", raw_body=b"{bad-json")
    assert status == 400
    assert payload == {"error": "Invalid JSON"}
    assert storage.list_all() == []


def test_missing_required_field_does_not_mutate_store():
    storage = InMemoryTaskStorage()
    application = TaskApplication(storage)

    status, payload = request(application, "POST", "/tasks", {})
    assert status == 400
    assert payload == {"error": "Missing or invalid required field: title"}
    assert storage.list_all() == []


def test_delete_missing_task_returns_404():
    application = TaskApplication(InMemoryTaskStorage())

    status, payload = request(application, "DELETE", "/tasks/999")
    assert status == 404
    assert payload == {"error": "Task not found"}


def test_storage_strategy_can_be_replaced():
    class AlternateStorage(InMemoryTaskStorage):
        pass

    application = TaskApplication(AlternateStorage())
    status, created = request(application, "POST", "/tasks", {"title": "Task"})
    assert status == 201
    assert created["title"] == "Task"
