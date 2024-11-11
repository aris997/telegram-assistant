from time import sleep
import yaml
import ngrok
import requests
import telegram_endpoint
from fastapi import FastAPI
from fastapi import Request
import uvicorn
from log import logger
from openai import OpenAI
import utils
import json
app = FastAPI()

ECHO: bool = True
UNUSEFUL_KEYS = ["chat", "date", "from", "message_id"]

with open('secrets.yaml', mode = 'r') as f:
    secrets = yaml.safe_load(f)

TELEGRAM_SEND_MESSAGE = f"https://api.telegram.org/bot{secrets['TELEGRAM_BOT_TOKEN']}/SendMessage"
client = OpenAI(api_key=secrets['OPENAI_APIKEY'])

@app.get("/")
async def health_check(request: Request):
    logger.debug(f"GET Request OK 200")
    return {"status":"ok", "status_code" : 200}

@app.post("/webhook")
async def messager(request: Request):
    payload: dict[dict] = await request.json()
    with open(f"incoming_payloads/item_{utils.now()}.json", mode = 'w') as f:
        json.dump(payload, f, ensure_ascii=True, indent=4, sort_keys=True)

    chat_id = payload.get("message", {}).get("chat", {}).get("id", 0)
    message_type = [key for key in payload.get("message", {}).keys() if key not in UNUSEFUL_KEYS]
    logger.debug(f"{message_type}, {type(message_type) = }")

    if 'text' in message_type:
        user_message = payload.get("message", {}).get("text", "")
        logger.debug(user_message)
        if not ECHO:
            logger.info('gpt-4o started')
            completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {"role": "system", "content": "Be an helpful assistant in a telegram chat. If it's needed use the right syntax to highlight titles, bullet points and more. You are allowed to use emojis."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_message = completion.choices[0].message.content
        elif ECHO:
            logger.debug('echo mode')
            bot_message = user_message
        else:
            logger.error('echo not set')
            bot_message = 'error FLAG ECHO not set.'
    else:
        logger.error("not a text message")
        bot_message = f"Sorry, issues encountered. You sent a \*{message_type[0]}\*. Check datatype you sent."

    message = {
        "chat_id" : chat_id,
        "text" : str(bot_message),
        "parse_mode": "MarkdownV2"
        }
    response = requests.post(TELEGRAM_SEND_MESSAGE, json = message)
    logger.debug(response.content)
    return response.json()

if __name__ == "__main__":
    listener = ngrok.forward("0.0.0.0:8001", authtoken = secrets['NROK_AUTH_TOKEN'])
    sleep(1)
    print(f"Ingress established at {listener.url()}")
    print(telegram_endpoint.set(secrets['TELEGRAM_BOT_TOKEN'], listener.url()))
    sleep(1)
    uvicorn.run("main:app", host = "0.0.0.0", port = 8001, reload = False)