import os 
import telebot
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
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
#endregion