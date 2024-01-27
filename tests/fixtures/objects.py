import os
import pytest
import pickle
from collections import namedtuple
from hdmdata.schemas.advertisements import (
    RentOfficeSchema,
    AdvertisementsSchema
)

from hdmdata.models.advertisements import RentOffice


@pytest.fixture(autouse=True)
def pickled_rent_office_schema():
    rent_office = RentOfficeSchema(
        title="test",
        link="test_link",
        advertisements=[
            AdvertisementsSchema(
                title="advertisement_title",
                link="https://www.example.com",
                price=1000,
                parking=True,
                rooms=2,
                size=100
            )
        ]
    )
    return pickle.dumps(rent_office.model_dump())


@pytest.fixture(autouse=True)
def rent_office_schema():
    return RentOfficeSchema(
        title="test",
        link="test_link",
        advertisements=[
            AdvertisementsSchema(
                title="advertisement_title",
                link="https://www.example.com",
                price=1000,
                parking=True,
                rooms=2,
                size=100
            )
        ]
    ).model_dump()

@pytest.fixture(autouse=True)
def mock_db_get():
    return RentOffice(id=1, title="test", link="test_link")

@pytest.fixture(autouse=True)
def os_filling():
    envvars = [
        "DB_PROVIDER",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_DB",
    ]
    for i in envvars:
        os.environ[i] = "test"
