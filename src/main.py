import os
from dotenv import load_dotenv
from bot import Bot

load_dotenv()

CLIENT = Bot()
CLIENT.run(os.getenv("TOKEN"))