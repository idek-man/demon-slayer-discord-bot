# keep_alive.py
from flask import Flask
import threading
import os
import bot  # Import your bot file (without running bot.run here!)

app = Flask(__name__)

@app.route("/")
def home():
    return "☀️ Demon Slayer Bot is running!", 200

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    server = threading.Thread(target=run)
    server.start()
    
