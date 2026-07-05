import io
from PIL import Image
from fastapi.testclient import TestClient

from main import app


def test_target_size_jpeg_near_10kb():
    client = TestClient(app)

    image_bytes = io.BytesIO()
    image = Image.new("RGB", (500, 500), color=(123, 222, 100))
    image.save(image_bytes, format="JPEG", quality=95)
    image_bytes.seek(0)

    upload_response = client.post(
        "/upload",
        files={"file": ("test.jpg", image_bytes.getvalue(), "image/jpeg")},
    )
    assert upload_response.status_code == 200
    file_id = upload_response.json()["id"]

    response = client.get(
        f"/download/{file_id}",
        params={
            "output_format": "JPEG",
            "target_size_kb": 10,
            "quality": 95,
        },
    )

    assert response.status_code == 200
    processed = Image.open(io.BytesIO(response.content))
    size_kb = len(response.content) / 1024
    assert processed.format == "JPEG"
    assert size_kb <= 15
