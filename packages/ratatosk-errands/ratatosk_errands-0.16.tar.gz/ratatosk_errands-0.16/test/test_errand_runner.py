import time

from starlette.testclient import TestClient

from errand_runner.main import app
from ratatosk_errands.model import Errand, TextToImageInstructions, ChatInstructions, ImageToImageInstructions


def test_text_to_image_errand():
    with TestClient(app) as client:
        errand = Errand(
            instructions=TextToImageInstructions(
                prompt="ratatosk ascending yggdrasil",
                image_identifier="ratatosk"
            ),
            origin="test",
            destination="test",
            errand_identifier="test",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200


def test_image_to_image_errand():
    with TestClient(app) as client:
        errand = Errand(
            instructions=ImageToImageInstructions(
                prompt="a flock of squirrels",
                image_identifier="squirrels",
                base_image_identifier="green_pastures"
            ),
            origin="test",
            destination="test",
            errand_identifier="test",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200


def test_chat_errand():
    with TestClient(app) as client:
        errand = Errand(
            instructions=ChatInstructions(
                prompt=""
            ),
            origin="ratatosk",
            destination="ratatosk",
            errand_identifier="ratatosk",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200
