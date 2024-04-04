from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

#App Object
app = FastAPI()


from model import Todo
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    delete_todo
)

origins = ['http://localhost:3000/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Ping":"Pong"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await get_todo_by_id(title)
    if response:
        return response
    raise HTTPException(404, "There is no Todo item with this title")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad Request")

@app.put("/api/todo{title}/", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, "There is no Todo item with this title")

@app.delete("/api/todo{title}")
async def delete_todo(title : str):
    response = await delete_todo(title)
    if response:
        return "Succesfully deleted todo item !"
    raise HTTPException(404, "There is no Todo item with this title")