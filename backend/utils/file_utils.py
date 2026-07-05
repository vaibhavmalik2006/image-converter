import json
import uuid
from pathlib import Path
from typing import Optional

TEMP_DIR = Path(__file__).resolve().parent.parent / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def get_temp_path(file_id: str) -> Path:
    metadata = read_metadata(file_id)
    if not metadata:
        return TEMP_DIR / f"{file_id}.bin"
    return TEMP_DIR / f"{file_id}{metadata.get('extension', '.bin')}"


def read_metadata(file_id: str) -> Optional[dict]:
    metadata_path = TEMP_DIR / f"{file_id}.json"
    if not metadata_path.exists():
        return None
    with metadata_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def create_temp_file(uploaded_file_name: str) -> tuple[str, Path, Path]:
    ext = Path(uploaded_file_name).suffix.lower() or ".bin"
    file_id = uuid.uuid4().hex
    temp_path = TEMP_DIR / f"{file_id}{ext}"
    metadata_path = TEMP_DIR / f"{file_id}.json"
    metadata = {"file_id": file_id, "filename": uploaded_file_name, "extension": ext}
    with metadata_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle)
    return file_id, temp_path, metadata_path


def cleanup_file(file_id: str) -> None:
    for candidate in [TEMP_DIR / f"{file_id}.*", TEMP_DIR / f"{file_id}.json"]:
        if candidate.exists():
            candidate.unlink(missing_ok=True)
    for path in TEMP_DIR.glob(f"{file_id}*"):
        if path.is_file():
            path.unlink(missing_ok=True)
