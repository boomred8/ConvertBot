import  os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("BOT_TOKEN environment variable not set")