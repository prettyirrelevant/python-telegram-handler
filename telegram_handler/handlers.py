import logging
from io import BytesIO

import requests

from telegram_handler.formatters import HtmlFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.propagate = False

__all__ = ['TelegramHandler']


MAX_MESSAGE_LEN = 4096


class TelegramHandler(logging.Handler):
    API_ENDPOINT = 'https://api.telegram.org'

    def __init__(
        self,
        token,
        timeout=2,
        chat_id=None,
        proxies=None,
        level=logging.NOTSET,
        disable_notification=False,
        disable_web_page_preview=False,
    ):
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.chat_id = chat_id or self.get_chat_id()
        self.disable_notification = disable_notification
        self.disable_web_page_preview = disable_web_page_preview

        if not self.chat_id:
            level = logging.NOTSET
            logger.error('Did not get chat id. Setting handler logging level to NOTSET.')

        logger.info('Chat id: %s', self.chat_id)

        super().__init__(level=level)
        self.setFormatter(HtmlFormatter())

    def emit(self, record: logging.LogRecord):
        text = self.format(record)
        data = {
            'chat_id': self.chat_id,
            'disable_web_page_preview': self.disable_web_page_preview,
            'disable_notification': self.disable_notification,
        }

        if getattr(self.formatter, 'parse_mode', None):
            data['parse_mode'] = self.formatter.parse_mode

        try:
            if len(text) < MAX_MESSAGE_LEN:
                self.send_message(text, **data)
            else:
                self.send_document(text=text[:1000], document=BytesIO(text.encode()), **data)
        except:
            logger.exception('Error sending message/document with payload %s due to:', data)

    def send_message(self, text: str, **kwargs):
        kwargs.update({'text': text})
        return self.make_request('sendMessage', json=kwargs)

    def send_document(self, text: str, document: BytesIO, **kwargs):
        kwargs.update({'caption': text})
        return self.make_request(
            data=kwargs,
            method='sendDocument',
            files={'document': ('traceback.txt', document, 'text/plain')},
        )

    def make_request(self, method, **kwargs):
        url = self.format_url(method)

        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('proxies', self.proxies)

        response = requests.post(url, **kwargs)
        response.raise_for_status()

        return response.json()

    def get_chat_id(self):
        try:
            response = self.make_request('getUpdates')
        except:
            logger.exception('Request to method "getUpdates" failed due to:')
            return None

        try:
            return response['result'][-1]['message']['chat']['id']
        except:
            logger.exception('Error obtaining chat identifier from response, %s', response)
            return None

    def format_url(self, method):
        return f'{self.API_ENDPOINT}/bot{self.token}/{method}'
