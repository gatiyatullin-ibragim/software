# Acceptance Criteria

1. **Create Task (`POST /tasks`):** Sending a valid task payload creates a new task and returns HTTP status `201 Created` along with the created task representation.
2. **Invalid Payload Handling:** Sending malformed/invalid JSON or missing required fields to endpoints accepting a JSON body returns HTTP status `400 Bad Request` without mutating stored state.
3. **List Tasks (`GET /tasks`):** Requesting the tasks collection returns HTTP status `200 OK` and a JSON list/array of tasks matching the current store state.
4. **Delete Task (`DELETE /tasks/{id}`):** Deleting an existing task by ID removes it from the task list and returns HTTP status `200 OK` (or `204 No Content`), while requesting a non-existent ID returns `404 Not Found`.
