import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = [
    "sad", "unhappy", "die", "depressed", "angry", "failed",
    "can't take this anymore", "tired", "unmotivated", "frustrated", "fear",
    "rejected", "cant't handle this anymore", "pressurized"
]

starter_encouragements = [
    "Cheer up", "Hang on!", "You are not this kind of person!",
    "Come on, you can overcome this!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)

    quote = "\'" + json_data[0]['q'] + "\' *-" + json_data[0]['a'] + "*"
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$help'):
        await message.channel.send(
            "1.** $hello bot** - say hello to our bot\n2.** $inspire** - Gives you random inpirational quotes\n3.** $new** - add new encouragments senteces [Syntax :** $new** encouraging_quote/sentences\n4.** $del** - delete the sentece/quote from the database. [Syntax : ** $del** index_value *\n5.** $list**  - list all the senteces present in the data base which has been added by a particular user.\n6.** $respond true/false** - responding on negative vibes word feature on/off"
        )

    if msg.startswith('$hello bot'):
        await message.channel.send("Hello! {0} ".format(message.author))

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send('{0}'.format(quote))

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(db["encouragements"].value)

    if msg.startswith("$respond"):
      values = msg.split("$respond ", 1)[1]

      if values.lower() == "true":
          db["responding"] = True
          await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

keep_alive()


client.run(os.getenv('TOKEN'))
