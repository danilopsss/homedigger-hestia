import pickle
import logging

from argparse import Namespace
from hdmdata.database._session import get_session
from hdhestia.utils.advertisements import RentOfficeProcessor


logging.basicConfig(filename="app.log", level=logging.INFO)


class CallbackHandler:
    def __init__(self, args: Namespace):
        self._bulk_pre = []
        self._bulk_ready = []
        self._args = args
        self._chunk_size = 100
        self._queue_mapping = {
            "scrapped": "_callback_advertisements",
            "visited": "_callback_visited_links",
        }

    def callback(self, *args) -> callable:
        topic = self._args.queue.split(".")[-1]
        method_name = self._queue_mapping.get(topic, "")
        if not (callback_ := getattr(self, method_name, None)):
            raise NotImplementedError(f"Callback method {method_name} not implemented")
        return callback_(*args)

    def _callback_advertisements(self, *args):
        body = args[-1]
        unserialized_body = pickle.loads(body)
        if not len(self._bulk_pre) >= self._chunk_size:
            self._bulk_pre.append(unserialized_body)
        else:
            breakpoint()
            processed = RentOfficeProcessor(self._bulk_pre).process()
            with get_session() as session:
                try:
                    session.add_all(processed)
                    session.commit()
                except Exception as e:
                    logging.error(e)
                    session.rollback()
            self._bulk_pre.clear()


    def _callback_visited_links(self, *args):
        raise NotImplementedError("Not implemented yet")
        # body = args[-1]
        # unserialized_body = pickle.loads(body)
        # AdvertisementsMainLinkSchema(**unserialized_body).save()
