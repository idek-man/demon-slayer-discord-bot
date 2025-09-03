import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "Bot is running!", 200

import bot
