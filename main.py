from pydantic import BaseModel
import json
import requests
from fastapi import FastAPI, Request

version = "Beta 1.0.0"

app = FastAPI()

class attendance_submission(BaseModel):
    course_name: str
   
def send_message(id, message):
    token = "8022723908:AAESaQMh7pFdPICysbLKhYt5UETY1DB7HlM"
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
