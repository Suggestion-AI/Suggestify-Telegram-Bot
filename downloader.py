import os
import json
from logger import get_logger

# base logger
logger = get_logger(__name__)

#region Configurations
# load config
with open("config.json", "r") as read_file:
    config = json.load(read_file)
#endregion

#region Downloader
def download(url,message_id,chat_id):

    print("URL: ",url)
    print("Chat ID: ",chat_id)
    print("Message ID: ",message_id)

    # make url
    url = "'" + url + "'"

    # directory
    os.system(f'mkdir -p temp/{message_id}{chat_id}')
    os.chdir(f'./temp/{message_id}{chat_id}')

    logger.info(f'current directory: {os.getcwd()}')
    logger.info(f'start downloading')
                
    # spotify downloader
    if config["SPOTDL_DOWNLOADER"]:
        os.system(f'spotdl {url}')
    elif config["SPOTIFYDL_DOWNLOADER"]:
        os.system(f'spotifydl {url}')
    else:
        logger.log(logging.ERROR, 'you should select one of downloader')
#endregion
