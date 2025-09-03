import discord
from discord.ext import commands
from groq import Groq
import keep_alive  # this imports the Flask app so gunicorn can serve it

import os
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix="!", intents=intents)

client_ai = Groq(api_key=GROQ_API_KEY)
conversation_history = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"☀️ The Breath of the Sun awakens within {bot.user}")

@bot.tree.command(name="sun_breath", description="Channel the Breath of the Sun and seek guidance")
async def sun_breath(interaction: discord.Interaction, question: str):
    user_id = str(interaction.user.id)

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": question})

    try:
        response = client_ai.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history[user_id],
        )

        bot_reply = response.choices[0].message.content
        conversation_history[user_id].append({"role": "assistant", "content": bot_reply})

        if len(conversation_history[user_id]) > 10:
            conversation_history[user_id] = conversation_history[user_id][-10:]

        await interaction.response.send_message(
            f"☀️ *Breath of the Sun answers your call...*\n\n{bot_reply}"
        )

    except Exception as e:
        await interaction.response.send_message("⚠️ The flame flickers... no answer came.")
        print("---- ERROR ----")
        print(e)

@bot.command()
async def ask(ctx, *, question: str = None):
    user_id = str(ctx.author.id)

    if not question:
        await ctx.send("❓ Use it like this: `!ask your question`")
        return

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": question})

    try:
        response = client_ai.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history[user_id],
        )

        bot_reply = response.choices[0].message.content
        conversation_history[user_id].append({"role": "assistant", "content": bot_reply})

        if len(conversation_history[user_id]) > 10:
            conversation_history[user_id] = conversation_history[user_id][-10:]

        await ctx.send(f"🔥 *The Demon Slayer AI declares...*\n\n{bot_reply}")

    except Exception as e:
        await ctx.send("⚠️ Even the Hashira are silent on this matter...")
        print("---- ERROR ----")
        print(e)

@bot.command()
async def delete(ctx, amount: int = 1):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ The crow erased {amount} messages.", delete_after=5)

@bot.command()
async def kick(ctx, member: discord.Member):
    await member.kick(reason="Banished by the Demon Slayer Bot")
    await ctx.send(f"👢 {member} was cast out from the Corps.")

@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban(reason="Sealed by the Demon Slayer Bot")
    await ctx.send(f"🔨 {member} was struck down by the Demon Slayer’s judgment.")

bot.run(DISCORD_TOKEN)
