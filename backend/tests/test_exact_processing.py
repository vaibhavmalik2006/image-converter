import io
from PIL import Image
from fastapi.testclient import TestClient

from main import app


def test_exact_resize_and_dpi_and_format():
    client = TestClient(app)

    image_bytes = io.BytesIO()
    image = Image.new("RGB", (200, 200), color=(255, 0, 0))
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    upload_response = client.post(
        "/upload",
        files={"file": ("test.png", image_bytes.getvalue(), "image/png")},
    )
    assert upload_response.status_code == 200
    file_id = upload_response.json()["id"]

    response = client.get(
        f"/download/{file_id}",
        params={
            "output_format": "JPEG",
            "width": 10,
            "height": 10,
            "keep_aspect_ratio": False,
            "dpi": 150,
            "quality": 95,
            "target_size_kb": 10,
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    processed = Image.open(io.BytesIO(response.content))
    assert processed.size == (10, 10)
    assert processed.format == "JPEG"
    assert processed.info.get("dpi") == (150, 150)
