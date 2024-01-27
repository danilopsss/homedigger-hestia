import pickle
from argparse import Namespace
from unittest.mock import patch
from hdhestia.callback_methods import CallbackHandler


@patch("sqlalchemy.orm.session.Session.commit")
@patch("sqlalchemy.orm.session.Session.add_all")
@patch("hdhestia.utils.advertisements.RentOfficeProcessor.process")
def test_callback_advertisements_with_valid_queue(process, addall, commit, pickled_rent_office_schema):
    arguments = Namespace(queue="scrapped")
    cb_handler = CallbackHandler(args=arguments)
    cb_handler._bulk_pre = [
        pickle.loads(pickled_rent_office_schema),
        *range(101)
    ]
    cb_handler.callback(pickled_rent_office_schema)
    assert process.called
    assert addall.called
    assert commit.called
