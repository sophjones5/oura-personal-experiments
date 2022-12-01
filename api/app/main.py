from fastapi import FastAPI,Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class User(BaseModel):
    Auth_token: Optional[str] = None
    Authenticated: Optional[bool] = False
    Experiment: Optional[str]
    Name: str
    Email: str
    Experiment_Classification_dict: Optional[dict]
    Created_at: Optional[datetime]

#----------database connection----------
text_file = open("app/password.txt", "r")
password = text_file.read()
text_file.close()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='oura',user='postgres', password=password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error:",error)
        time.sleep(3)

#----------api endpoints----------
@app.get("/users")
def get_all_users():
    cursor.execute("""SELECT * FROM public."User" """)
    users = cursor.fetchall()
    return {"Data": users}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user :User):
    cursor.execute("""INSERT INTO public."User" ("Name", "Email") VALUES (%s,%s) RETURNING * """, (user.Name, user.Email))
    new_user = cursor.fetchone()
    conn.commit()
    return{'new user':new_user}

@app.get("/users/{id}")
def get_user(id: int, response:Response):
    cursor.execute("""SELECT * FROM public."User" WHERE "UID" = %s """, (str(id)))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'user with id: {id} was not found')
    return {'User':user}

@app.delete("/users/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id):
    #delete user
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'user with id: {id} was not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/users/{id}")
def update_post(id: int, user: User):
    #update user
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'user with id: {id} was not found')
    
    user_dict = user.dict()
    user_dict['UID'] = id
    #my_users[index] = user_dict
    
    return{'message':user_dict}
