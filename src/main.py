import os
from dotenv import load_dotenv
from bot import Bot

load_dotenv()

CLIENT = Bot()

token = os.getenv("TOKEN")
if not token:
    raise Exception("TOKEN not found in environment variables")

CLIENT.run(token)