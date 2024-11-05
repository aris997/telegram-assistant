import os
import traceback
from datetime import datetime

def now():
    """return a string of 12 numbers indicating `year month day hour minute second`"""
    return datetime.now().strftime("%y%m%d%H%M%S")

def create_folder(path: str) -> str:
    """This just check if a folder exist, if not it create it. Error handling correct. Hopefuly"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return path
        else:
            return path
    except Exception as e:
        print("ERROR", e, traceback.format_exc())
        return ""