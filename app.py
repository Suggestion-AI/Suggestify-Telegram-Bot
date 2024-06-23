import os
import telebot
import downloader
import suggest_spotify
from logger import get_logger
from dotenv import load_dotenv

# logger
logger = get_logger(__name__)

#region Bot configuration
# Load environment variables
load_dotenv()
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

# Create bot 
bot = telebot.TeleBot(TG_BOT_TOKEN)
#endregion

#region start 
# /start 
@bot.message_handler(commands=['start'])
def help_command(message):

    # info log
    logger.info("User: {} - /start".format(message.chat.username))

    # connect spotify
    suggest_spotify.spotify_connect()

    # send welcome and help messages
    bot.send_message(message.chat.id, "Welcome to the music Suggestify app!")
    bot.send_message(message.chat.id,
                                     "============================ \n" +
                                     "==========Suggestify========== \n" +
                                     "============================ \n" +
                                    #  "\n" +
                                    #  "Spotify Downloader \n" +
                                    #  "--------------------------------------- \n"
                                    #  "/spotify [Enter spotify track url] \n" +
                                    #  "/spotify https://spotify/..... \n" +
                                    #  "--------------------------------------- \n" +
                                     "\n" +
                                     "Suggest: Send (music) here \n"
                                     "--------------------------------------- \n"
                                     "/suggest_dl [Enter message] \n" +
                                     "/suggest_dl I happy very good day \n" +
                                     "--------------------------------------- \n"
                                     "\n"
                                     "Suggest: Send spotify playlist link here \n" +
                                     "--------------------------------------- \n"
                                     "/suggest [Enter message] \n" +
                                     "/suggest I happy very good day \n" +
                                     "--------------------------------------- \n" 
                                     )
#endregion

#region Spotify Downloader
# /spotify https://spotify.com/
# @bot.message_handler(commands=['spotify'])
# def spotify_downloader(message):
#     if str(message.text).startswith("/spotify http"):
#         url = str(message.text).replace("/spotify ","")
#         bot.reply_to(message, "URL Received")
#         bot.send_message(message.chat.id,"Please Wait . . . ")

#         # downloader 
#         try:
#             downloader.download(url=url ,message_id=message.message_id, chat_id=message.chat.id)
#             bot.send_message(message.chat.id,"Download Completed")
#         except:
#             bot.send_message(message.chat.id,"Error")
#             print("Download Error")

#         # send audio
#         try:
#             sent = 0
#             bot.send_message(message.chat.id,"Sending To You . . .")
#             files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
#             for file in files:
#                 bot.send_audio(chat_id=message.chat.id, audio=open(f'./{file}', 'rb'), timeout=1000)
#                 sent += 1
#         except:
#             bot.send_message(message.chat.id,"Error")
#             print("Send Audio Error")

        # delete files
        # try:
        #     os.chdir('./..')
        #     os.system(f'rm -rf {message.message_id}{message.chat.id}')
        # except:
        #     print("delete files Error")
#endregion

#region Suggest Music
# / suggest [Message]
@bot.message_handler()
def suggest_command(message):

    # info log
    logger.info("User: {} - /suggest".format(message.chat.username) + " - Suggestify Run" )

    # checking get command
    if str(message.text).startswith("/suggest"):
        msg = str(message.text).replace("/suggest ","")
        bot.reply_to(message, "Message Received")
        bot.send_message(message.chat.id,"Please Wait . . . ")
        
        # spotify
        try:
            playlist = suggest_spotify.suggest_music(playlist_name=message.chat.id, msg=msg)
            # info log
            logger.info("User: {} - /suggest".format(message.chat.username) + " - Suggestify Success")
            bot.send_message(message.chat.id,playlist)
            bot.send_message(message.chat.id,"Suggestify")
        except (ZeroDivisionError, ValueError) as e:
            print(f"Error occurred: {e}")
            # error log 
            logger.error("Error: User: {} - /suggest".format(message.chat.username) + " - Suggestify Error")
            bot.send_message(message.chat.id,"Error")
#endregion

#region Suggest Music and Download
# /suggest_dl [Message]
@bot.message_handler(commands=['suggest_dl'])
def suggest_dl_command(message):

    # info log
    logger.info("User: {} - /suggest_dl".format(message.chat.username) + " - Suggestify_dl Run")

    # checking get command
    if str(message.text).startswith("/suggest_dl"):
        msg = str(message.text).replace("/spotify_dl ","")
        bot.reply_to(message, "Message Received")
        bot.send_message(message.chat.id,"Please Wait . . . ")

        # spotify
        try:
            playlist = suggest_spotify.suggest_music(playlist_name=message.chat.id, msg=msg)
            # info log
            logger.info("User: {} - /suggest_dl".format(message.chat.username) + " - Suggestify_dl Success")
            bot.send_message(message.chat.id,playlist)
        except:
            # error log 
            logger.error("Error: User: {} - /suggest_dl".format(message.chat.username) + " - Suggestify_dl Error")
            bot.send_message(message.chat.id,"Error")
        
        # downloader 
        try:
            bot.send_message(message.chat.id,"Start Downloading ...")
            downloader.download(url=playlist ,message_id=message.message_id, chat_id=message.chat.id)
            # info log
            logger.info("User: {} - Download ".format(message.chat.username) + " - Download Success")
            bot.send_message(message.chat.id,"Download Completed")
        except:
            # error log 
            logger.error("Error: User: {} - Download ".format(message.chat.username) + " - Download Error")
            bot.send_message(message.chat.id,"Error")
            print("Download Error")

        # send audio
        try:
            sent = 0
            # info log
            logger.info("User: {} - Send Audio ".format(message.chat.username) + " - Start Send Audio")
            bot.send_message(message.chat.id,"Sending To You . . .")
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
            for file in files:
                bot.send_audio(chat_id=message.chat.id, audio=open(f'./{file}', 'rb'), timeout=1000)
                sent += 1
                # info log
                logger.info("User: {} - Send Audio ".format(message.chat.username) + f" - {sent} Success")

            # info log
            logger.info("User: {} - Send Audio ".format(message.chat.username) + " - Send Audio Success")
            bot.send_message(message.chat.id, "Suggestify")
        except:
            # error log 
            logger.error("Error: User: {} - Send Audio ".format(message.chat.username) + " - Send Audio Error")
            bot.send_message(message.chat.id,"Error")

#endregion
