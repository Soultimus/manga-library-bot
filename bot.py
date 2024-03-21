import discord
import json
import os
import requests
import time

from discord.ext import commands, tasks


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

subscriptions_file = "subscriptions.json"
subscriptions = []

if __name__ == "__main__":
    with open(subscriptions_file, 'r') as f:
        subscriptions = json.load(f)

@bot.event
async def on_ready():
    print("Bot is up and running!")
    check_chapters.start()

# Help command
@bot.command()
async def h(ctx):
    embed = discord.Embed(
        title="Hello!",
        description=
        """
        \U0001F4DA**Here's what I can do**:
        `sub`: Subscribe to a manga series. I'll send a notification when a new chapter is published.
        `unsub`: Unsubscribe to a manga series.
        `list`: List the manga you're currently following
        """
    )
    await ctx.send(embed=embed)

# Subscribe to a series
base_url = "https://api.mangadex.org"
@bot.command()
async def sub(ctx, *, title):
    await ctx.send('Looking...')
    r = requests.get(
        f"{base_url}/manga",
        params={ "title": title }
    )
    if r.status_code == 200 :
        try:
            info = r.json()["data"][0]
            id = info["id"]
            retrieved_title = info["attributes"]["title"].get("en") or info["attributes"]["title"].get("ja-ro")
            if retrieved_title is None:
                raise KeyError("Title language was something different than English or Romanji")
            r = requests.get(
                f"{base_url}/manga/{id}/feed",
                params={"translatedLanguage[]": "en"}
            )
            if r.status_code == 200:
                latest = ""
                json = r.json()
                for i in range(len(json["data"]) - 1):
                    if float(json["data"][i + 1]["attributes"]["chapter"]) > float(json["data"][i]["attributes"]["chapter"]):
                        latest = float(json["data"][i + 1]["attributes"]["chapter"])
                obj = {
                    "id": id,
                    "title" : retrieved_title,
                    "latest" : latest
                }
                # Write to file
                add_new_title(obj)
                await ctx.send(f'Found it! You\'re now following **{retrieved_title}**. I\'ll send you a notification when a new chapter is out!')
        except:
            # Typically sent when I wrote an invalid title
            await ctx.send('Sorry, but I couldn\'t find the title you\'re looking for... Did you write it correctly?')

# Unsubscribe to a series
@bot.command()
async def unsub(ctx, *, title):
    with open(subscriptions_file, 'r') as file:
        data = json.load(file)

    try:
        subscriptions.clear()
        actual_title = ""
        for sub in data:
            if title not in sub["title"]:
                subscriptions.append(sub)
            else:
                actual_title = sub["title"]

        with open(subscriptions_file, 'w') as file:
            json.dump(subscriptions, file, indent=4)
    
        await ctx.send(f"I have unsubscribed you from **{actual_title}**. Hope you enjoyed reading it!")
    
    except:
        await ctx.send("It doesn't seem like you're subscribed to this series... Are you sure you remember its name correctly?")


# List all subscribed series
@bot.command()
async def list(ctx):
    list = ""
    for manga in subscriptions:
        list += f"- {manga["title"]}\n"

    embed = discord.Embed(
        title="Here's what you're currently reading!",
        description=list
    )
    await ctx.send(embed=embed)


# Check for new chapters
@tasks.loop(hours=1)
async def check_chapters():
    for manga in subscriptions:
        r = requests.get(
                f"{base_url}/manga/{manga["id"]}/feed",
                params={"translatedLanguage[]": ["en"]}
            )
        if r.status_code == 200:
            json = r.json()
            for data in json["data"]:
                if float(data["attributes"]["chapter"]) > manga["latest"]:
                    channel = discord.utils.get(bot.get_all_channels(), name="manga-updates")
                    await channel.send(
                        f"A new chapter for **{manga["title"]}** was released!\nRead it here: https://mangadex.org/chapter/{data["id"]}"
                    )
        time.sleep(30)


def add_new_title(obj):
    # Load existing JSON data from the file
    with open(subscriptions_file, 'r') as file:
        data = json.load(file)
    
    # Append the dictionary to the list
    data.append(obj)

    # Write the updated list to the file
    with open(subscriptions_file, 'w') as file:
        json.dump(data, file, indent=4)

    subscriptions.append(obj)
            

bot.run(os.getenv('DISCORD_TOKEN'))
