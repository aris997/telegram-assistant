# import ngrok python sdk
from time import sleep
import yaml
import ngrok
import requests
import telegram_endpoint
from fastapi import FastAPI, Request
import uvicorn
from log import *


app = FastAPI()

with open('secrets.yaml', mode = 'r') as f:
    secrets = yaml.safe_load(f)

TELEGRAM_SEND_MESSAGE = f"https://api.telegram.org/bot{secrets['TELEGRAM_BOT_TOKEN']}/SendMessage"

@app.get("/")
async def health_check(request: Request):
    logger.debug(f"GET Request OK 200")
    return {"status":"ok", "status_code" : 200}

@app.post("/webhook")
async def messager(request: Request):

    payload = await request.json()
    chat_id = payload.get("message", {}).get("chat", {}).get("id", 0)
    user_message = payload.get("message", {}).get("text", "")
    logger.debug(user_message)

    bot_message = user_message

    message = {
        "chat_id" : chat_id,
        "text" : bot_message
        }
    response = requests.post(TELEGRAM_SEND_MESSAGE, json = message)
    logger.debug(response)
    return response.json()



if __name__ == "__main__":
    listener = ngrok.forward("0.0.0.0:9000", authtoken = secrets['NROK_AUTH_TOKEN'])
    sleep(1)
    print(f"Ingress established at {listener.url()}")
    print(telegram_endpoint.set(secrets['TELEGRAM_BOT_TOKEN'], listener.url()))
    sleep(1)
    uvicorn.run("main:app", host = "0.0.0.0", port = 9000, reload = False)