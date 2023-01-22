import pytest

import factory

from core.models import User
from goals.models import *


@pytest.fixture
def get_auth_client(client):
    def _get_auth_client(user):
        client.force_login(user=user)
        return client

    return _get_auth_client

