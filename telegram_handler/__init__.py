import argparse
import logging
import sys

from telegram_handler.handlers import TelegramHandler

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser('Telegram Logging Handler', description='Helps to retrieve chat_id')
    parser.add_argument('token')

    args = parser.parse_args()
    token = args.token

    handler = TelegramHandler(token, 'foo')
    chat_id = handler.get_chat_id()
    if not chat_id:
        logger.info('Did not get chat id')
        logger.info(handler.last_response.status_code, handler.last_response.text)
        sys.exit(-1)

    logger.info(chat_id)


if __name__ == '__main__':  # pragma: no cover
    main()
