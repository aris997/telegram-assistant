# import ngrok python sdk
import ngrok
import time
import yaml
import telegram_endpoint
from log import *

with open('secrets.yaml', mode = 'r') as f:
    secrets = yaml.safe_load(f)

# Establish connectivity
listener = ngrok.forward(80, authtoken=secrets['NROK_AUTH_TOKEN'])

# Output ngrok url to console
logger.info(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Closing listener")