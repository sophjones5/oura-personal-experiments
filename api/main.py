from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    UID: int
    Auth_token: Optional[str] = None
    Authenticated: Optional[bool] = False
    Experiment: str
    Classification_dict: dict
    Name: str
    Email: str

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/users")
def posts():
    return {"Hello": "User"}

@app.post("/users")
def create_user(new_user :User):
    print(new_user)
    return{'user created':new_user.Name}

