from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from json import dumps

app = FastAPI()

temp_db = []
blacklist_db = []


class User(BaseModel):
    name: str
    password: str
    role: Optional[list] = []


@app.get("/")
async def root():
    return "hello"

@app.get("/user")
async def root():
    return temp_db

@app.post("/login")
async def login(user: User):
    for registered_user in temp_db:
        if user.name == registered_user.name and user.password == registered_user.password:
            return JSONResponse(content="fake token", status_code=200)
    return JSONResponse(content="Login failed", status_code=401)

@app.post("/logout")
async def logout(token):
    blacklist_db.append(token)
    return "logged out"

@app.post("/register")
async def register(user: User):
    temp_db.append(user)
    return JSONResponse(content=user.model_dump(), status_code=201)

@app.post("/validate")
async def validate(token):
    return JSONResponse(content="Invalid token", status_code=401)