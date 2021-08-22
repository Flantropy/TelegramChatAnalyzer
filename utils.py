import json
import logging
from io import BytesIO
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
    except KeyError as e:
        logging.getLogger().error(
            msg=f'Unable to form DataFrame from json. '
            f'Key "messages" not found. {e}'
        )
        return None
    else:
        messages_df.set_index('id', inplace=True)
        messages_df['date'] = pd.to_datetime(messages_df['date'])
        return messages_df


def _make_barplot(messages_df: pd.DataFrame):
    messages_per_month = messages_df['date'].groupby(messages_df['date'].dt.to_period('M')).agg('count')
    p = sns.barplot(
        x=messages_per_month.index,
        y=messages_per_month.values,
        color=(0.44, 0.35, 0.95)
    )
    plt.xticks(rotation=45)
    plt.title('All time history')
    buffer = BytesIO()
    p.figure.savefig(buffer)
    return buffer
