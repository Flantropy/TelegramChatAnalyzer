import logging
from .utils import (
    _form_data_frame_from_json,
    _unpack_telegram_document,
    _make_barplot,
)


def start(update, context):
    """
    Greets user on chat startup
    """
    update.message.reply_text(text='Hello and welcome')


def echo(update, context):
    with open('C:\\Users\\User\\PycharmProjects\\TelegramChatAnalyzer\\bot\\my_image.jpg', 'rb') as image:
        update.message.reply_photo(photo=image.read())
    # update.message.reply_text(text=update.message.text)


def analyze_history(update, context):
    """
    This function
    """
    logging.getLogger().info('History Analyse function called', )
    chat_json = _unpack_telegram_document(update)
    messages_df = _form_data_frame_from_json(chat_json)
    buffer_with_img = _make_barplot(messages_df)
    update.message.reply_photo(photo=buffer_with_img.getvalue())
    buffer_with_img.close()
