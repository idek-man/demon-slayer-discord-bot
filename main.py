# main.py
from keep_alive import keep_alive
from bot import bot, DISCORD_TOKEN

keep_alive()
bot.run(DISCORD_TOKEN)
