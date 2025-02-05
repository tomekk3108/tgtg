import logging
from notifiers.push_safer import PushSafer
from notifiers.smtp import SMTP
from notifiers.ifttt import IFTTT
from notifiers.webhook import WebHook
from notifiers.telegram import Telegram
from models import Config, Item

log = logging.getLogger('tgtg')


class Notifiers():
    def __init__(self, config: Config):
        self.push_safer = PushSafer(config)
        self.smtp = SMTP(config)
        self.ifttt = IFTTT(config)
        self.webhook = WebHook(config)
        self.telegram = Telegram(config)
        log.info("Activated notifiers:")
        if self.smtp.enabled:
            log.info("- SMTP: %s", self.smtp.recipient)
        if self.ifttt.enabled:
            log.info("- IFTTT: %s", self.ifttt.key)
        if self.push_safer.enabled:
            log.info("- PushSafer: %s", self.push_safer.key)
        if self.webhook.enabled:
            log.info("- WebHook: %s", self.webhook.url)
        if self.telegram.enabled:
            log.info("- Telegram: %s", self.telegram.chat_id)
        test_item = Item({"item": {"item_id": "12345","price_including_taxes": {"minor_units": 1099,"code": "EUR"}},
                        "display_name": "test_item",
                        "pickup_interval": {
                            "start": "2022-02-07T20:00:00Z",
                            "end": "2022-02-07T21:00:00Z"},
                        "items_available": 1})
        log.info("Sending test notifications ...")
        self.send(test_item)

    def send(self, item: Item):
        self.push_safer.send(item)
        self.smtp.send(item)
        self.ifttt.send(item)
        self.webhook.send(item)
        self.telegram.send(item)
