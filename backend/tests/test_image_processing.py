import io
from PIL import Image
from fastapi.testclient import TestClient

from main import app


def test_download_applies_resize_and_format_changes():
    client = TestClient(app)

    image_bytes = io.BytesIO()
    image = Image.new("RGB", (200, 100), color=(255, 0, 0))
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    upload_response = client.post(
        "/upload",
        files={"file": ("test.png", image_bytes.getvalue(), "image/png")},
    )
    file_id = upload_response.json()["id"]

    response = client.get(
        f"/download/{file_id}",
        params={
            "output_format": "JPEG",
            "width": 50,
            "height": 25,
            "keep_aspect_ratio": False,
            "dpi": 150,
            "quality": 60,
            "target_size_kb": 0.5,
        },
    )

    assert response.status_code == 200
    processed = Image.open(io.BytesIO(response.content))
    assert processed.size == (50, 25)
    assert processed.format == "JPEG"
