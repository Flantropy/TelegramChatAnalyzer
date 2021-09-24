import logging

from telegram import LabeledPrice, ShippingOption, Update
from telegram.constants import PARSEMODE_HTML
from telegram.ext import CallbackContext

from src.doc import HELP_INFO
from src.utils import (
    _form_data_frame_from_json,
    _unpack_telegram_document,
    make_plots,
)


def start(update, context):
    """
    Greets user on chat startup
    """
    update.message.reply_text(text='Hello and welcome')


def help_info(update, context):
    update.message.reply_text(
        text=HELP_INFO,
        parse_mode=PARSEMODE_HTML
    )


def analyze_history(update, context):
    """
    This function
    """
    logging.getLogger().info('History Analyse function called')
    chat_json = _unpack_telegram_document(update)
    messages_df = _form_data_frame_from_json(chat_json)
    if messages_df is None:
        update.message.reply_text('Exit early. Invalid json')
        return
    photos = make_plots(messages_df)
    update.message.reply_media_group(media=photos)


def start_shipping_callback(update: Update, context: CallbackContext):
    update.message.reply_invoice(
        title='Invoce title',
        description='Invoce description',
        payload='My Payload',
        provider_token='r2e00dV1T',
        currency='USD',
        prices=[LabeledPrice('Test', 100)],
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


def start_noshipping_callback(update: Update, context: CallbackContext):
    update.message.reply_invoice(
        title='Invoice title',
        description='Invoice description',
        payload='My Payload',
        provider_token='r2e00dV1T',
        currency='USD',
        prices=[LabeledPrice('Test', 100)],
    )


def shipping_callback(update: Update, context: CallbackContext) -> None:
    query = update.shipping_query
    if query.invoice_payload != 'My Payload':
        query.answer(ok=False, error_message='Something went wrong')
        return
    
    options = [ShippingOption('1', 'Option A', [LabeledPrice('A', 100)])]
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Option B', price_list))
    
    query.answer(ok=True, shipping_options=options)


def pre_checkout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    params = dict(ok=True) if query.invoice_payload != 'My Payload' \
        else dict(ok=True, error_message='Something went wrong')
    
    query.answer(**params)
    # query.answer(ok=True) if query.invoice_payload != 'My Payload'\
    #     else query.answer(ok=False, error_message='Something went wrong')


def successful_payment(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Thank you for your payment')
