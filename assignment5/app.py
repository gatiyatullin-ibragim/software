import json
from abc import ABC, abstractmethod
from threading import Lock


class TaskStorage(ABC):
    @abstractmethod
    def create(self, payload):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id):
        raise NotImplementedError


class InMemoryTaskStorage(TaskStorage):
    def __init__(self):
        self._tasks = {}
        self._next_id = 1
        self._lock = Lock()

    def create(self, payload):
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            task = {"id": task_id, **payload}
            self._tasks[task_id] = task
            return task

    def list_all(self):
        with self._lock:
            return [dict(task) for task in self._tasks.values()]

    def delete(self, task_id):
        with self._lock:
            return self._tasks.pop(task_id, None)


class TaskApplication:
    def __init__(self, storage):
        self.storage = storage

    def __call__(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "")

        if method == "POST" and path == "/tasks":
            return self._create_task(environ, start_response)
        if method == "GET" and path == "/tasks":
            return self._json_response(start_response, 200, self.storage.list_all())
        if method == "DELETE" and path.startswith("/tasks/"):
            return self._delete_task(path, start_response)
        return self._json_response(start_response, 404, {"error": "Not found"})

    def _create_task(self, environ, start_response):
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
            body = environ["wsgi.input"].read(length)
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            return self._json_response(start_response, 400, {"error": "Invalid JSON"})

        if not isinstance(payload, dict):
            return self._json_response(
                start_response, 400, {"error": "Invalid payload"}
            )

        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            return self._json_response(
                start_response,
                400,
                {"error": "Missing or invalid required field: title"},
            )

        task = self.storage.create({"title": title})
        return self._json_response(start_response, 201, task)

    def _delete_task(self, path, start_response):
        raw_id = path.removeprefix("/tasks/")
        try:
            task_id = int(raw_id)
        except ValueError:
            return self._json_response(start_response, 404, {"error": "Task not found"})

        task = self.storage.delete(task_id)
        if task is None:
            return self._json_response(start_response, 404, {"error": "Task not found"})
        return self._json_response(start_response, 200, task)

    @staticmethod
    def _json_response(start_response, status, payload):
        body = json.dumps(payload).encode("utf-8")
        start_response(
            f"{status} "
            + {
                200: "OK",
                201: "Created",
                400: "Bad Request",
                404: "Not Found",
            }[status],
            [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]


application = TaskApplication(InMemoryTaskStorage())
app = application
