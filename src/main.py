import logging
import os

import telegram.ext as tg

from src.commands import (
    analyze_history, help_info, pre_checkout_callback, shipping_callback, start,
    start_noshipping_callback, start_shipping_callback, successful_payment,
)


def main():
    # Setting up a basic logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Creating updater and dispatcher for bot
    updater = tg.Updater(token=os.getenv('BOT_TOKEN'))
    dispatcher: tg.Dispatcher = updater.dispatcher

    # Filters
    json_only_filter = tg.Filters.document.file_extension('json')

    # Creating handlers
    handlers = [
        tg.CommandHandler('start', start),
        tg.CommandHandler('help', help_info),
        tg.CommandHandler('shipping', start_shipping_callback),
        tg.CommandHandler('noshipping', start_noshipping_callback),
        tg.PreCheckoutQueryHandler(pre_checkout_callback),
        tg.ShippingQueryHandler(shipping_callback),
        tg.MessageHandler(json_only_filter, analyze_history),
        tg.MessageHandler(tg.Filters.successful_payment, successful_payment),
    ]

    # Adding handlers
    for handler in handlers:
        dispatcher.add_handler(handler)

    # Start polling for updates
    updater.start_polling(poll_interval=5)
    updater.idle()


if __name__ == '__main__':
    main()
