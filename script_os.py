import os.path
from random import choice

CURRENT_FILE = os.path.abspath(__file__)

CURRENT_DIR = os.path.dirname(CURRENT_FILE)

TMP_DIR = os.path.join(CURRENT_DIR, "temp")

if not os.path.exists("temp"):
    os.mkdir("temp")

NUM = choice([1, 2, 3, 4, 5])




