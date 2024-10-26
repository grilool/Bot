from fastapi import FastAPI
import os
from typing import Optional
from mongo import *

app = FastAPI()

@app.get("/users")
def get_users():
    k = []
    for res in users.find():
        k.append(res)
    print(k)
    return k[0]
