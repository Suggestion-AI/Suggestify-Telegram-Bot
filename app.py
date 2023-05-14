import os
import telebot
import downloader
import suggest_spotify
from dotenv import load_dotenv

#region Bot configuration
# Load environment variables
load_dotenv()
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

# Create bot 
bot = telebot.TeleBot(TG_BOT_TOKEN)
print('Bot is running...')
#endregion

#region Bot commands
# /start 
@bot.message_handler(commands=['start'])
def help_command(message):
    suggest_spotify.spotify_connect()
    bot.send_message(message.chat.id,
                                     "============================ \n" +
                                     "==========Suggestify========== \n" +
                                     "============================ \n" +
                                     "\n" +
                                     "Spotify Downloader \n" +
                                     "--------------------------------------- \n"
                                     "/spotify [Enter spotify track url] \n" +
                                     "/spotify https://spotify/..... \n" +
                                     "--------------------------------------- \n" +
                                     "\n" +
                                     "Suggest Music Send to you \n"
                                     "--------------------------------------- \n"
                                     "/suggest_dl [Enter message] \n" +
                                     "/suggest_dl I happy very good day \n" +
                                     "--------------------------------------- \n"
                                     "\n"
                                     "Suggest Music Send to your Spotify Playlist \n" +
                                     "--------------------------------------- \n"
                                     "/suggest [Enter message] \n" +
                                     "/suggest I happy very good day \n" +
                                     "--------------------------------------- \n" 
                                     )

# /spotify https://spotify.com/
@bot.message_handler(commands=['spotify'])
def spotify_downloader(message):
    if str(message.text).startswith("/spotify http"):
        url = str(message.text).replace("/spotify ","")
        bot.reply_to(message, "URL Received")
        bot.send_message(message.chat.id,"Please Wait . . . ")

        # downloader 
        try:
            downloader.download(url=url ,message_id=message.message_id, chat_id=message.chat.id)
            bot.send_message(message.chat.id,"Download Completed")
        except:
            bot.send_message(message.chat.id,"Error")
            print("Download Error")

        # send audio
        try:
            sent = 0
            bot.send_message(message.chat.id,"Sending To You . . .")
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
            for file in files:
                bot.send_audio(chat_id=message.chat.id, audio=open(f'./{file}', 'rb'), timeout=1000)
                sent += 1
        except:
            bot.send_message(message.chat.id,"Error")
            print("Send Audio Error")

        # delete files
        # try:
        #     os.chdir('./..')
        #     os.system(f'rm -rf {message.message_id}{message.chat.id}')
        # except:
        #     print("delete files Error")

# / suggest [Message]
@bot.message_handler(commands=['suggest'])
def suggest_command(message):
    if str(message.text).startswith("/suggest"):
        msg = str(message.text).replace("/spotify ","")
        bot.reply_to(message, "Message Received")
        bot.send_message(message.chat.id,"Please Wait . . . ")

        try:
            playlist = suggest_spotify.suggest_music(playlist_name=message.chat.id, msg=msg)
            bot.send_message(message.chat.id,playlist)
            bot.send_message(message.chat.id,"Suggestify")
        except:
            bot.send_message(message.chat.id,"Error")
            print("Suggestify Error")

# /suggest_dl [Message]
@bot.message_handler(commands=['suggest_dl'])
def suggest_dl_command(message):
    if str(message.text).startswith("/suggest_dl"):
        msg = str(message.text).replace("/spotify_dl ","")
        bot.reply_to(message, "Message Received")
        bot.send_message(message.chat.id,"Please Wait . . . ")

        # spotify
        try:
            playlist = suggest_spotify.suggest_music(playlist_name=message.chat.id, msg=msg)
            bot.send_message(message.chat.id,playlist)
        except:
            bot.send_message(message.chat.id,"Error")
            print("Suggestify Error")
        
        # downloader 
        try:
            bot.send_message(message.chat.id,"Start Downloading ...")
            downloader.download(url=playlist ,message_id=message.message_id, chat_id=message.chat.id)
            bot.send_message(message.chat.id,"Download Completed")
        except:
            bot.send_message(message.chat.id,"Error")
            print("Download Error")

        # send audio
        try:
            sent = 0
            bot.send_message(message.chat.id,"Sending To You . . .")
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
            for file in files:
                bot.send_audio(chat_id=message.chat.id, audio=open(f'./{file}', 'rb'), timeout=1000)
                sent += 1
            bot.send_message(message.chat.id, "Suggestify")
        except:
            bot.send_message(message.chat.id,"Error")
            print("Send Audio Error")

#endregion