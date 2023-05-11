import os
import json
import logging
from dotenv import load_dotenv

# base logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#region Configurations
# load config
with open("config.json", "r") as read_file:
    config = json.load(read_file)
#endregion

#region Downloader
def download(url,message_id,chat_id):

    print("URL: ",url)
    logging.log(logging.INFO, f'URL: {url}')
    print("Chat ID: ",chat_id)
    logging.log(logging.INFO, f'Chat ID: {chat_id}')
    print("Message ID: ",message_id)
    logging.log(logging.INFO, f'Message ID: {message_id}')

    # make url
    url = "'" + url + "'"

    # directory
    os.system(f'mkdir -p temp/{message_id}{chat_id}')
    os.chdir(f'./temp/{message_id}{chat_id}')

    logging.log(logging.INFO, f'start downloading')

    # spotify downloader
    if config["SPOTDL_DOWNLOADER"]:
        os.system(f'spotdl {url}')
    elif config["SPOTIFYDL_DOWNLOADER"]:
        os.system(f'spotifydl {url}')
    else:
        logging.log(logging.ERROR, 'you should select one of downloader')
#endregion