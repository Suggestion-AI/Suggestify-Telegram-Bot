import os 
import logging
import telebot
import downloader
from dotenv import load_dotenv

# base logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
#region Bot configuration
# Load environment variables
load_dotenv()
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

# Create bot 
bot = telebot.TeleBot(TG_BOT_TOKEN)
print('Bot is running...')
#endregion

#region Bot commands

#  /start 
@bot.message_handler(commands=['start'])
def help_command(message):
    bot.send_message(message.chat.id,"Help \n" +
                                     "----------------------- \n"
                                     "Spotify Downloader \n" +
                                     "/spotify [Enter spotify track url] \n" +
                                     "/spotify https://spotify/..... \n" +
                                     "----------------------- \n"
                                     )

# /spotify https://spotify.com/
@bot.message_handler(commands=['spotify'])
def send_url(message):
    if str(message.text).startswith("/spotify http"):
        url = str(message.text).replace("/spotify ","")

        bot.reply_to(message, "URL Received")
        logging.log(logging.INFO, 'URL Received')

        bot.send_message(message.chat.id,"Please Wait . . . ")

        # downloader 
        try:
            downloader.download(url=url ,message_id=message.message_id, chat_id=message.chat.id)
            bot.send_message(message.chat.id,"Download Completed")
        except:
            print("Download Error")
            logging.log(logging.ERROR, 'Download Error')
            bot.send_message(message.chat.id,"Download Error")

        # send audio
        try:
            sent = 0
            bot.send_message(message.chat.id,"Sending To You . . .")
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
            for file in files:
                bot.send_audio(chat_id=message.chat.id, audio=open(f'./{file}', 'rb'), timeout=1000)
                sent += 1
        except:
            print("Send Audio Error")
            logging.log(logging.ERROR, 'Send Audio Error')
            bot.send_message(message.chat.id,"Send Audio Error")

        # delete files
        # try:
        #     os.chdir('./..')
        #     os.system(f'rm -rf {message.message_id}{message.chat.id}')
        # except:
        #     print("delete files Error")
     
#endregion