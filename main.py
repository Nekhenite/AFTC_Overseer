from pydantic import BaseModel
import json
import requests
from fastapi import FastAPI, Request
from enum import Enum
import os
from dotenv import load_dotenv

version = "Beta 2.0.0"

app = FastAPI()

class ApiMethod(Enum):
    GET = 1
    POST = 2
    UPDATE = 3
    DELETE = 4


class course(BaseModel):
    course_name: str
    course_display_name: str
    poc: str
    poc_contact: str

def get_env_var(var):
    load_dotenv()
    envVar = os.getenv(var)
    return envVar

def supabase_api_call(path: str, method: ApiMethod):
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1dW5qdXBweXNscmhpZmJlY2lnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM3NTYzMDQsImV4cCI6MjA1OTMzMjMwNH0" \
    ".VgKmGPPt5WegB4RD_-aaA-Zg_hGWSLytMdWuut0JtqQ"
    url = "https://puunjuppyslrhifbecig.supabase.co/rest/v1"

    response = ""

    match (method):
        case ApiMethod.GET:
            response = requests.get(url+path, headers={"apikey": key})

    return response


def send_message(id, message):
    token = get_env_var("botToken")
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': id, 'text': message}
    requests.post(url, payload)

def handle_command(id, command):
    match(command):
        case "/report":
            send_message(id, "/report called")

        case "/add_course":
            send_message(id, "/add_course called")

        case "/get_courses":
            send_message(id, "/get_courses called")

        case "/remove_course":
            send_message(id, "/remove_course called")

        case "/cancel":
            send_message(id, "/cancel called")

        case "/help":
            send_message(id, "/cancel called")
        
        case "/start":
            send_message(id, f"AFTC Attendance Bot\nVersion: {version}")
        case _:
            send_message(id, "Unknown Command")
            
@app.post("/webhook")
async def telegram_webhook(request: Request):

    body = await request.json()

    if "message" in body and "text" in body["message"]:
        message = body["message"]["text"]
        id = body["message"]["from"]["id"]
        username = body["message"]["from"]["username"]

        if  (message.startswith("/")):
            handle_command(id, message)

        print(f"{username}({id}) says: {message}")

        send_message(id, f"{username}({id}) says: {message}")

    print(body)

    return {"OK": "200"}
