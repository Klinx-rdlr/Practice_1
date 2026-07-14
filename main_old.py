from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str


app = FastAPI()

tasks = []
next_id = 1

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_id
    new_task = task.model_dump()
    new_task["id"] = next_id
    next_id += 1
    tasks.append(new_task)
    return {"added_task": new_task}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"task removed": task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{id}")
def update_task(id: int, updated_task: TaskCreate):
    for task in tasks:
        if task["id"] == id:
            task["title"] = updated_task.title
            return {"updated_task": updated_task}
    raise HTTPException(status_code=404, detail="Task not found")