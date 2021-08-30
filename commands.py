import logging

from doc import HELP_INFO
from telegram.constants import PARSEMODE_HTML
from utils import (
    _form_data_frame_from_json,
    _unpack_telegram_document,
    make_plots
)


def start(update, context):
    """
    Greets user on chat startup
    """
    update.message.reply_text(text='Hello and welcome')


def help_info(update, context):
    update.message.reply_text(
        text=HELP_INFO,
        parse_mode=PARSEMODE_HTML,
        
    )
    

def analyze_history(update, context):
    """
    This function
    """
    logging.getLogger().info('History Analyse function called')
    chat_json = _unpack_telegram_document(update)
    messages_df = _form_data_frame_from_json(chat_json)
    # messages_df can be None
    photos = make_plots(messages_df)
    logging.getLogger().info(f'{[type(i) for i in photos]}')
    update.message.reply_media_group(media=photos)
