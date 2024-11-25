import os
import locale
import logging
import logging.handlers

import utils

# logger
LOG_DIR = os.path.join("logs")
utils.create_folder(LOG_DIR)

# max size of log file:
MAX_BYTES = 20 * 1024 * 1024  # 20 MBytes
MAX_BACKUPS_LOGS = 5
LOG_FNAME = os.path.join(LOG_DIR, f"echobot_{utils.now()[:7]}.log")

# If you want to read months in your language
locale.setlocale(locale.LC_ALL, "it_IT.UTF-8")

# TODO: monkeytype the colors to the logging class so that the colors change
# following the level of criticity
formatter = logging.Formatter(
    "%(levelname)s:    %(asctime)s \033[94mf=%(funcName)s \033[95m%(filename)s:%(lineno)d\033[0m %(message)s",
    datefmt="%d %B %Y %H:%M:%S",
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FNAME,
    mode="a",
    maxBytes=MAX_BYTES,
    backupCount=MAX_BACKUPS_LOGS,
    encoding="utf-8",
    delay=False,
)
formatter = logging.Formatter(
    "%(levelname)s: %(asctime)s f=%(funcName)s %(filename)s:%(lineno)d = %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S",
)
file_handler.setFormatter(formatter)
logger = logging.getLogger("echobot")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# level set should be in global as a global var
logger.setLevel(logging.DEBUG)
