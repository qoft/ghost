import os

def create_defaults():
    if not os.path.exists("scripts/"):
        os.mkdir("scripts/")