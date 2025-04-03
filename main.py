from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.any("/")
def read_root():
    return {"Hello": "World"}
