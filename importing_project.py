import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event

async def on_ready():
    print(f"We have logged in as {client.user}")
    
@client.event

async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startsWith("$hello"):
        await message.channel.send("Hello!")

client.run("MTA1NDk1ODQxMTg5ODQyMTI1OA.Gwerg-.S2l7Kvg4niT0t0MNBuYIjnz8fuIrBnHBV8LwSg")