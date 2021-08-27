import os
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    Dispatcher
)
from commands import (
    start,
    echo,
    analyze_history,
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
    updater = Updater(token=os.getenv('BOT_TOKEN'))
    dispatcher: Dispatcher = updater.dispatcher
    
    # Filters
    file_extension_filter = Filters.document.file_extension('json')
    
    # Creating handlers
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    analyze_history_handler = MessageHandler(file_extension_filter, analyze_history)

    # Adding handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(analyze_history_handler)
    
    # Starts polling to telegram for updates
    updater.start_polling(poll_interval=5)
    updater.idle()
    

if __name__ == '__main__':
    main()
