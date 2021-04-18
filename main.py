import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import urllib


client = discord.Client()



sad_words = ["sad", "unhappy", "die", "depressed", "angry", "failed","can't take this anymore", "tired","unmotivated", "frustrated", "fear","rejected", "cant't handle this anymore", "pressurized"]

starter_encouragements = [">>> Cheer up 🤗" , ">>> Hang on!", ">>> You are not this kind of perso!",">>> Come on, you can overcome this!"]

cmd = ["#hello-bot","#inspire-me","#new-sentence","#del-sentence","#list-sentece","#respond","#add-event", "#list-event", "#del-event", "#meme","#joke","#help","#syntax","#celebrate","#git search"]

bad_words = ["fuck", "asshole", "slut", "lesbian","gay","shit","horny","madharchod"]

code_not_working = ["not working","error","failed","code is dumb"]

code_not_working_sentence = [">>> :coffee: Seems your code is really dumb! :unamused:",">>> :thumbsdown: It seems like it is not working!"]

celeb_sentence = [":fire: It is working awesome! :boom:","Finally it is working :v:"]



if "responding" not in db.keys():
    db["responding"] = True

#Condition to get random quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = "\'" + json_data[0]['q'] + "\' *-" + json_data[0]['a'] + "*"
    return (quote)

#Condition for adding encouraging statement
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

#Condition for deleting encoragaing statement
def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

#Function to add event to data base
def add_events(event, event_date, event_time):
  new_event = event, event_date, event_time
  if "events" in db.keys():
        events = db["events"]
        events.append(new_event)
        db["events"] = events
  else:
      db["events"] = [(new_event)]

#Function to delete event from the database
def delete_events(index):
  event = db["events"]
  if len(event) > index:
    del event[index]
    db["events"] = event

# code of random meme
def random_meme():
  url =  "https://meme-api.herokuapp.com/gimme"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  path = data["preview"][1]
  return path

#code of random joke
def random_joke():
  url = "https://api.jokes.one/joke/random"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  joke = data["joke"]
  return joke

#Function for youtube API to play music
title = []
def youtube_music(search):
  response = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?key="+"$YOUTUBE_API"+"&type=video&part=snippet&maxResult=20&q=" + search)
  data = json.loads(response.read())
  link_list = []
  item_len = len(data["items"])
  for i in range(item_len):
    video_id = data["items"][i]["id"]["videoId"]
    video_title = data["items"][i]["snippet"]["title"]
    link = "http://www.youtube.com/embed/"+ video_id
    video_discription = link, video_title

    link_list.append(video_discription)
    
  return link_list

servers = {}

# code for github api
repo_list = []

def github_search_user(user_name_to_search):
  response = urllib.request.urlopen("https://api.github.com/users/" + user_name_to_search )
  data = json.loads(response.read())
   
  github_url = data["html_url"]
  github_repos = data["repos_url"]
  user_name = data["login"]
  github_avatar_url = data["avatar_url"]
  github_follower = data["followers"]
  github_bio = data["bio"]
  github_following = data["following"]
  repo_state = urllib.request.urlopen(github_repos)
  repo_data = json.loads(repo_state.read())

  repo_length = len(repo_data)
  for i in range(repo_length):
    repo_list.append(repo_data[i]["full_name"])

  git_resource = [github_url,repo_length,user_name,github_avatar_url,github_follower,github_bio,github_following]
  return git_resource


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

#11 commands in total now 
    if msg.startswith('#help'):
        await message.channel.send(
            ">>> 1.  `{0}` - say hello to our bot\n2.  `{1}` - Gives you random inpirational quotes\n3.  `{2}` - add new encouragments senteces \n4.  `{3}` - delete the sentece/quote from the database. \n5.  `{4}`  - list all encouraging sentence\n6.  `{5} true/false` - responding on negative vibes word feature on/off\n7.  `{6}` - adds new event \n8.  `{7}` - list all the current event in the database\n9.  `{8}` - delete a event\n10. `{9}` : random meme\n11. `{10}` : return random joke\n12. `{11}` - view all commads\n13. `{12}` - to list all syntax\n14. `{13}` - celebrate with our bot\n15. `{14}` - get the link of a user github profile".format(cmd[0],cmd[1],cmd[2],cmd[3],cmd[4],cmd[5],cmd[6],cmd[7],cmd[8],cmd[9],cmd[10],cmd[11],cmd[12],cmd[13],cmd[14])
        )

#condition to see all the syntax commands
    if msg.startswith('#syntax'):
      await message.channel.send(">>> ` {} encouraging_quote/sentences\n {} index_value \n {} | event_name | event_date | event_time\n {} index_value `".format(cmd[2],cmd[3],cmd[6],cmd[8]))
