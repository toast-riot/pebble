import os
from bot import Bot

CLIENT = Bot()

token = os.getenv("TOKEN")
if not token:
    raise RuntimeError("TOKEN not found in environment variables")

CLIENT.run(token)