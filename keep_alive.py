import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "Bot is running!", 200

import bot

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 👈 must use $PORT
    app.run(host="0.0.0.0", port=port)
