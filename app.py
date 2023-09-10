from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from json import dumps
from model.User import User
from model.Users import Users
from model.Blacklist import Blacklist
from helper.jwt_helper import generate_jwt_token, decode_jwt_token, validate_jwt_token, public_pem
from datetime import datetime

app = FastAPI()

users = Users._users
blacklist = Blacklist._blacklist

@app.get("/")
async def root():
    return f"boop :3"

@app.get("/api/v1/auth/users")
async def root():
    return users

@app.post("/api/v1/auth/login")
async def login(user: User):
    for registered_user in users:
        if user.name == registered_user.name and user.password == registered_user.password:
            token = generate_jwt_token(user=user.name, role=registered_user.role)
            return JSONResponse(content={"token": token, "generated_time": datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}, status_code=200)
    return JSONResponse(content={"msg": "Login failed", "generated_time": datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}, status_code=401)

@app.put("/api/v1/auth/logout")
async def logout(token = Header(None)):
    blacklist.append(token)
    return "logged out"

@app.post("/api/v1/auth/register")
async def register(user: User):
    users.append(user)
    return JSONResponse(content=user.model_dump(), status_code=201)

@app.get("/api/v1/auth/validate")
async def validate(token = Header(None), role: Optional[list] = []):
    
    if token not in blacklist and validate_jwt_token(token)[0]:
        decoded_token = decode_jwt_token(token)
        if not role:
            return JSONResponse(content="Valid token", status_code=200)
        elif role in decoded_token:
            return JSONResponse(content="Valid token", status_code=200)
    return JSONResponse(content="Invalid token", status_code=401)

@app.get("/api/v1/auth/keys")
async def getKeys():
    return public_pem