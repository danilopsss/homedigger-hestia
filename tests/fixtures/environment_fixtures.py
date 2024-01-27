import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def environment():
    with patch("os.getenv"):
        yield

@pytest.fixture(autouse=True)
def db_url():
    with patch("hdmdata.database._session.__get_url"):
        yield

@pytest.fixture(autouse=True)
def db_session2():
    with patch("hdmdata.database._session.get_session"):
        yield
