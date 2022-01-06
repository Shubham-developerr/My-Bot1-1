import discord
import os
import requests 
import json 
import random
from replit import db

client = discord.Client()
sad_words = ["sad","depressed","depressing","unhappy","angry","lonely"]

starter_encouragements =[
  "cheer up!",
  "Don.t be!",
  "hang on!",
  "you are a great person/bot"
]
if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+"-"+json_data[0]['a']
  return(quote)
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > len(index):
    del encouragements[index]
    db["encouragements"] = encouragements
  
token = os.environ['token']
@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))
  @client.event
  async def on_message(message):
    if message.author==client.user:
      return
    msg = message.content
    if msg.startswith('$hello'):
      quote= get_quote()
      await message.channel.send(quote)
    if db["responding"]:
      options = (starter_encouragements)
      if "encouragements" in db.keys():
        options =options + list(db["encouragements"])
      if any(word in msg for word in sad_words) :
        await message.channel.send(random.choice(options))
    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")
    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        db['encouragements'] = encouragements
        index = (msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    if msg.startswith("$list"):
      keys = db.keys()
      await message.channel.send(keys)

client.run(token)