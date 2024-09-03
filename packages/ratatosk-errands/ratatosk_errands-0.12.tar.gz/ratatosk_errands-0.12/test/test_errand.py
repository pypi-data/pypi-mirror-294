import time

from dotenv import load_dotenv
from starlette.testclient import TestClient

from ratatosk_errands.model import Errand, TextToImageInstructions, ChatInstructions, ImageToImageInstructions


def test_text_to_image_errand():
    load_dotenv("../ratatosk.env")
    from ratatosk.main import app
    with TestClient(app) as client:
        errand = Errand(
            instructions=TextToImageInstructions(
                prompt="a textured oil painting of green pastures and still waters"
            ),
            origin="ratatosk",
            destination="ratatosk",
            identifier="green_pastures",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200


def test_image_to_image_errand():
    load_dotenv("../ratatosk.env")
    from ratatosk.main import app
    with TestClient(app) as client:
        errand = Errand(
            instructions=ImageToImageInstructions(
                prompt="a flock of squirrels",
                base_image_identifier="green_pastures"
            ),
            origin="ratatosk",
            destination="ratatosk",
            identifier="squirrels",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200


def test_chat_errand():
    load_dotenv("../ratatosk.env")
    from ratatosk.main import app
    with TestClient(app) as client:
        errand = Errand(
            instructions=ChatInstructions(
                prompt=""
            ),
            origin="ratatosk",
            destination="ratatosk",
            identifier="ratatosk",
            timestamp=time.time()
        )
        response = client.post("/give_errand", json=errand.model_dump())
        assert response.status_code == 200
