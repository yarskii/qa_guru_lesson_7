import os.path
from random import randint

CURRENT_FILE = os.path.abspath(__file__)

CURRENT_DIR = os.path.dirname(CURRENT_FILE)

TMP_DIR = os.path.join(CURRENT_DIR, "temp")

if not os.path.exists("temp"):
    os.mkdir("temp")

NUM = randint(1, 5)
