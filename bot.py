import os

from telegram.ext import Updater
import logging

token = os.environ['API_TOKEN']
updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)