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
    last_response = None

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

        if len(text) < MAX_MESSAGE_LEN:
            response = self.send_message(text, **data)
        else:
            response = self.send_document(text=text[:1000], document=BytesIO(text.encode()), **data)

        if response and not response.get('ok', False):
            logger.warning('Telegram responded with ok=false status! %s', response)

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
        response = None
        url = self.format_url(method)

        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('proxies', self.proxies)

        try:
            response = requests.post(url, **kwargs)
            self.last_response = response
            response.raise_for_status()
            return response.json()
        except:
            logger.exception('Error while making POST to %s', url)
            logger.debug(str(kwargs))
            if response is not None:
                logger.debug(response.content)

        return response

    def get_chat_id(self):
        response = self.make_request('getUpdates')
        if not response or not response.get('ok', False):
            logger.error('Telegram response is not ok: %s', str(response))
            return None

        try:
            return response['result'][-1]['message']['chat']['id']
        except:
            logger.exception('Something went terribly wrong while obtaining chat id')
            logger.debug(response)

    def format_url(self, method):
        return f'{self.API_ENDPOINT}/bot{self.token}/{method}'
