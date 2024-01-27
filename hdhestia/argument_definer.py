from argparse import Namespace
from hdmailman import MailMan
from .callback_methods import CallbackHandler


class ArgumentDefiner:
    def __init__(self, args: Namespace):
        self._args = args
        self._mailman = MailMan(broker=args.broker)
        self._callback = CallbackHandler(args=args)

    @property
    def get_args(self):
        return self._args

    @property
    def callback(self):
        return self._callback.callback

    @property
    def broker(self):
        return self._mailman.broker

    def start_broker_consumer(self) -> None:
        self.broker.start_consuming(
            queue=self.get_args.queue,
            callback=self.callback
        )
