import json
import logging
from io import BytesIO

import pandas as pd


def start(update, context):
    """
    Greets user on chat startup
    """
    update.message.reply_text(text='Hello and welcome')


def echo(update, context):
    update.message.reply_text(text=update)


def _unpack_telegram_document(update) -> dict:
    """
    This function retrieves JSON representation of a chat history
    from given telegram.Update
    """
    document = update.message.document.get_file()
    chat_file = BytesIO(document.download_as_bytearray())
    chat_json = json.load(chat_file)
    return chat_json


def analyze_history(update, context):
    """
    This function
    """
    logger = logging.getLogger()
    logger.info('History Analyse function called', )
    chat_json = _unpack_telegram_document(update)
    try:
        document = update.message.document.get_file()
    except AttributeError:
        message = 'Ooops...\nTry again'
    else:
        chat_file = BytesIO(document.download_as_bytearray())
        chat_json = json.load(chat_file)
        messages_df = pd.DataFrame(chat_json['messages'])  # KeyError possible
        message = f'Processing your file {messages_df.head()}'
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )
