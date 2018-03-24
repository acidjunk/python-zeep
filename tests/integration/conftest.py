import uuid

import pytest


@pytest.fixture()
def ims_login_token():
    return str(uuid.uuid4())