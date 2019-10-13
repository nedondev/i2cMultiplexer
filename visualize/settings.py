from dotenv import load_dotenv
import os

load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")
PORT = int(os.getenv("PORT"))
