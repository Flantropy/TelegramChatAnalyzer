import json
import logging
from io import BytesIO
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from telegram import InputMediaPhoto


def __convert_plot_to_telegram_photo(plot) -> InputMediaPhoto:
    with BytesIO() as buffer:
        plot.figure.savefig(buffer)
        photo = InputMediaPhoto(buffer.getvalue())
    return photo


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
            columns=['id', 'type', 'date', 'from', 'text', 'media_type'])
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


def _make_barplot(messages_df: pd.DataFrame) -> InputMediaPhoto:
    """
    :param messages_df: DataFrame with user messaging history
    :return: telegram.InputMediaPhoto
    """
    messages_per_month = messages_df['date'] \
        .groupby(messages_df['date'].dt.to_period('M')) \
        .agg('count')
    plot = sns.barplot(
        x=messages_per_month.index,
        y=messages_per_month.values,
        color=(0.44, 0.35, 0.95)
    )
    plt.xticks(rotation=45)
    plt.title('All time history')
    return __convert_plot_to_telegram_photo(plot)


def _make_kde_plot(messages_df: pd.DataFrame) -> InputMediaPhoto:
    plt.close()
    plot = sns.kdeplot(
        x=messages_df['date'],
        hue=messages_df['from'],
        shade=True
    )
    plt.title('Activity by user')
    plt.xticks(rotation=45)
    plt.xlabel('')
    return __convert_plot_to_telegram_photo(plot)


def _make_media_distribution_bar_plot(messages_df: pd.DataFrame) -> InputMediaPhoto:
    plt.close()
    sns.set_theme(context='paper')
    r = messages_df[['from', 'media_type']].value_counts()
    media_dist_plot = r.unstack().plot(
        kind='bar',
        stacked=True,
        ylabel='Media messages',
        xlabel='User'
    )
    plt.xticks(rotation=0)
    plt.title('Distribution of media messages')
    return __convert_plot_to_telegram_photo(media_dist_plot)


def make_plots(messages_df: pd.DataFrame) -> List[InputMediaPhoto]:
    return [
        _make_barplot(messages_df),
        _make_media_distribution_bar_plot(messages_df),
        _make_kde_plot(messages_df),
    ]
