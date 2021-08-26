########################
#    DEPENDENCIES      #
########################

# pip install pytest


########################
#        IMPORTS       #
########################


from fastapi.testclient import TestClient
from .api import app

########################
#      TESTS API       #
########################


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}