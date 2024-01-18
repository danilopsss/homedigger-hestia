import pickle
import logging

from argparse import Namespace
from hdmdata.types.get_by_type import by_
from hdmdata.database._session import get_session
from hdmdata.schemas.advertisements import RentOfficeSchema, AdvertisementsSchema


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
        if len(self._bulk_pre) >= self._chunk_size:
            for item in self._bulk_pre:
                rent_office_schema =  RentOfficeSchema(**item)
                by = by_(column="title", value=rent_office_schema.title)
                has_rent_office = rent_office_schema.get(by)

                if has_rent_office:
                    [(rent_office,)] = has_rent_office
                    for adv in item.get("advertisements", []):
                        adv_model = AdvertisementsSchema(**adv).to_dbmodel()
                        setattr(adv_model, 'rent_office_id', rent_office.id)
                        setattr(adv_model, 'rent_office', rent_office)
                        self._bulk_ready.append(adv_model)
                else:
                    rent_office_schema.save()
            self._bulk_pre.clear()

            with get_session() as session:
                for advert in self._bulk_ready:
                    try:
                        session.merge(advert)
                        session.commit()
                    except Exception as e:
                        logging.error(e)
                        session.rollback()
            self._bulk_ready.clear()
        else:
            self._bulk_pre.append(unserialized_body)

    def _callback_visited_links(self, *args):
        raise NotImplementedError("Not implemented yet")
        # body = args[-1]
        # unserialized_body = pickle.loads(body)
        # AdvertisementsMainLinkSchema(**unserialized_body).save()
