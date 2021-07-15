import discord
import os
#allows code to make https requests to retrieve data from api
import aiohttp
#api returns JSON
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "mad", "annoyed", "tired", "vent"]

init_encouragements = [
    "Cheer up!", "Look on the bright side!", "Hope you feel better soon~",
    "Sorry you felt that way~", "*sends you a virtual hug*", "<3"
]

if "ready" not in db.keys():
  db["ready"] = True

def update_encouragements(enc_msg):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(enc_msg)
        print(enc_msg + ' was added to the eng_msg database!')
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [enc_msg]
        print(enc_msg + ' was added to the new eng_msg database!')

def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!hello'):
        await message.channel.send('Hello!')

    if msg.startswith('!Inspire'):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://zenquotes.io/api/random') as response:
            html = await response.text()
            json_data = json.loads(html)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await message.channel.send(quote)

    #to combine init msgs with user submitted ones
    if db["ready"]:
      options = init_encouragements
      if "encouragements" in db.keys():
        options = options + list(db["encouragements"])
        #moved this part into the conditional to avoid unbound local error
        if any(word in msg for word in sad_words):
          await message.channel.send(random.choice(options))


    if msg.startswith("!new"):
        enc_msg = msg.split("!new ", 1)[1]
        update_encouragements(enc_msg)
        await message.channel.send(
            "New encouraging message added. Thanks for sharing! ^~^")
        print('testing?')

    if msg.startswith("!del"):
      encouragements = []
      if "encouragements" in db.keys():
          index = int(msg.split("!del", 1)[1])
          delete_encouragement(index)
          encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("!list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("!ready"):
      value = msg.split("!ready ", 1)[1]

      if value.lower() == "true":
        db["ready"] = True
        await message.channel.send("I'm ready to encourage!")
      else:
        db["ready"] = False
        await message.channel.send("I'm out of here!")

#dont give away tokens to strangers lol
client.run(os.environ['TOKEN'])