#Conition to react on hello
    if msg.startswith(cmd[0]):

        await message.channel.send(">>> :wave: Hello! {0} ".format(message.author))

#Condition which returns random quote
    if msg.startswith(cmd[1]):
        quote = get_quote()
        await message.channel.send('{0}'.format(quote))

#Conditin to check the responding of negative words feature
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

#Condition to check weather a user typed a sad word
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

#Condition to add new sentences to our encouraging feature
    if msg.startswith(cmd[2]):
        encouraging_message = msg.split("/new-sentence ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send(">>> :+1: New encouraging message added.")

#Condition to delete a sentence typed by user
    if msg.startswith(cmd[3]):

        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("/del-sentence", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"].value

        await message.channel.send(">>> " + encouragements)

#Condition to list all encouraging statements present in data base
    if msg.startswith(cmd[4]):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]

        await message.channel.send(">>> " + db["encouragements"])

#Condition to turn on or off the encouraging feature
    if msg.startswith(cmd[5]):
      values = msg.split(cmd[5]+" ", 1)[1]

      if values.lower() == "true":
          db["responding"] = True
          await message.channel.send(">>> Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send(">>> Responding is off.")

#Condition to add new events in data base
    if msg.startswith(cmd[6]):
      msg_array = msg.split("|")
      event_name = msg_array[1]
      event_date = msg_array[2]
      event_time = msg_array[3]
      add_events(event_name, event_date, event_time)
      await message.channel.send(">>> :+1: New event added!")

#Condition to list all the events
    if msg.startswith(cmd[7]):
      events = db["events"].value
      for event_name, event_date, event_time in events:
          await message.channel.send(">>> **Event**: {} || **Date**: {} || **Time**: {}"
          .format(event_name, event_date, event_time))
    
#Condition to delete an event
    if msg.startswith(cmd[8]):
      index = int(msg.split(cmd[8],1)[1])
      delete_events(index)
      await message.channel.send(">>> :+1: Succesfully deleted the event")

#Condition to return random meme
    if msg.startswith(cmd[9]):
      meme = random_meme()
      await message.channel.send(meme)

#Condition to return random jokes
    if msg.startswith(cmd[10]):
      joke = random_joke()
      await message.channel.send(joke)

    
#Conditio for any one saying bad words
    if any(words in msg for words in bad_words):
      await message.channel.send(">>> ⚠ No stuff like this allowed here please!")

#Condition for celebrating
    if msg.startswith('#celebrate'):
      await message.channel.send(">>> "+ random .choice(celeb_sentence))


#Condition for yt [Under devlopment]
    if msg.startswith('#yt'):
      search = msg.split("#yt ",1)[1]
      await message.channel.send(search)
      music = youtube_music(search)
      vd_title1.append(music[0][1])
      vd_title2.append(music[1][1])
      vd_title3.append(music[2][1])
      vd_title4.append(music[3][1])

      vd_url1 = music[0][0]
      vd_url2 = music[1][0]
      vd_url3 = music[2][0]
      vd_url4 = music[3][0]
      embed = discord.Embed()
      embed.description = ("`1.` [{}]({}) \n\n`2.` [{}]({}) \n\n`3.` [{}]({}) \n\n`4.` [{}]({})\n\n".format(vd_title1,vd_url1,vd_title2,vd_url2,vd_title3,vd_url3,vd_title4,vd_url4))
      await message.channel.send(embed=embed)

#Condition for error
    if any(words in msg for words in code_not_working):
      await message.channel.send(random.choice(code_not_working_sentence))
      await message.channel.send(">>> :sunglasses: No free tip here!  \n:bulb: Get your butt to stack-overlflow")

#Condition for searching a user in github
    if msg.startswith(cmd[14]):
      user_to_be_searched = msg.split(" ",3)
      user_fname = user_to_be_searched[2]
      user = user_fname
      git_result = github_search_user(user)
      
      github_user_name = str(git_result[2])
      github_url = git_result[0]
      github_repo_size = str(git_result[1])
      github_avatar_url = git_result[3]
      github_followers = str(git_result[4])
      github_dis = str(git_result[5])
      github_following = str(git_result[6])

      embed=discord.Embed(description=github_dis, color=0xff1095 )
      embed.set_author(name = github_user_name, url=github_url, icon_url = github_avatar_url)
      embed.add_field(name = "Repository", value = github_repo_size,inline = False)
      embed.add_field(name = "Followers", value=github_followers,inline = True)
      embed.add_field(name = "Following", value=github_following,inline = True)
      embed.set_thumbnail(url= "https://i.ibb.co/VHgTs6q/Git-Hub-Mark-Light-32px.png")
      

      await message.channel.send(embed=embed)



#keeping the server running continuolsy 
keep_alive()

#BOT Token
client.run(os.getenv('TOKEN'))
