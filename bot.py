import telebot
import json
from os import path
import sys

# Creamos el bot
if not path.isfile("bot.token"):
    print("Error: \"bot.token\" not found!")
    sys.exit()

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Abrimos la informacion para mencionar
if not path.isfile("./data/groups.json"):
    print("Error: \"./data/groups.json\" not found!")
    sys.exit()

with open("./data/groups.json", "r") as groups_file:
    global groups
    groups = json.load(groups_file)

# Handlers
@bot.message_handler(content_types=['new_chat_member'])
def greetings(m):
    if m.new_chat_member.username == 'iron_test_bot':
        bot.send_message(m.chat.id, "Hi! I'm a mentioner bot!\nClick here -> /addme@mentioner_2_bot or talk to be added automatically.")

@bot.message_handler(commands=['all'])
def mention(m):
    with open("./data/groups.json", "r") as groups_file:
        groups = json.load(groups_file)

    users_to_mention = ""
    for user in groups[str(m.chat.id)]:
        users_to_mention += "@" + user + " "

    users_to_mention += " -> " + m.text.split(' ', 1)[1]
    bot.send_message(m.chat.id, users_to_mention)

@bot.message_handler(commands=['addme'])
def addme(m):
    if m.chat.id in groups:
        if not m.from_user.username in groups[m.chat.id]:
            # Si no esta el usuario aniadido lo aniadimos
            groups[m.chat.id].append(m.from_user.username)
        else:
            # Si esta el usuario le avisamos
            bot.reply_to(m, "Already added!")
            return
    else:
        # Si el grupo no existe lo creamos y aniadimos al primer miembro
        groups[m.chat.id] = [m.from_user.username]

    # Guardamos al nuevo miembro
    with open("./data/groups.json", "w") as groups_file:
        groups_file.write(json.dumps(groups))

    bot.reply_to(m, "Added!")

@bot.message_handler(content_types=['text'])
def add(m):
    if m.chat.id in groups:
        if not m.from_user.username in groups[m.chat.id]:
            # Si no esta el usuario aniadido lo aniadimos
            groups[m.chat.id].append(m.from_user.username)
    else:
        # Si el grupo no existe lo creamos y aniadimos al primer miembro
        groups[m.chat.id] = [m.from_user.username]

    # Guardamos al nuevo miembro
    with open("./data/groups.json", "w") as groups_file:
        groups_file.write(json.dumps(groups))

# Skip pending!
bot.skip_pending = True

# Start the bot!
print("Running...")
bot.polling()
