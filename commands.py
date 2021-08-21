import json
import logging
from io import BytesIO
from typing import Optional

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def start(update, context):
    """
    Greets user on chat startup
    """
    update.message.reply_text(text='Hello and welcome')


def echo(update, context):
    with open('C:\\Users\\User\\PycharmProjects\\TelegramChatAnalyzer\\bot\\my_image.jpg', 'rb') as image:
        update.message.reply_photo(photo=image.read())
    # update.message.reply_text(text=update.message.text)


def _unpack_telegram_document(update) -> dict:
    """
    This function retrieves JSON representation of a chat history
    from given telegram.Update
    """
    document = update.message.document.get_file()
    chat_file = BytesIO(document.download_as_bytearray())
    chat_json = json.load(chat_file)
    return chat_json


def _form_data_frame_from_json(chat_json) -> Optional[pd.DataFrame]:
    try:
        messages_df = pd.DataFrame(
            chat_json['messages'],
            columns=['id', 'type', 'date', 'from', 'text'])
    except KeyError:
        logging.getLogger().error(
            msg=f'Unable to form DataFrame from json. '
            f'Key "messages" not found.'
        )
        return None
    else:
        messages_df.set_index('id', inplace=True)
        messages_df['date'] = pd.to_datetime(messages_df['date'])
        return messages_df


def _make_plot(messages_df: pd.DataFrame):
    messages_per_month = messages_df['date'].groupby(messages_df['date'].dt.to_period('M')).agg('count')
    p = sns.barplot(
        x=messages_per_month.index,
        y=messages_per_month.values,
        color=(0.44, 0.35, 0.95)
    )
    plt.xticks(rotation=45)
    plt.title('Total messeges in each month')
    buffer = BytesIO()
    p.figure.savefig(buffer)
    return buffer


def analyze_history(update, context):
    """
    This function
    """
    logger = logging.getLogger()
    logger.info('History Analyse function called', )
    chat_json = _unpack_telegram_document(update)
    messages_df = _form_data_frame_from_json(chat_json)
    buffer_with_img = _make_plot(messages_df)
    # message = messages_df.head() if messages_df is not None else ''
    # update.message.reply_text(text=f'Response: {message}')
    update.message.reply_photo(photo=buffer_with_img.getvalue())
    buffer_with_img.close()
